from django import forms
from django.contrib.auth.models import User
from django.core.mail import send_mail

from users.models import Profile


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,required=True)

    class Meta:
        model = User  
        fields = ['username', 'email', 'password']

    def save(self, commit = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

        # send mail
        send_mail(subject="Goodreads ga hush kelibsiz",
                  message="Bu veb-sayt orqali o'zizga yoqgan kitoblarni topishiz yoki qolganlarga tavsiya berishiz mumkin!",
                  from_email="jaloliddin6003@gmail.com",
                  recipient_list=[]
                  )


        return user




class UserPrifileEditForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'required':False}))
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ProfilePicForm(forms.ModelForm):
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'id':"pic_form_input"}))
    class Meta:
        model = Profile
        fields = ['profile_picture']
