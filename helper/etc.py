import copy
import django
import uuid
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.timezone import now

DEFAULT_CHOICES_NAME = 'STATUS'


class AutoCreatedField(models.DateTimeField):
    """
    A DateTimeField that automatically populates itself at
    object creation.
    By default, sets editable=False, default=datetime.now.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('default', now)
        super().__init__(*args, **kwargs)


class AutoLastModifiedField(AutoCreatedField):
    """
    A DateTimeField that updates itself on each save() of the model.
    By default, sets editable=False and default=datetime.now.
    """

    def get_default(self):
        # Return the default value for this field.
        if not hasattr(self, "_default"):
            self._default = self._get_default()
        return self._default

    def pre_save(self, model_instance, add):
        value = now()
        if add:
            current_value = getattr(
                model_instance, self.attname, self.get_default())
            if current_value != self.get_default():
                # when creating an instance and the modified date is set
                # don't change the value, assume the developer wants that
                # control.
                value = getattr(model_instance, self.attname)
            else:
                for field in model_instance._meta.get_fields():
                    if isinstance(field, AutoCreatedField):
                        value = getattr(model_instance, field.name)
                        break
        setattr(model_instance, self.attname, value)
        return value


class StatusField(models.CharField):
    """
    A CharField that looks for a ``STATUS`` class-attribute and
    automatically uses that as ``choices``. The first option in
    ``STATUS`` is set as the default.

    Also has a default max_length so you don't have to worry about
    setting that.

    Also features a ``no_check_for_status`` argument to make sure
    South can handle this field when it freezes a model.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 100)
        self.check_for_status = not kwargs.pop('no_check_for_status', False)
        self.choices_name = kwargs.pop('choices_name', DEFAULT_CHOICES_NAME)
        super().__init__(*args, **kwargs)

    def prepare_class(self, sender, **kwargs):
        if not sender._meta.abstract and self.check_for_status:
            assert hasattr(sender, self.choices_name), \
                "To use StatusField, the model '%s' must have a %s choices class attribute." \
                % (sender.__name__, self.choices_name)
            self.choices = getattr(sender, self.choices_name)
            if not self.has_default():
                self.default = tuple(getattr(sender, self.choices_name))[
                    0][0]  # set first as default

    def contribute_to_class(self, cls, name):
        models.signals.class_prepared.connect(self.prepare_class, sender=cls)
        # we don't set the real choices until class_prepared (so we can rely on
        # the STATUS class attr being available), but we need to set some dummy
        # choices now so the super method will add the get_FOO_display method
        self.choices = [(0, 'dummy')]
        super().contribute_to_class(cls, name)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['no_check_for_status'] = True
        return name, path, args, kwargs


