from django.urls import path
from .views import signup_view, login_view, dashboard_view, activate ,sign_out, admin_dashboard, assign_role, create_group, group_list, edit_group,delete_group,delete_user,user_list_view
app_name = 'users'
urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
     path('sign-out/', sign_out, name='logout'), 
    path('activate/<int:uid>/<str:token>/', activate, name='activate'),
    
    
    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/<int:user_id>/assign-role/', assign_role, name='assign-role'),
    path('admin/create-group/', create_group, name='create-group'),
    path('admin/group-list/', group_list, name='group-list'),
    path('admin/group/<int:pk>/edit/', edit_group, name='edit-group'),
    path('admin/group/<int:pk>/delete/', delete_group, name='delete-group'),
    path('admin/user/<int:user_id>/delete/', delete_user, name='delete-user'),
    path('admin/user-list/', user_list_view, name='user-list'),
    
]

    # Example: path('', views.home, name='home'),