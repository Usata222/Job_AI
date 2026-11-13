from django.urls import path

from .views import ProfileView, ResumeView

urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('resume/', ResumeView.as_view(), name='resume'),
]