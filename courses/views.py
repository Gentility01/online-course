from django.shortcuts import render, redirect, get_object_or_404
from .forms import CourseForm, EnrollmentForm
from .models import Course, Enrollment
from lessons.models import Lesson
from django.contrib import messages

# Create your views here.

def create_course(request):
    course = "create_course"
    # check if user is super user
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, "You do not have permission to create a course.")
        return redirect("login_user")

    if request.method == "POST":
        # Set the created_by field to the logged-in user
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user
             # Manually set the instructors for the course
            instructors = form.cleaned_data['instructors']
            course.save()
            course.instructors.set(instructors)  # Assuming instructors is a ManyToManyField in the Course model
            messages.success(request, "Course created successfully.")
            return redirect("home_page")
        else: 
            messages.error(request, "Error creating the course")
    else:
        form = CourseForm()
    

    return render(request, "courses/course.html", {"form":form, "course":course})


def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    # get current courses
    current_courses = Course.objects.exclude(pk=course_id).order_by('pub_date')[:5]


    context = {
        "course":course,
        "current_courses":current_courses
    }
    return render(request, "courses/course_detail.html", context)



def edit_course(request, course_id):
    course = "edit_course"
    # check if user is super user
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, "You do not have permission to create a course.")
        return redirect("login_user")

    # Retrieve the course object
    course = get_object_or_404(Course, id=course_id)

    # Check if the current user is the owner of the course
    if request.user != course.created_by:
        messages.error(request, "You do not have permission to edit this course.")
        return redirect("home_page")

    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully.")
            return redirect("home_page")
        else:
            messages.error(request, "Error updating the course.")
    else:
        form = CourseForm(instance=course)
    return render(request, "courses/course.html", {"form":form})



def enroll_course(request, course_id):

    try:
        course = Course.objects.get(pk=course_id)

        # ceck if user is enrolled already or user is intructor
        user_already_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
        if  user_already_enrolled:
            messages.error(request, "Oops You're enrolled already")
            return redirect("enrolledcourse_details", course_id=course.id)

        elif not user_already_enrolled and  request.method == "POST":
            form = EnrollmentForm(request.POST)
            if form.is_valid():
                enrollment = form.save(commit=False)
                enrollment.user = request.user
                enrollment.course = course
                enrollment.save()
                return redirect("enrolledcourse_details", course_id=course.id)
        else:
            form = EnrollmentForm()
    except TypeError:
        messages.warning(request, "You must login before enrolling")
        return redirect("home_page")
        
    
    context = {
        "form":form,
        "course":course
    }
            
    return render(request, "courses/enroll_course.html", context)



def enrolledcourse_details(request, course_id):
    # get a course
    course = get_object_or_404(Course, pk=course_id)

    # Retrieve the current user's enrollments for all courses
    user_enrollment = request.user.enrollment_set.all()
    other_enrolledcourses = user_enrollment.exclude(course=course)

    # Retrieve lessons related to the enrolled course
    lessons_for_enrolled_course = Lesson.objects.filter(course=course)

    context = {
        "course":course,
        "enrolled_course":other_enrolledcourses,
        "lessons":lessons_for_enrolled_course

    }
   
    return render(request, "courses/enrolledcourse_detail.html", context)


def get_all_courses(request):
    courses = Course.objects.all()
    context = {
        "courses":courses
    }
    return render(request, "courses/all_courses.html", context)