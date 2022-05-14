from django.urls import path, re_path
from . import views

urlpatterns = (
    path('home', views.home, name='home'),
    path('register', views.signup, name='register'),
    path('home/<int:id>', views.home, name='client'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout', views.CustomLoginOutView.as_view(), name='logout'),
    path('pay', views.pay_for_style, name='pay'),
    # re_path(r'^$', views.IndexFromView.as_view(), name='index'),
    path('timetable', views.timetable, name='timetable'),
    path('', views.index, name='index'),
    path('profile', views.profile, name='profile'),
    # re_path(r'^home/(?P<id>[0-9]*)/$', views.home, name='client'),
)
