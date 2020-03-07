from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path, re_path
from django.views.generic import TemplateView

# from . import views as inviews

# from menus.views import HomeView, AllUserRecentItemListView
# from profiles.views import ProfileFollowToggle, RegisterView, activate_user_view
# from users import views as user_view


urlpatterns = [
    # path("staff/", include('staff.urls', namespace='staff')),
    path('student/', include('students.urls', namespace='student')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('aids/', include('aids.urls', namespace='aids')),

    re_path(r'^$', TemplateView.as_view(
        template_name='index.html'), name='home'),
    re_path(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    re_path(r'^contact/$',
            TemplateView.as_view(template_name='contact.html'), name='contact'),
    re_path(r'^faq/$', TemplateView.as_view(template_name='faq.html'), name='faq'),

    re_path(r'^profile/$',
            TemplateView.as_view(template_name='profile.html'), name='profile'),


    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),


    # static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# handler404 = 'inviews.page_not_found'
# handler500 = 'inviews.error'
# handler403 = 'inviews.permission_denied'
# handler400 = 'inviews.bad_request'
