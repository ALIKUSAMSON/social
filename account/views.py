from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password,make_password
from .models import Profile
from django.contrib import messages
from django.conf import settings

# Create your views here.
def user_login(request):
	form = LoginForm()
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			lf = form.cleaned_data
			user = authenticate(username=lf['username'],password=lf['password'])
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponse('Authenticated successfully')
				else:
					return HttpResponse('Disabled account')
			else:
				return HttpResponse('invalid login')
		else:
			form = LoginForm()
	return render(request, 'account/login.html',{'form':form})


@login_required
def dashboard(request):
	prof = get_object_or_404(Profile, user=request.user.username)
	return render(request, 'account/dashboard.html',{'section':dashboard,'prof':prof})


#def register_done(request):
#	template_name = 'account/register_done.html'
#	context = locals()
#	return render(request, template_name, context)

def register(request):
	form  = UserRegistrationForm()
	
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			username = user_form.cleaned_data['username']
			email = user_form.cleaned_data['email']
			password = user_form.cleaned_data['password']
			password2 = user_form.cleaned_data['password2']
			check = User.objects.filter(username=username)
			if (password == password2):
				if check:
					return HttpResponse('no password')
				else:
					new_user = User(username=username,email=email, password=make_password(password,salt=None,hasher='default'))
					new_user.save()
					profile = Profile.objects.create(user=new_user)
				
					return render(request, 'account/register_done.html', {'new_user':new_user})
		else:
			form = UserRegistrationForm()
			return render(request,'account/register.html',{'form': form})

	return render(request,'account/register.html',{'form': form})

#@login_required
#def edit(request):
#	user_form = UserEditForm()
#
#	if request.method == 'POST':
#		user_form = ProfileEditForm(request.POST, instance=request.user)
#		profile_form = UserEditForm(request.POST, instance=request.user.profile,files=request.FILES)
#
#		if user_form.is_valid() and profile_form.is_valid():
#			user_form.save()
#			profile_form.save()
#			messages.success(request,'Profile updated successfully')
#			return redirect(reverse('dashboard'))
#		else:
#			messages.error(request,'Error updating your profile')
#	else:
#		user_form = UserEditForm(instance=request.user)
#		profile_form = ProfileEditForm(instance=request.user.profile)
#	return render(request,'account/edit.html',{'user_form':user_form,'profile_form':profile_form})




@login_required
def edit(request):
	user_form = UserEditForm()
	profile_form = ProfileEditForm()

	if request.method == 'POST':
		user_form = ProfileEditForm(request.POST or None,instance=request.user )
		profile_form = UserEditForm(request.POST or None, instance=request.user.profile, files=request.FILES)
		inst_user = User.objects.all().filter(username=request.user).values
		inst_prof = Profile.objects.all().filter(user=request.user.profile.user).values

		if user_form.is_valid() and profile_form.is_valid():
			user_form = ProfileEditForm(request.POST ,instance=request.user)
			profile_form = UserEditForm(request.POST, instance=request.user.profile, files=request.FILES)
			user_form.save()
			profile_form.save()
			messages.success(request,'Profile updated successfully')
			return redirect(reverse('dashboard'))
		else:
			messages.error(request,'Error updating your profile')
	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = ProfileEditForm(instance=request.user.profile)
	return render(request,'account/edit.html',{'user_form':user_form,'profile_form':profile_form})



def logout(request):
	logout(request)
	context = locals()
	return render(request,'registration/logged_on.html',context)

	