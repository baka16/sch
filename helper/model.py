import django
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.db import connection, models, router, transaction
from django.db.models.constants import LOOKUP_SEP
from django.db.models.fields.related import OneToOneField, OneToOneRel
from django.db.models.functions import Now
from django.db.models.query import ModelIterable, QuerySet
from django.db.models.signals import post_save, pre_save
from django.db.models.sql.datastructures import Join
from django.utils.translation import ugettext_lazy as _
from .ect import (AutoCreatedField, AutoLastModifiedField, MonitorField, StatusField, UUIDField)
# from model_utils.managers import QueryManager, SoftDeletableManager

now = Now()


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.

    """
    created = AutoCreatedField(_('created'))
    modified = AutoLastModifiedField(_('modified'))

    class Meta:
        abstract = True


class TimeFramedModel(models.Model):
    """
    An abstract base class model that provides ``start``
    and ``end`` fields to record a timeframe.

    """
    start = models.DateTimeField(_('start'), null=True, blank=True)
    end = models.DateTimeField(_('end'), null=True, blank=True)

    class Meta:
        abstract = True


class StatusModel(models.Model):
    """
    An abstract base class model with a ``status`` field that
    automatically uses a ``STATUS`` class attribute of choices, a
    ``status_changed`` date-time field that records when ``status``
    was last modified, and an automatically-added manager for each
    status that returns objects with that status only.

    """
    status = StatusField(_('status'))
    status_changed = MonitorField(_('status changed'), monitor='status')

    class Meta:
        abstract = True


def add_status_query_managers(sender, **kwargs):
    """
    Add a Querymanager for each status item dynamically.

    """
    if not issubclass(sender, StatusModel):
        return

    default_manager = sender._meta.default_manager

    for value, display in getattr(sender, 'STATUS', ()):
        if _field_exists(sender, value):
            raise ImproperlyConfigured(
                "StatusModel: Model '%s' has a field named '%s' which "
                "conflicts with a status of the same name."
                % (sender.__name__, value)
            )
        sender.add_to_class(value, QueryManager(status=value))

    sender._meta.default_manager_name = default_manager.name


def add_timeframed_query_manager(sender, **kwargs):
    """
    Add a QueryManager for a specific timeframe.

    """
    if not issubclass(sender, TimeFramedModel):
        return
    if _field_exists(sender, 'timeframed'):
        raise ImproperlyConfigured(
            "Model '%s' has a field named 'timeframed' "
            "which conflicts with the TimeFramedModel manager."
            % sender.__name__
        )
    sender.add_to_class('timeframed', QueryManager(
        (models.Q(start__lte=now) | models.Q(start__isnull=True))
        & (models.Q(end__gte=now) | models.Q(end__isnull=True))
    ))


models.signals.class_prepared.connect(add_status_query_managers)
models.signals.class_prepared.connect(add_timeframed_query_manager)


def _field_exists(model_class, field_name):
    return field_name in [f.attname for f in model_class._meta.local_fields]


class SoftDeletableModel(models.Model):
    """
    An abstract base class model with a ``is_removed`` field that
    marks entries that are not going to be used anymore, but are
    kept in db for any reason.
    Default manager returns only not-removed entries.
    """
    is_removed = models.BooleanField(default=False)

    class Meta:
        abstract = True

    objects = SoftDeletableManager()
    all_objects = models.Manager()

    def delete(self, using=None, soft=True, *args, **kwargs):
        """
        Soft delete object (set its ``is_removed`` field to True).
        Actually delete object if setting ``soft`` to False.
        """
        if soft:
            self.is_removed = True
            self.save(using=using)
        else:
            return super().delete(using=using, *args, **kwargs)


class UUIDModel(models.Model):
    """
    This abstract base class provides id field on any model that inherits from it
    which will be the primary key.
    """
    id = UUIDField(
        primary_key=True,
        version=4,
        editable=False,
    )

    class Meta:
        abstract = True


class SaveSignalHandlingModel(models.Model):
    """
    An abstract base class model to pass a parameter ``signals_to_disable``
    to ``save`` method in order to disable signals
    """
    class Meta:
        abstract = True

    def save(self, signals_to_disable=None, *args, **kwargs):
        """
        Add an extra parameters to hold which signals to disable
        If empty, nothing will change
        """

        self.signals_to_disable = signals_to_disable or []

        super().save(*args, **kwargs)

    def save_base(self, raw=False, force_insert=False,
                  force_update=False, using=None, update_fields=None):
        """
        Copied from base class for a minor change.
        This is an ugly overwriting but since Django's ``save_base`` method
        does not differ between versions 1.8 and 1.10,
        that way of implementing wouldn't harm the flow
        """
        using = using or router.db_for_write(self.__class__, instance=self)
        assert not (force_insert and (force_update or update_fields))
        assert update_fields is None or len(update_fields) > 0
        cls = origin = self.__class__

        if cls._meta.proxy:
            cls = cls._meta.concrete_model
        meta = cls._meta
        if not meta.auto_created and 'pre_save' not in self.signals_to_disable:
            pre_save.send(
                sender=origin, instance=self, raw=raw, using=using,
                update_fields=update_fields,
            )
        with transaction.atomic(using=using, savepoint=False):
            if not raw:
                self._save_parents(cls, using, update_fields)
            updated = self._save_table(
                raw, cls, force_insert, force_update, using, update_fields)

        self._state.db = using
        self._state.adding = False

        if not meta.auto_created and 'post_save' not in self.signals_to_disable:
            post_save.send(
                sender=origin, instance=self, created=(not updated),
                update_fields=update_fields, raw=raw, using=using,
            )

        # Empty the signals in case it might be used somewhere else in future
        self.signals_to_disable = []


class InheritanceIterable(ModelIterable):
    def __iter__(self):
        queryset = self.queryset
        iter = ModelIterable(queryset)
        if getattr(queryset, 'subclasses', False):
            extras = tuple(queryset.query.extra.keys())
            # sort the subclass names longest first,
            # so with 'a' and 'a__b' it goes as deep as possible
            subclasses = sorted(queryset.subclasses, key=len, reverse=True)
            for obj in iter:
                sub_obj = None
                for s in subclasses:
                    sub_obj = queryset._get_sub_obj_recurse(obj, s)
                    if sub_obj:
                        break
                if not sub_obj:
                    sub_obj = obj

                if getattr(queryset, '_annotated', False):
                    for k in queryset._annotated:
                        setattr(sub_obj, k, getattr(obj, k))

                for k in extras:
                    setattr(sub_obj, k, getattr(obj, k))

                yield sub_obj
        else:
            yield from iter


class InheritanceQuerySetMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._iterable_class = InheritanceIterable

    def select_subclasses(self, *subclasses):
        levels = None
        calculated_subclasses = self._get_subclasses_recurse(
            self.model, levels=levels)
        # if none were passed in, we can just short circuit and select all
        if not subclasses:
            subclasses = calculated_subclasses
        else:
            verified_subclasses = []
            for subclass in subclasses:
                # special case for passing in the same model as the queryset
                # is bound against. Rather than raise an error later, we know
                # we can allow this through.
                if subclass is self.model:
                    continue

                if not isinstance(subclass, (str,)):
                    subclass = self._get_ancestors_path(
                        subclass, levels=levels)

                if subclass in calculated_subclasses:
                    verified_subclasses.append(subclass)
                else:
                    raise ValueError(
                        '{!r} is not in the discovered subclasses, tried: {}'.format(
                            subclass, ', '.join(calculated_subclasses))
                    )
            subclasses = verified_subclasses

        # workaround https://code.djangoproject.com/ticket/16855
        previous_select_related = self.query.select_related
        new_qs = self.select_related(*subclasses)
        previous_is_dict = isinstance(previous_select_related, dict)
        new_is_dict = isinstance(new_qs.query.select_related, dict)
        if previous_is_dict and new_is_dict:
            new_qs.query.select_related.update(previous_select_related)
        new_qs.subclasses = subclasses
        return new_qs

    def _chain(self, **kwargs):
        for name in ['subclasses', '_annotated']:
            if hasattr(self, name):
                kwargs[name] = getattr(self, name)

        return super()._chain(**kwargs)

    def _clone(self, klass=None, setup=False, **kwargs):
        if django.VERSION >= (2, 0):
            qs = super()._clone()
            for name in ['subclasses', '_annotated']:
                if hasattr(self, name):
                    setattr(qs, name, getattr(self, name))
            return qs

        for name in ['subclasses', '_annotated']:
            if hasattr(self, name):
                kwargs[name] = getattr(self, name)

        return super()._clone(**kwargs)

    def annotate(self, *args, **kwargs):
        qset = super().annotate(*args, **kwargs)
        qset._annotated = [a.default_alias for a in args] + list(kwargs.keys())
        return qset

    def _get_subclasses_recurse(self, model, levels=None):
        """
        Given a Model class, find all related objects, exploring children
        recursively, returning a `list` of strings representing the
        relations for select_related
        """
        related_objects = [
            f for f in model._meta.get_fields()
            if isinstance(f, OneToOneRel)]

        rels = [
            rel for rel in related_objects
            if isinstance(rel.field, OneToOneField)
            and issubclass(rel.field.model, model)
            and model is not rel.field.model
            and rel.parent_link
        ]

        subclasses = []
        if levels:
            levels -= 1
        for rel in rels:
            if levels or levels is None:
                for subclass in self._get_subclasses_recurse(
                        rel.field.model, levels=levels):
                    subclasses.append(
                        rel.get_accessor_name() + LOOKUP_SEP + subclass)
            subclasses.append(rel.get_accessor_name())
        return subclasses

    def _get_ancestors_path(self, model, levels=None):
        """
        Serves as an opposite to _get_subclasses_recurse, instead walking from
        the Model class up the Model's ancestry and constructing the desired
        select_related string backwards.
        """
        if not issubclass(model, self.model):
            raise ValueError(
                "{!r} is not a subclass of {!r}".format(model, self.model))

        ancestry = []
        # should be a OneToOneField or None
        parent_link = model._meta.get_ancestor_link(self.model)
        if levels:
            levels -= 1
        while parent_link is not None:
            related = parent_link.remote_field
            ancestry.insert(0, related.get_accessor_name())
            if levels or levels is None:
                parent_model = related.model
                parent_link = parent_model._meta.get_ancestor_link(
                    self.model)
            else:
                parent_link = None
        return LOOKUP_SEP.join(ancestry)

    def _get_sub_obj_recurse(self, obj, s):
        rel, _, s = s.partition(LOOKUP_SEP)

        try:
            node = getattr(obj, rel)
        except ObjectDoesNotExist:
            return None
        if s:
            child = self._get_sub_obj_recurse(node, s)
            return child
        else:
            return node

    def get_subclass(self, *args, **kwargs):
        return self.select_subclasses().get(*args, **kwargs)


class InheritanceQuerySet(InheritanceQuerySetMixin, QuerySet):
    pass

    def instance_of(self, *models):
        """
        Fetch only objects that are instances of the provided model(s).
        """
        # If we aren't already selecting the subclasess, we need
        # to in order to get this to work.

        # How can we tell if we are not selecting subclasses?

        # Is it safe to just apply .select_subclasses(*models)?

        # Due to https://code.djangoproject.com/ticket/16572, we
        # can't really do this for anything other than children (ie,
        # no grandchildren+).
        where_queries = []
        for model in models:
            where_queries.append('(' + ' AND '.join([
                '"{}"."{}" IS NOT NULL'.format(
                    model._meta.db_table,
                    field.attname,  # Should this be something else?
                ) for field in model._meta.parents.values()
            ]) + ')')

        return self.select_subclasses(*models).extra(where=[' OR '.join(where_queries)])


class InheritanceManagerMixin:
    _queryset_class = InheritanceQuerySet

    def get_queryset(self):
        return self._queryset_class(self.model)

    def select_subclasses(self, *subclasses):
        return self.get_queryset().select_subclasses(*subclasses)

    def get_subclass(self, *args, **kwargs):
        return self.get_queryset().get_subclass(*args, **kwargs)

    def instance_of(self, *models):
        return self.get_queryset().instance_of(*models)


class InheritanceManager(InheritanceManagerMixin, models.Manager):
    pass


class QueryManagerMixin:

    def __init__(self, *args, **kwargs):
        if args:
            self._q = args[0]
        else:
            self._q = models.Q(**kwargs)
        self._order_by = None
        super().__init__()

    def order_by(self, *args):
        self._order_by = args
        return self

    def get_queryset(self):
        qs = super().get_queryset().filter(self._q)
        if self._order_by is not None:
            return qs.order_by(*self._order_by)
        return qs


class QueryManager(QueryManagerMixin, models.Manager):
    pass


class SoftDeletableQuerySetMixin:
    """
    QuerySet for SoftDeletableModel. Instead of removing instance sets
    its ``is_removed`` field to True.
    """

    def delete(self):
        """
        Soft delete objects from queryset (set their ``is_removed``
        field to True)
        """
        self.update(is_removed=True)


class SoftDeletableQuerySet(SoftDeletableQuerySetMixin, QuerySet):
    pass


class SoftDeletableManagerMixin:
    """
    Manager that limits the queryset by default to show only not removed
    instances of model.
    """
    _queryset_class = SoftDeletableQuerySet

    def get_queryset(self):
        """
        Return queryset limited to not removed entries.
        """
        kwargs = {'model': self.model, 'using': self._db}
        if hasattr(self, '_hints'):
            kwargs['hints'] = self._hints

        return self._queryset_class(**kwargs).filter(is_removed=False)


class SoftDeletableManager(SoftDeletableManagerMixin, models.Manager):
    pass


class JoinQueryset(models.QuerySet):

    def get_quoted_query(self, query):
        query, params = query.sql_with_params()

        # Put additional quotes around string.
        params = [
            '\'{}\''.format(p)
            if isinstance(p, str) else p
            for p in params
        ]

        # Cast list of parameters to tuple because I got
        # "not enough format characters" otherwise.
        params = tuple(params)
        return query % params

    def join(self, qs=None):
        '''
        Join one queryset together with another using a temporary table. If
        no queryset is used, it will use the current queryset and join that
        to itself.

        `Join` either uses the current queryset and effectively does a self-join to
        create a new limited queryset OR it uses a querset given by the user.

        The model of a given queryset needs to contain a valid foreign key to
        the current queryset to perform a join. A new queryset is then created.
        '''
        to_field = 'id'

        if qs:
            fk = [
                fk for fk in qs.model._meta.fields
                if getattr(fk, 'related_model', None) == self.model
            ]
            fk = fk[0] if fk else None
            model_set = '{}_set'.format(self.model.__name__.lower())
            key = fk or getattr(qs.model, model_set, None)

            if not key:
                raise ValueError('QuerySet is not related to current model')

            try:
                fk_column = key.column
            except AttributeError:
                fk_column = 'id'
                to_field = key.field.column

            qs = qs.only(fk_column)
            # if we give a qs we need to keep the model qs to not lose anything
            new_qs = self
        else:
            fk_column = 'id'
            qs = self.only(fk_column)
            new_qs = self.model.objects.all()

        TABLE_NAME = 'temp_stuff'
        query = self.get_quoted_query(qs.query)
        sql = '''
            DROP TABLE IF EXISTS {table_name};
            DROP INDEX IF EXISTS {table_name}_id;
            CREATE TEMPORARY TABLE {table_name} AS {query};
            CREATE INDEX {table_name}_{fk_column} ON {table_name} ({fk_column});
        '''.format(table_name=TABLE_NAME, fk_column=fk_column, query=str(query))

        with connection.cursor() as cursor:
            cursor.execute(sql)

        class TempModel(models.Model):
            temp_key = models.ForeignKey(
                self.model,
                on_delete=models.DO_NOTHING,
                db_column=fk_column,
                to_field=to_field
            )

            class Meta:
                managed = False
                db_table = TABLE_NAME

        conn = Join(
            table_name=TempModel._meta.db_table,
            parent_alias=new_qs.query.get_initial_alias(),
            table_alias=None,
            join_type='INNER JOIN',
            join_field=self.model.tempmodel_set.rel,
            nullable=False
        )
        new_qs.query.join(conn, reuse=None)
        return new_qs


class JoinManagerMixin:
    """
    Manager that adds a method join. This method allows you to join two querysets together.
    """
    _queryset_class = JoinQueryset

    def get_queryset(self):
        return self._queryset_class(model=self.model, using=self._db)


class JoinManager(JoinManagerMixin, models.Manager):
    pass