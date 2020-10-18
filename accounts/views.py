from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact

def register(reqest):
    if reqest.method == 'POST':
        # Register user

        first_name = reqest.POST['first_name']
        last_name = reqest.POST['last_name']
        username = reqest.POST['username']
        email = reqest.POST['email']
        password = reqest.POST['password']
        password2 = reqest.POST['password2']

        # Check if passwords match

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(reqest, 'That username is taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(reqest, 'That email is being used')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,
                                                password=password,
                                                email=email,
                                                first_name=first_name,
                                                last_name=last_name)
                # # Login after register
                # auth.login(reqest, user)
                # messages.success(reqest, 'You are now logged in')
                # return redirect('index')
                user.save()
                messages.success(reqest, 'You are now registered and log in')
                return redirect('login')

        else:
            messages.error(reqest, 'Passwords do not match')
            return redirect('register')


        #messages.error(reqest, 'Testing error message')
        #return redirect('register')

    return render(reqest, 'accounts/register.html')

def login(reqest):
    if reqest.method == 'POST':
        username = reqest.POST['username']
        password = reqest.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(reqest, user)
            messages.success(reqest, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(reqest, 'Invalid credentials')
            redirect('login')

    return render(reqest, 'accounts/login.html')

def logout(reqest):
    if reqest.method == 'POST':
        auth.logout(reqest)
        messages.success(reqest, 'You are now logged out')
        return redirect('index')

def dashboard(reqest):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=reqest.user.id)

    context = {
        'contacts': user_contacts
    }
    return render(reqest, 'accounts/dashboard.html', context)