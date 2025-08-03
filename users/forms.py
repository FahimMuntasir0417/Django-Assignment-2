from django import forms
from django.contrib.auth.models import User, Permission, Group

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from users.models import CustomUser
from django.contrib.auth import get_user_model
User = get_user_model()

class AssignRoleForm(forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role"
    )
    
class CreateGroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Assign Permission'
    )
    
    class Meta:
        model = Group
        fields = ['name', 'permissions']
        
class CustomPasswordChangeForm(PasswordChangeForm):
    pass


class CustomPasswordResetForm(PasswordResetForm):
    pass


class CustomPasswordResetConfirmForm(SetPasswordForm):
    pass


# class EditProfileForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['email', 'first_name', 'last_name', 'bio', 'profile_image']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'bio', 'profile_image']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'Enter your email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'Last Name'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'rows': 4,
                'placeholder': 'Tell us about yourself'
            }),
            'profile_image': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'
            }),
        }