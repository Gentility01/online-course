from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, InstructorRegistrationForm, LearnerRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib import messages
from .models import Instructor
# Create your views here.

def register_instructor(request):
    page = "instructor"
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        instructor_form = InstructorRegistrationForm(request.POST)
        if user_form.is_valid() and instructor_form.is_valid():
            # save your data  
            user = user_form.save()

            # Save instructor data linked to the user
            try:
                # attempt to create new instructor instance
                instructor = instructor_form.save(commit=False)
                instructor.user = user
                instructor.save()
            except IntegrityError:
                # Handle the case where an Instructor already exists for the user
                # You might want to update the existing instance or handle it differently
                instructor = Instructor.objects.get(user=user)
                # Update the existing instance with the new data
                instructor.full_time = instructor_form.cleaned_data['full_time']
                instructor.total_learners = instructor_form.cleaned_data['total_learners']
                instructor.save()

            # Log in the user
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect("home_page")
    else:
        user_form = UserRegistrationForm()
        instructor_form = InstructorRegistrationForm()

    context = {
        "page":page,
        "user_form":user_form,
        "instructor_form":instructor_form
    }

    return render(request, "users/register.html", context)

def register_learner(request):
    page = "learner"
    
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        learner_form = LearnerRegistrationForm(request.POST)
        if user_form.is_valid() and learner_form.is_valid():
            user = user_form.save()
            learner = learner_form.save(commit=False)
            learner.user = user
            learner.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect("home_page")
    else:
        user_form = UserRegistrationForm()
        learner_form = LearnerRegistrationForm()

    context = {
        "user_form": user_form,
        "learner_form": learner_form,
        "page": page
    }

    return render(request, "users/register.html", context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Manually authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('home_page')  
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, "users/login_user.html")



def logout_user(request):
    logout(request)
    return redirect("login_user")