class MonitorField(models.DateTimeField):
    """
    A DateTimeField that monitors another field on the same model and
    sets itself to the current date/time whenever the monitored field
    changes.

    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', now)
        monitor = kwargs.pop('monitor', None)
        if not monitor:
            raise TypeError(
                '%s requires a "monitor" argument' % self.__class__.__name__)
        self.monitor = monitor
        when = kwargs.pop('when', None)
        if when is not None:
            when = set(when)
        self.when = when
        super().__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        self.monitor_attname = '_monitor_%s' % name
        models.signals.post_init.connect(self._save_initial, sender=cls)
        super().contribute_to_class(cls, name)

    def get_monitored_value(self, instance):
        return getattr(instance, self.monitor)

    def _save_initial(self, sender, instance, **kwargs):
        if self.monitor in instance.get_deferred_fields():
            # Fix related to issue #241 to avoid recursive error on double monitor fields
            return
        setattr(instance, self.monitor_attname,
                self.get_monitored_value(instance))

    def pre_save(self, model_instance, add):
        value = now()
        previous = getattr(model_instance, self.monitor_attname, None)
        current = self.get_monitored_value(model_instance)
        if previous != current:
            if self.when is None or current in self.when:
                setattr(model_instance, self.attname, value)
                self._save_initial(model_instance.__class__, model_instance)
        return super().pre_save(model_instance, add)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['monitor'] = self.monitor
        if self.when is not None:
            kwargs['when'] = self.when
        return name, path, args, kwargs


SPLIT_MARKER = getattr(settings, 'SPLIT_MARKER', '<!-- split -->')

# the number of paragraphs after which to split if no marker
SPLIT_DEFAULT_PARAGRAPHS = getattr(settings, 'SPLIT_DEFAULT_PARAGRAPHS', 2)


def _excerpt_field_name(name):
    return '_%s_excerpt' % name


def get_excerpt(content):
    excerpt = []
    default_excerpt = []
    paras_seen = 0
    for line in content.splitlines():
        if not line.strip():
            paras_seen += 1
        if paras_seen < SPLIT_DEFAULT_PARAGRAPHS:
            default_excerpt.append(line)
        if line.strip() == SPLIT_MARKER:
            return '\n'.join(excerpt)
        excerpt.append(line)

    return '\n'.join(default_excerpt)


class SplitText:
    def __init__(self, instance, field_name, excerpt_field_name):
        # instead of storing actual values store a reference to the instance
        # along with field names, this makes assignment possible
        self.instance = instance
        self.field_name = field_name
        self.excerpt_field_name = excerpt_field_name

    # content is read/write
    @property
    def content(self):
        return self.instance.__dict__[self.field_name]

    @content.setter
    def content(self, val):
        setattr(self.instance, self.field_name, val)

    # excerpt is a read only property
    def _get_excerpt(self):
        return getattr(self.instance, self.excerpt_field_name)
    excerpt = property(_get_excerpt)

    # has_more is a boolean property
    def _get_has_more(self):
        return self.excerpt.strip() != self.content.strip()
    has_more = property(_get_has_more)

    def __str__(self):
        return self.content


class SplitDescriptor:
    def __init__(self, field):
        self.field = field
        self.excerpt_field_name = _excerpt_field_name(self.field.name)

    def __get__(self, instance, owner):
        if instance is None:
            raise AttributeError('Can only be accessed via an instance.')
        content = instance.__dict__[self.field.name]
        if content is None:
            return None
        return SplitText(instance, self.field.name, self.excerpt_field_name)

    def __set__(self, obj, value):
        if isinstance(value, SplitText):
            obj.__dict__[self.field.name] = value.content
            setattr(obj, self.excerpt_field_name, value.excerpt)
        else:
            obj.__dict__[self.field.name] = value


class SplitField(models.TextField):
    def __init__(self, *args, **kwargs):
        ''' for South FakeORM compatibility: the frozen version of a
        SplitField can't try to add an _excerpt field, because the
        _excerpt field itself is frozen as well. See introspection
        rules below.'''
        self.add_excerpt_field = not kwargs.pop('no_excerpt_field', False)
        super().__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        if self.add_excerpt_field and not cls._meta.abstract:
            excerpt_field = models.TextField(editable=False)
            cls.add_to_class(_excerpt_field_name(name), excerpt_field)
        super().contribute_to_class(cls, name)
        setattr(cls, self.name, SplitDescriptor(self))

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        excerpt = get_excerpt(value.content)
        setattr(model_instance, _excerpt_field_name(self.attname), excerpt)
        return value.content

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return value.content

    def get_prep_value(self, value):
        try:
            return value.content
        except AttributeError:
            return value

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['no_excerpt_field'] = True
        return name, path, args, kwargs


class UUIDField(models.UUIDField):
    """
    A field for storing universally unique identifiers. Use Python UUID class.
    """

    def __init__(self, primary_key=True, version=4, editable=False, *args, **kwargs):
        """
        Parameters
        ----------
        primary_key : bool
            If True, this field is the primary key for the model.
        version : int
            An integer that set default UUID version.
        editable : bool
            If False, the field will not be displayed in the admin or any other ModelForm,
            default is false.

        Raises
        ------
        ValidationError
            UUID version 2 is not supported.
        """

        if version == 2:
            raise ValidationError(
                'UUID version 2 is not supported.')

        if version < 1 or version > 5:
            raise ValidationError(
                'UUID version is not valid.')

        if version == 1:
            default = uuid.uuid1
        elif version == 3:
            default = uuid.uuid3
        elif version == 4:
            default = uuid.uuid4
        elif version == 5:
            default = uuid.uuid5

        kwargs.setdefault('primary_key', primary_key)
        kwargs.setdefault('editable', editable)
        kwargs.setdefault('default', default)
        super().__init__(*args, **kwargs)


class Choices:
    """
    A class to encapsulate handy functionality for lists of choices
    for a Django model field.

    Each argument to ``Choices`` is a choice, represented as either a
    string, a two-tuple, or a three-tuple.

    If a single string is provided, that string is used as the
    database representation of the choice as well as the
    human-readable presentation.

    If a two-tuple is provided, the first item is used as the database
    representation and the second the human-readable presentation.

    If a triple is provided, the first item is the database
    representation, the second a valid Python identifier that can be
    used as a readable label in code, and the third the human-readable
    presentation. This is most useful when the database representation
    must sacrifice readability for some reason: to achieve a specific
    ordering, to use an integer rather than a character field, etc.

    Regardless of what representation of each choice is originally
    given, when iterated over or indexed into, a ``Choices`` object
    behaves as the standard Django choices list of two-tuples.

    If the triple form is used, the Python identifier names can be
    accessed as attributes on the ``Choices`` object, returning the
    database representation. (If the single or two-tuple forms are
    used and the database representation happens to be a valid Python
    identifier, the database representation itself is available as an
    attribute on the ``Choices`` object, returning itself.)

    Option groups can also be used with ``Choices``; in that case each
    argument is a tuple consisting of the option group name and a list
    of options, where each option in the list is either a string, a
    two-tuple, or a triple as outlined above.

    """

    def __init__(self, *choices):
        # list of choices expanded to triples - can include optgroups
        self._triples = []
        # list of choices as (db, human-readable) - can include optgroups
        self._doubles = []
        # dictionary mapping db representation to human-readable
        self._display_map = {}
        # dictionary mapping Python identifier to db representation
        self._identifier_map = {}
        # set of db representations
        self._db_values = set()

        self._process(choices)

    def _store(self, triple, triple_collector, double_collector):
        self._identifier_map[triple[1]] = triple[0]
        self._display_map[triple[0]] = triple[2]
        self._db_values.add(triple[0])
        triple_collector.append(triple)
        double_collector.append((triple[0], triple[2]))

    def _process(self, choices, triple_collector=None, double_collector=None):
        if triple_collector is None:
            triple_collector = self._triples
        if double_collector is None:
            double_collector = self._doubles

        def store(c): return self._store(c, triple_collector, double_collector)

        for choice in choices:
            if isinstance(choice, (list, tuple)):
                if len(choice) == 3:
                    store(choice)
                elif len(choice) == 2:
                    if isinstance(choice[1], (list, tuple)):
                        # option group
                        group_name = choice[0]
                        subchoices = choice[1]
                        tc = []
                        triple_collector.append((group_name, tc))
                        dc = []
                        double_collector.append((group_name, dc))
                        self._process(subchoices, tc, dc)
                    else:
                        store((choice[0], choice[0], choice[1]))
                else:
                    raise ValueError(
                        "Choices can't take a list of length %s, only 2 or 3"
                        % len(choice)
                    )
            else:
                store((choice, choice, choice))

    def __len__(self):
        return len(self._doubles)

    def __iter__(self):
        return iter(self._doubles)

    def __reversed__(self):
        return reversed(self._doubles)

    def __getattr__(self, attname):
        try:
            return self._identifier_map[attname]
        except KeyError:
            raise AttributeError(attname)

    def __getitem__(self, key):
        return self._display_map[key]

    def __add__(self, other):
        if isinstance(other, self.__class__):
            other = other._triples
        else:
            other = list(other)
        return Choices(*(self._triples + other))

    def __radd__(self, other):
        # radd is never called for matching types, so we don't check here
        other = list(other)
        return Choices(*(other + self._triples))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._triples == other._triples
        return False

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join("%s" % repr(i) for i in self._triples)
        )

    def __contains__(self, item):
        return item in self._db_values

    def __deepcopy__(self, memo):
        return self.__class__(*copy.deepcopy(self._triples, memo))

    def subset(self, *new_identifiers):
        identifiers = set(self._identifier_map.keys())

        if not identifiers.issuperset(new_identifiers):
            raise ValueError(
                'The following identifiers are not present: %s' %
                identifiers.symmetric_difference(new_identifiers),
            )

        return self.__class__(*[
            choice for choice in self._triples
            if choice[1] in new_identifiers
        ])
