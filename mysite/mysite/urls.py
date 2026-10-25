from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('account.urls')),
    path('api/profile/', include('profiles.urls')),
]




# h;wuicbhiauhc[oiajc[owjpwojpor]]