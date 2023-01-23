from django.contrib import admin
from django.urls import path
from . import views

app_name = "magazine"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('login/',views.login,name="login"),
    path('view_magazine/',views.view_magazine,name="view_magazine")
]