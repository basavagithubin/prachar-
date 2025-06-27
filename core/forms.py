from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from .models import Candidate, Comment, Volunteer


class CandidateForm(forms.ModelForm):
    registration_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-input',
            'type': 'date',
        }),
        initial=timezone.now().date
    )

    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-input',
            'type': 'date',
            'placeholder': 'YYYY-MM-DD',
        }),
        label='Date of Birth'
    )

    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-textarea',
            'placeholder': 'Address',
            'rows': 3,
        })
    )

    mother_tongue = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Mother Tongue',
        })
    )

    class Meta:
        model = Candidate
        fields = [
            'name',
            'phone',
            'email',
            'date_of_birth',
            'address',
            'mother_tongue',
            'assigned_volunteer',
            'attended',
            'followed_up',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email Address'}),
            'assigned_volunteer': forms.Select(attrs={'class': 'form-select'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Enter your comment...',
                'rows': 3
            })
        }


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ['name', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full rounded-md border-gray-300 shadow-sm focus:ring focus:ring-blue-300 focus:border-blue-500'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full rounded-md border-gray-300 shadow-sm focus:ring focus:ring-blue-300 focus:border-blue-500'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full rounded-md border-gray-300 shadow-sm focus:ring focus:ring-blue-300 focus:border-blue-500'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full rounded-md border-gray-300 shadow-sm focus:ring focus:ring-blue-300 focus:border-blue-500',
                'rows': 3
            }),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input',
        'placeholder': 'Password'
    }))

    
# # core/forms.py

# from django import forms
# from django.contrib.auth.forms import AuthenticationForm
# from .models import Candidate, Comment, Volunteer
# from django import forms
# from django.utils import timezone
# from .models import Candidate, Comment, Volunteer

# # core/forms.py

# from django import forms
# from django.contrib.auth.forms import AuthenticationForm
# from .models import Candidate, Comment, Volunteer
# from django.utils import timezone


# class CandidateForm(forms.ModelForm):
#     registration_date = forms.DateField(
#         required=False,
#         widget=forms.DateInput(attrs={
#             'class': 'form-input',
#             'type': 'date',
#         }),
#         initial=timezone.now().date
#     )

#     date_of_birth = forms.DateField(
#         required=False,
#         widget=forms.DateInput(attrs={
#             'class': 'form-input',
#             'type': 'date',
#             'placeholder': 'YYYY-MM-DD',
#         }),
#         label='Date of Birth'
#     )

#     address = forms.CharField(
#         required=False,
#         widget=forms.Textarea(attrs={
#             'class': 'form-textarea',
#             'placeholder': 'Address',
#             'rows': 3,
#         })
#     )

#     mother_tongue = forms.CharField(
#         required=False,
#         widget=forms.TextInput(attrs={
#             'class': 'form-input',
#             'placeholder': 'Mother Tongue',
#         })
#     )

#     class Meta:
#         model = Candidate
#         fields = ['name', 'phone', 'email', 'date_of_birth', 'address', 'mother_tongue', 'assigned_volunteer','attended', 'followed_up]
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name'}),
#             'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number'}),
#             'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email Address'}),
#             'assigned_volunteer': forms.Select(attrs={'class': 'form-select'}),
#         }



# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['content']
#         widgets = {
#             'content': forms.Textarea(attrs={
#                 'class': 'form-textarea',
#                 'placeholder': 'Enter your comment...',
#                 'rows': 3
#             })
#         }



# class VolunteerForm(forms.ModelForm):
#     class Meta:
#         model = Volunteer
#         fields = ['name', 'email', 'phone','address']
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:ring focus:ring-blue-300 focus:border-blue-500'}),
#             'email': forms.EmailInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:ring focus:ring-blue-300 focus:border-blue-500'}),
#             'phone': forms.TextInput(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:ring focus:ring-blue-300 focus:border-blue-500'}),
#             'address': forms.Textarea(attrs={'class': 'w-full rounded-md border-gray-300 shadow-sm focus:ring focus:ring-blue-300 focus:border-blue-500', 'rows': 3}),
#         }


# class LoginForm(AuthenticationForm):
#     username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'}))

# from django import forms
# from django.contrib.auth.forms import AuthenticationForm
# from .models import Candidate, Comment, Volunteer

# class CandidateForm(forms.ModelForm):
#     class Meta:
#         model = Candidate
#         fields = ['name', 'phone', 'email', 'volunteer']
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name'}),
#             'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number'}),
#             'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email Address'}),
#             'volunteer': forms.Select(attrs={'class': 'form-select'})
#         }

# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['content']
#         widgets = {
#             'content': forms.Textarea(attrs={
#                 'class': 'form-textarea',
#                 'placeholder': 'Enter your comment...',
#                 'rows': 3
#             })
#         }

# class VolunteerForm(forms.ModelForm):
#     class Meta:
#         model = Volunteer
#         fields = ['name', 'email', 'phone']
#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Name'}),
#             'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}),
#             'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone'}),
#         }

# class LoginForm(AuthenticationForm):
#     username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'}))
