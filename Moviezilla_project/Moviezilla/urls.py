from django.contrib import admin
from django.urls import path,include

from django.conf.urls.static import static
from django.conf import settings
from home import views
from register import views as v
from recommend import views as vr
from userprofile import views as vu

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homepage,name='home'),

    path("signup/", v.signupuser, name='signupuser'),
    path("selectgenre/", v.selectgenre, name='selectgenre'),

    # path('', include("django.contrib.auth.urls")),
    path('logout/', v.logoutuser,name='logoutuser'),
    path('login/', v.loginuser,name='loginuser'),
    path('dashboard/', vr.dashb,name='dashb'),
    path('userprofile/', vu.userprofile,name='userprofile'),
    path('aboutUs/',views.aboutUs,name='aboutUs'),
    path('wishlist/', vr.wishlist,name='wishlist'),


    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

