from django import forms
from user.models import UserInfo


class RegisterForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = [
            'Name',
            'Class',
            'Father_Name',
            'Mother_Name',
            'Phone_no',
            'email',
            'password',
            'Profile_pic',
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Phone_no'].required = True
        self.fields['password'].required = True
        self.fields['Profile_pic'].required = False
        self.fields['Profile_pic'].widget.attrs.update({'accept': 'image/*'})

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip()
        # Store blank email as NULL to avoid unique conflicts on empty string.
        return email or None
    

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = [
            'Name',
            'Class',
            'Father_Name',
            'Mother_Name',
            'Phone_no',
            'email',
            'Profile_pic',
        ]


class LoginForm(forms.Form):
    Phone_no = forms.CharField(max_length=10, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean_Phone_no(self):
        return (self.cleaned_data.get('Phone_no') or '').strip()
