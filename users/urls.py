from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView, LoginView 
from .views import (
    signup_view, login_view, dashboard_view, activate, sign_out, admin_dashboard,
    assign_role, create_group, group_list, edit_group, delete_group,
    delete_user, user_list_view, ProfileView, UserLogoutView, ChangePassword
)
from .views import (
    # CustomPasswordChangeView,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    CustomLoginView,
    ChangePassword,
)
from .views import EditProfileView



app_name = 'users'

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    # path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('sign-out/', sign_out, name='sign-out'),

    path('activate/<int:uid>/<str:token>/', activate, name='activate'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('password-change/', ChangePassword.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'), name='password_change_done'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/',
         CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('admin/dashboard/', admin_dashboard, name='admin-dashboard'),
    path('admin/<int:user_id>/assign-role/', assign_role, name='assign-role'),
    path('admin/create-group/', create_group, name='create-group'),
    path('admin/group/<int:pk>/edit/', edit_group, name='edit-group'),
    path('admin/group/<int:pk>/delete/', delete_group, name='delete-group'),
    path('admin/user/<int:user_id>/delete/', delete_user, name='delete-user'),
    path('admin/user-list/', user_list_view, name='group-list'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile')
]
