
from django.urls import path
from django.urls import include
from . import views


urlpatterns = [
    
    path('', views.index, name='index'),
    path('signup/', views.signup,  name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('like', views.like_post, name='like_post'),
    path('profile/<str:pk>', views.profile_usr, name='profile_usr'),
    path('follow', views.follower_count, name='follow'),
    path('search', views.search, name='search'),
    path('setting', views.setting, name='setting'),
    path('upload', views.upload_post, name='upload_post'),


]