from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required, user_passes_test
from users.forms import AssignRoleForm, CreateGroupForm ,CustomPasswordResetForm, CustomPasswordResetConfirmForm ,CustomPasswordChangeForm , EditProfileForm
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import TemplateView , UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView ,LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model



User = get_user_model()

class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect('users:profile')


def is_admin(user):
    return user.groups.filter(name='Admin').exists()



def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('users:signup')

        try:
            validate_password(password1)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return redirect('users:signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('users:signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return redirect('users:signup')

       
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            is_active=False  # Ensure is_active is False during creation
        )

        messages.success(request, "Account created! Check your email to activate your account.")
        return redirect('users:login')

    return render(request, 'users/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect('users:dashboard')
            else:
                messages.error(request, "Account not activated. Please check your email.")
                return redirect('users:login')
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('users:login')

    return render(request, 'users/login.html')

def activate(request, uid, token):
    user = get_object_or_404(User, pk=uid)
    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated! You can now log in.")
        return redirect('users:login')
    else:
        messages.error(request, "Invalid or expired activation link.")
        return redirect('users:signup')
    
@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('users:login')

@user_passes_test(is_admin)
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()

    print(users)

    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'
    return render(request, 'admin/dashboard.html', {"users": users})

@user_passes_test(is_admin)
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()  # Remove old roles
            user.groups.add(role)
            messages.success(request, f"User {
                             user.username} has been assigned to the {role.name} role")
            return redirect('users:admin-dashboard')

    return render(request, 'admin/assign_role.html', {"form": form})


@user_passes_test(is_admin)
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            return redirect('users:group-list')
            messages.success(request, f"Group {
                             group.name} has been created successfully")
            return redirect('admin/create-group')

    return render(request, 'admin/create_group.html', {'form': form})

@user_passes_test(is_admin)
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})


def dashboard_view(request):
    return render(request, 'users/dashboard.html')


@user_passes_test(is_admin)
def edit_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        form = CreateGroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, 'Group updated successfully.')
            return redirect('users:group-list')
    else:
        form = CreateGroupForm(instance=group)
    return render(request, 'admin/edit_group.html', {'form': form, 'group': group})


@user_passes_test(is_admin)
def delete_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    group.delete()
    return redirect('users:group-list')


@user_passes_test(is_admin)
def delete_user(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        if user_to_delete == request.user:
            messages.error(request, "You cannot delete your own account.")
        else:
            user_to_delete.delete()
            messages.success(request, f"User {user_to_delete.username} deleted successfully.")
        return redirect('users:admin-dashboard')
    return redirect('users:admin-dashboard')


@user_passes_test(is_admin)
def user_list_view(request):
    users = User.objects.all()
    return render(request, 'admin/user_list.html', {'users': users})

class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['username'] = user.username
        context['email'] = user.email
        context['name'] = user.get_full_name()

        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        return context
    
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('users:login')
    
    
    
# users/views.py


# class CustomLoginView(LoginView):
#     form_class = LoginForm

#     def get_success_url(self):
#         next_url = self.request.GET.get('next')
#         return next_url if next_url else super().get_success_url()
class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'accounts/reset_password.html'
    success_url = reverse_lazy('users:login')
    html_email_template_name = 'accounts/reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        print(context)
        return context

    def form_valid(self, form):
        messages.success(
            self.request, 'A Reset email sent. Please check your email')
        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'accounts/reset_password.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        messages.success(
            self.request, 'Password reset successfully')
        return super().form_valid(form)


class ChangePassword(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('users:login')