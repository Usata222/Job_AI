from django.contrib import admin
from django.urls import include, path

from profiles.views import CountryListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('account.urls')),
    path('api/profile/', include('profiles.urls')),
    path('api/countries/', CountryListView.as_view(), name='countries'),
]