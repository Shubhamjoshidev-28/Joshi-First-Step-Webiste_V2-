from django.shortcuts import render , redirect
from user.forms import RegisterForm , LoginForm , ProfileForm
from django.contrib import messages
from django.contrib.messages import get_messages
from user.models import UserInfo 

def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful')
            return redirect('home')
         

        else:
            messages.error(request, 'Please correct the errors below')

    else:
        form = RegisterForm()

    return render(request, 'Register.html', {'form': form})

def login(request):
    # Clear old queued messages so login page only shows current feedback.
    list(get_messages(request))

    if request.session.get('user_id'):
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            phone_no = form.cleaned_data['Phone_no']
            password = form.cleaned_data['password']

            user = UserInfo.objects.filter(Phone_no=phone_no, password=password).first()

            if user:
                request.session['user_id'] = user.id
                request.session['user_name'] = user.Name
                if user.Profile_pic:
                    request.session['user_profile_pic'] = user.Profile_pic.url
                else:
                    request.session.pop('user_profile_pic', None)
                user.logged_in = True
                user.save(update_fields=['logged_in'])
                messages.success(request, 'Logged in successfully')
                return redirect('home')

            messages.error(request, 'Invalid phone number or password')
        else:
            messages.error(request, 'Please enter a valid phone number and password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout(request):
    request.session.flush()
    messages.success(request, "Logged out successfully")
    return redirect('login')   


def profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Please login first')
        return redirect('login')

    userinfo = UserInfo.objects.filter(id=user_id).first()
    if not userinfo:
        request.session.flush()
        messages.error(request, 'Session expired. Please login again')
        return redirect('login')

    return render(request, 'profile.html', {'userinfo': userinfo})


def edit_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Please login first')
        return redirect('login')

    userinfo = UserInfo.objects.filter(id=user_id).first()
    if not userinfo:
        request.session.flush()
        messages.error(request, 'Session expired. Please login again')
        return redirect('login')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=userinfo)
        if form.is_valid():
            updated_user = form.save()
            request.session['user_name'] = updated_user.Name
            if updated_user.Profile_pic:
                request.session['user_profile_pic'] = updated_user.Profile_pic.url
            else:
                request.session.pop('user_profile_pic', None)
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        form = ProfileForm(instance=userinfo)

    return render(request, 'edit_profile.html', {'form': form, 'userinfo': userinfo})



        
