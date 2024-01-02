from django.urls import path
from Frontend import views

urlpatterns = [

    path('', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('save_register/', views.save_register, name="save_register"),
    path('user_login/', views.user_login, name="user_login"),
    path('user_logout/', views.user_logout, name="user_logout"),

    path('home/', views.home, name="home"),
    path('search', views.Search, name='Search'),
    path('timeline/', views.timeline, name="timeline"),
    path('post_to_timeline/', views.post_to_timeline, name="post_to_timeline"),
    path('like_post', views.like_post, name="like_post"),

    path('my_profile/', views.my_profile, name="my_profile"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('update_profile/<int:dataid>/', views.update_profile, name="update_profile"),
    path('change_password/', views.change_password, name="change_password"),
    path('update_password/<int:userid>/', views.update_password, name="update_password"),

    path('remove_post/<int:dataid>/', views.remove_post, name="remove_post"),

    path('userprofile/<int:dataid>/', views.userprofile, name="userprofile"),

    path('follow', views.follow, name='follow'),

    path('view_post/<int:dataid>/', views.view_post, name='view_post'),
    path('comment', views.comment, name="comment"),
    path('delete_comment', views.delete_comment, name='delete_comment'),

    path('disabled/', views.disabled, name="disabled"),
    path('report', views.report, name="report"),
    path('help_center/', views.help_center, name="help_center"),
    path('help_center_mail', views.help_center_mail, name="help_center_mail"),


]
