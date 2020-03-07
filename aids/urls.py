from django.urls import path, re_path
from . import views as v


app_name = 'aids'

urlpatterns = [
    path('', v.ClassRoomListView.as_view(), name="class"),
    path('<batch>/<classroom>/', v.ClassRoomListView.as_view(), name="classes"),
    path('classroom/', v.ClassRoomCreateView.as_view(), name="classroom"),
    path('classroom/<pk>/', v.ClassRoomCreateView.as_view(), name="classroom-details"),
    path('schoolinfo/', v.SchoolCreateView.as_view(), name="schoolinfo"),

    # path('<pk>/',  views.StudentDetailView.as_view(), name="details"),
    # path('<int:pk>/delete/',  StudentDeleteView.as_view(), name="delete"),
    # path('<pk>/edit/',  views.StudentUpdateView.as_view(), name="update"),

]
