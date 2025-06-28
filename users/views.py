from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm as AunticationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserRegistrationForm, UserPrifileEditForm, ProfilePicForm
from .tasks import send_email


class RegisterView(View):
    def get(self,request):
        form = UserRegistrationForm()
        context = {
            'conForm': form
        }
        return render(request, 'users/register.html', context)
    
    def post(self, request):
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
        else:
            context = {
                'conForm': form,
                'errors': form.errors
            }
            return render(request, 'users/register.html', context)
    
class LoginView(View):
    def get(self, request):
        login_form = AunticationForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'users/login.html', context)
    
    def post(self, request):
        login_form = AunticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('home')
        else:
            context = {
                'login_form': login_form,
                'errors': login_form.errors
            }
            return render(request, 'users/login.html', context)

class ProfileView(LoginRequiredMixin, View):
    def get(self,request):
        form = UserPrifileEditForm(instance=request.user)
        pic_form = ProfilePicForm(instance=request.user.profile)

        # test send mail
        send_email("test sub","test subedgvqiergvqeg",["piyeca7768@exitbit.com"])

        return render(request,'users/profile.html',{'user':request.user,'form':form,'pic_form':pic_form})

    def post(self,request):
        form = UserPrifileEditForm(data=request.POST,instance=request.user)
        pic_form = ProfilePicForm(data=request.POST,instance=request.user.profile,files=request.FILES)
        if form.is_valid() and pic_form.is_valid():
            user=form.save()
            profile_pic=pic_form.save(commit=False)
            if pic_form.cleaned_data['profile_picture'] is False:
                profile_pic.profile_picture = 'd_pic.jpg'
            profile_pic.user=user
            profile_pic.save()
        return redirect('users:profile')



    
class LogoutView(LoginRequiredMixin, View):
    def get(self,request):
        logout(request)
        return redirect('home')


