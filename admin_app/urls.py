from django.urls import path
from admin_app import views

urlpatterns = [
    path('index/', views.index, name="index"),
    path('', views.admin_login, name="admin_login"),
    path('adminlogin/', views.adminlogin, name="adminlogin"),
    path('admin_logout/', views.admin_logout, name="admin_logout"),

    path('user_data/', views.user_data, name="user_data"),
    path('remove_user/<int:dataid>/', views.remove_user, name="remove_user"),
    path('post_data/', views.post_data, name="post_data"),
    path('delete_post/<int:post_id>/', views.delete_post, name="delete_post"),

    path('user_profile/<int:dataid>/', views.user_profile, name="user_profile"),
    path('view_each_post/<int:dataid>/', views.view_each_post, name="view_each_post"),
    path('account_status', views.account_status, name="account_status"),
    path('report_mail/', views.report_mail, name="report_mail"),
    path('report_detail/<int:dataid>/', views.report_detail, name="report_detail"),
    path('report_review/', views.report_review, name="report_review"),
    path('help_mail/', views.help_mail, name="help_mail"),
    path('help_mail_detail/<int:dataid>/', views.help_mail_detail, name="help_mail_detail"),
    path('help_mail_review', views.help_mail_review, name="help_mail_review"),

]