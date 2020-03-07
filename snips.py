from django.db import models
class UserProfile(models.Model):
    name    = models.CharField(max_length=50, verbose_name="Name")
    login   = models.CharField(max_length=25, verbose_name="Login")
    password = models.CharField(max_length=100, verbose_name="Password")
    phone   = models.CharField(max_length=20, verbose_name="Phone number", null=True, default=None, blank=True)
    born_date = models.DateField(verbose_name="Born date" , null=True, default=None, blank=True)
    last_connection = models.DateTimeField(verbose_name="Date of last connection" , null=True, default=None, blank=True)
    email   = models.EmailField(verbose_name="Email")
    years_seniority = models.IntegerField(verbose_name="Seniority", default=0)
    date_created = models.DateField(verbose_name="Date of Birthday", auto_now_add=True)


from django.conf import settings
from django.db import models

# topics.models.py
class TopicManager(models.Manager):
    def create_or_new(self, title):
        title = title.strip()
        qs = self.get_queryset().filter(title__iexact=title)
        if qs.exists():
            return qs.first(), False
        return Topic.objects.create(title=title), True
    
    def comma_to_qs(self, topics_str):
        final_ids = []
        for topic in topics_str.split(','):
            obj, created = self.create_or_new(topic)
            final_ids.append(obj.id)
        qs = self.get_queryset().filter(id__in=final_ids).distinct()
        return qs
        
    
class Topic(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True)
    
    objects = TopicManager()

# posts.models.py
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    slug = models.SlugField()
    body = models.TextField()
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    topics = models.ManyToManyField(Topic, blank=True)

# posts.forms.py
from django import forms
from django.utils import timezone

