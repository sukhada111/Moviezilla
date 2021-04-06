from django.contrib import admin
from django.urls import path,include

from django.conf.urls.static import static
from django.conf import settings
from . import views
from register import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homepage,name='home'),
    path("register/", v.register, name="register"),
    path('', include("django.contrib.auth.urls")),
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

