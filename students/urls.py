from django.urls import path, re_path
from .views import StudentListView, StudentCreateView, StudentDetailView, StudentUpdateView


app_name = 'students'


urlpatterns = [
    path('', StudentListView.as_view(), name="list"),
    path('admit/', StudentCreateView.as_view(), name="new"),
    path('<int:pk>/', StudentDetailView.as_view(), name="details"),
    path('<int:pk>/edit/', StudentUpdateView.as_view(), name="update"),
]