class PostForm(forms.ModelForm):
    topic_str = forms.CharField(label='Topics', widget=forms.Textarea, required=False)
    class Meta:
        model = Post
        fields = [
            "user",
            "title",
            "media",
            "slug",
            "body",
            "topic_str",
            "publish_date"
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")
        if instance:
            self.fields['topic_str'].initial = ", ".join(x.title for x in instance.topics.all())
    
    def save(self, commit=True, *args, **kwargs):
        instance = super().save(commit=False, *args, **kwargs)
        topics_str = self.cleaned_data.get('topics_str')
        if commit:
            topic_qs = Topic.objects.comma_to_qs(topics_str)
            if not instance.id:
                '''
                This is a new instance.
                '''
                instance.save()
            instance.topics.clear()
            instance.topics.add(*topic_qs)
            instance.save()
        return instance

# posts.admin.py
from django.contrib import admin
from django.db.models import Count
from django.utils.safestring import mark_safe

from topics.models import Topic

from .forms import PostForm

class PostAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']
    list_display = ["title", "publish_date", "topic_list"]
    form = PostForm
    
    def topic_list(self, obj):
        topic_list = ", ".join([f"<a href='/blog/post/?topics__title={x.title}'>{x.title}</a>" for x in obj.topics.all()])
        return mark_safe(topic_list)
    
    def save_model(self, request, obj, form, change):
        topic_str = form.cleaned_data.get('topic_str')
        topic_qs = Topic.objects.comma_to_qs(topic_str)
        if not obj.id:
            obj.save()
        obj.topics.clear()
        obj.topics.add(*topic_qs)
        obj.save()

admin.site.register(Post, PostAdmin)


#################################################################################

from django.conf import settings
from django.db import models

# files.models.py
class FileItem(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    label = models.CharField(max_length=120, blank=true, null=True)
    file = models.FileField(upload_to='files/')

# posts.models.py
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    media = models.ForeignKey(FileItem, blank=True, null=True, on_delete=models.SET_NULL)
    slug = models.SlugField()
    body = models.TextField()
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

'''
The above models imply that each post has 1 file item (via the media field). So what we want to do is find all the FileItem instances that are unused. We can do that with the following:

unused_files = FileItem.objects.filter(post__isnull=True)
In forms, it's pretty simple to limit the choice. All you need to do is override the __init__ method:
'''

# post.forms.py
from django import forms
from django.utils import timezone

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "user",
            "title",
            "media",
            "slug",
            "body",
            "publish_date"
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        unused_files = FileItem.objects.filter(post__isnull=True)
        instance = kwargs.get("instance")
        if instance:
            if instance.media:
                # if we're using this form to edit a post instance, we'll do this
                current_file = File.objects.filter(pk=instance.media.pk) 
                unused_files = ( unused_files | current_file ) # combine querysets
        self.fields['media'].queryset  = unused_files
        # pre-fill the timezone for good measure
        self.fields['publish_date'].initial = timezone.now()
# Of course, if you want this to work within the Django admin, you'll also want to do this:


# post.admin.py
from django.contrib import admin

from .forms import PostForm

class PostModelAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']
    list_display = ["title", "publish_date"]
    form = PostForm
'''
I'm going to assume you're not a beginner for this one. If you are, check out this series and come back to this post.

The problem we're going to solve is a simple one: limit foreign key choices based on any arbitrary lookup like: - request.user - or company_id=1 - or publish_date__gte=timezone.now() - or a related file object is not used.

Let's say you have a blog for your entire team. Each person What I'm saying is how do we take a model like:
'''

from django.conf import settings
from django.db import models

# files.models.py
class FileItem(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    label = models.CharField(max_length=120, blank=true, null=True)
    file = models.FileField(upload_to='files/')

# posts.models.py
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    media = models.ForeignKey(FileItem, blank=True, null=True, on_delete=models.SET_NULL)
    slug = models.SlugField()
    body = models.TextField()
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

# The above models imply that each post has 1 file item (via the media field). So what we want to do is find all the FileItem instances that are unused. We can do that with the following:


unused_files = FileItem.objects.filter(post__isnull=True)
# In forms, it's pretty simple to limit the choice. All you need to do is override the __init__ method:


# post.forms.py
from django import forms
from django.utils import timezone

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "user",
            "title",
            "media",
            "slug",
            "body",
            "publish_date"
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        unused_files = FileItem.objects.filter(post__isnull=True)
        instance = kwargs.get("instance")
        if instance:
            if instance.media:
                # if we're using this form to edit a post instance, we'll do this
                current_file = File.objects.filter(pk=instance.media.pk) 
                unused_files = ( unused_files | current_file ) # combine querysets
        self.fields['media'].queryset  = unused_files
        # pre-fill the timezone for good measure
        self.fields['publish_date'].initial = timezone.now()
Of course, if you want this to work within the Django admin, you'll also want to do this:


# post.admin.py
from django.contrib import admin

from .forms import PostForm

class PostModelAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']
    list_display = ["title", "publish_date"]
    form = PostForm

    ############################################################################

'''
Create a new app

This will hold your custom user model. I'll call it accounts

python manage.py startapp accounts
2. Create the Custom User Model in models.py

You can use the Django example, or follow with ours below. We will simplify the process here.

'''
# accounts.models.py

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)



class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    # notice the absence of a "Password field", that's built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

'''
So what's the USERNAME_FIELD exactly? Well that's how Django is going to recognize this user. It replaces the built-in username field for whatever you designate. In this case, we said it was the email. So that's what we'll use.

3. Create the User model manager

Django has built-in methods for the User Manager. We have to customize them in order to make our custom user model work correctly.

'''
# accounts.models.py

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

# hook in the New Manager to our Model
class User(AbstractBaseUser): # from step 2
    ...
    objects = UserManager()

'''
4. Update settings module (aka settings.py):

First, run:


python manage.py makemigrations
python manage.py migrate
Now open up settings.py:


AUTH_USER_MODEL = 'accounts.User'
Run again:


python manage.py makemigrations
python manage.py migrate
Create a new super user:


python manage.py createsuperuser
5. Create the Forms for Register, Change, and Admin-Level Create

'''

# accounts.forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

# Update the Django Admin


# accounts.admin.py

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin')
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)


# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)

###########################################################################
# searchl
# blog.models
class Post(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title           = models.CharField(max_length=120)
    description     = models.TextField(null=True, blank=True)
    slug            = models.SlugField(blank=True, unique=True)
    publish_date    = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    
# courses.models
class Lesson(models.Model):
    title           = models.CharField(max_length=120)
    description     = models.TextField(null=True, blank=True)
    slug            = models.SlugField(blank=True, unique=True)
    featured        = models.BooleanField(default=False)
    publish_date    = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)

    
# profiles.models
class Profile(models.Model):
    user            = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title           = models.CharField(max_length=120)
    description     = models.TextField(null=True, blank=True)
    slug            = models.SlugField(blank=True, unique=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
# Simple Search (aka Lookup)


>>> from django.utils import timezone
>>> from blog.models import Post
>>> qs = Post.objects.filter(publish_date__lte=timezone.now(), title__icontains="Django")

>>> from django.utils import timezone
>>> from courses.models import Lesson
>>> qs = Lesson.objects.filter(publish_date__lte=timezone.now(), featured=True)

>>> from profiles.models import Profile
>>> obj = Profile.objects.get(user__id=1) 
# Advancing the Query Lookup

# Here's a few more queries that are a little more robut because of Q Lookups. You might want to learn more about lookups in the Products Component or specifically in Understanding Lookups.


>>> from django.db.models import Q
>>> from django.utils import timezone
>>> from blog.models import Post
>>> query = "Django"


>>> or_lookup = (Q(title__icontains=query) | Q(description__icontains=query))
>>> print(or_lookup)
(OR: ('title__icontains', 'Django'), ('description__icontains', 'Django'))

>>> and_lookup = (Q(title__icontains=query) & Q(description__icontains=query))
>>> print(and_lookup)
(<Q: (AND: ('title__icontains', 'Django'))>, <Q: (AND: ('description__icontains', 'Django'))>)


>>> qs_and = Post.objects.filter(publish_date__lte=timezone.now()).filter(and_lookup)
>>> print(qs_and)
>>> qs_or = Post.objects.filter(publish_date__lte=timezone.now()).filter(or_lookup)
>>> print(qs_or)
# Now that we see how easy Q Lookups are, we should implement a method to our model manager to handle any given query. Below is an example on the Post model, I'll leave it to you to implement your own.

# Update Model Manager to include a Search Method


# blog.models
from django.db.models import Q

class PostManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) | 
                         Q(description__icontains=query)|
                         Q(slug__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs

    
class Post(models.Model):
    user            = models.ForeignKey(settings.AUTH_USER_MODEL)
    title           = models.CharField(max_length=120)
    description     = models.TextField(null=True, blank=True)
    slug            = models.SlugField(blank=True, unique=True)
    publish_date    = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    
    objects         = PostManager()

# Now, let's implement this concept into a view.
# Create the search view


# search.views.py
from itertools import chain
from django.views.generic import ListView

from blog.models import Post
from courses.models import Lesson
from profiles.models import Profile

class SearchView(ListView):
    template_name = 'search/view.html'
    paginate_by = 20
    count = 0
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        
        if query is not None:
            blog_results        = Post.objects.search(query)
            lesson_results      = Lesson.objects.search(query)
            profile_results     = Profile.objects.search(query)
            
            # combine querysets 
            queryset_chain = chain(
                    blog_results,
                    lesson_results,
                    profile_results
            )        
            qs = sorted(queryset_chain, 
                        key=lambda instance: instance.pk, 
                        reverse=True)
            self.count = len(qs) # since qs is actually a list
            return qs
        return Post.objects.none() # just an empty queryset as default
Create a new template tag to get the class name


# search.templatetags.class_name.py
from django import template

register = template.Library()

@register.filter()
def class_name(value):
    return value.__class__.__name__
Create the view template

search/view.html


{% extends "base.html" %}
{% load class_name %}
{% block content %}

<div class='row title-row my-5'>
    <div class='col-12 py-0'>
        <h3 class='my-0 py-0'>{{ count }} results for <b>{{ query }}</b></h3>
    </div>
</div>
        
        
{% for object in object_list %}
    {% with object|class_name as klass %}
      {% if klass == 'Post' %}
           <div class='row'>
             <div class='col-12'>
                Blog post: <a href='{{ object.get_absolute_url }}'>{{ object.title }}</a>
            </div>
          </div>

      {% elif klass == 'Lesson' %}
           <div class='row'>
             <div class='col-12'>
                Lesson Item: <a href='{{ object.get_absolute_url }}'>{{ object.title }}</a>
              </div>
            </div>
        
      {% elif klass == 'Profile' %}
           <div class='row'>
                <div class='col-12'>
                   Lesson Item: <a href='{{ object.get_absolute_url }}'>{{ object.title }}</a>
                </div>
            </div>
      {% else %}
           <div class='row'>
             <div class='col-12 col-lg-8 offset-lg-4'>
                <a href='{{ object.get_absolute_url }}'>{{ object }} | {{ object|class_name }}</a>
            </div>
           </div>
        {% endif %}
        
    {% endwith %}
    
{% empty %}
<div class='row'>
    <div class='col-12 col-md-6 mx-auto my-5 py-5'>
    <form method='GET' class='' action='.'>
    
        <div class="input-group form-group-no-border mx-auto" style="margin-bottom: 0px; font-size: 32px;">
            <span class="input-group-addon cfe-nav" style='color:#000'>
                <i class="fa fa-search" aria-hidden="true"></i>
            </span>
            <input type="text" name="q" data-toggle="popover" data-placement="bottom" data-content="Press enter to search" class="form-control cfe-nav mt-0 py-3" placeholder="Search..." value="" style="" data-original-title="" title="" autofocus="autofocus">
        </div>

    </form>

    </div>
</div>
{% endfor %}
{% endblock content %}