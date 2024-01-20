from django.shortcuts import render, redirect, get_object_or_404
from .forms import LessonForm
from .models import Lesson
from courses.models import Course, Enrollment
from django.contrib import messages
from users.models import Instructor
from django.http import HttpResponse
# Create your views here.



def create_lesson(request, course_id):
    # Step 1: Get the course for which the lesson is being created
    course = get_object_or_404(Course, id=course_id)

    # Step 2: Check if the user is authenticated and is an instructor for the specific course
    if not request.user.is_authenticated or not course.instructors.filter(user=request.user).exists():
        messages.error(request, "You do not have permission to create a lesson for that course.")
        return redirect("/")

    if request.method == "POST":
        form = LessonForm(request.POST)
        if form.is_valid():
            # Step 3: Associate the lesson with the specific course
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()

            messages.success(request, "Lesson created successfully.")
            return redirect("lesson_success")
        else:
            messages.error(request, "Error creating the lesson. Please check the form.")
    else:
        form = LessonForm()

    return render(request, "lessons/create_lesson.html", {"form": form, "course": course})


def lesson_success(request):
    return render(request, "lessons/lesson_success.html")





def instructors_lessons_list(request, instructor_id):
    # getting an intructor 
    instructor = Instructor.objects.get(pk=instructor_id)

    # get lessons created by a particular  instructor
    lessons = Lesson.objects.filter(course__instructors=instructor)

    context = {
        "instructor":instructor,
        "lessons":lessons
    }
    return render(request, "lessons/instructors_lesson_list.html", context)


def edit_lesson(request, course_id, lesson_id):
    # Step 1: Get the course and lesson for editing
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)

    # Step 2: Check if the user is authenticated and is an instructor for the specific course
    if not request.user.is_authenticated or not course.instructors.filter(user=request.user).exists():
        messages.error(request, "You do not have permission to edit lessons for this course.")
        return redirect("login_user")

    if request.method == "POST":
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            # Step 3: Save the edited lesson
            edited_lesson = form.save()

            messages.success(request, "Lesson edited successfully.")
            return redirect("lesson_success")
        else:
            messages.error(request, "Error editing the lesson. Please check the form.")
    else:
        form = LessonForm(instance=lesson)

    return render(request, "lessons/edit_lesson.html", {"form": form, "course": course, "lesson": lesson})


def enrolled_course_lesson_details(request, course_id, lesson_id):
    # Get the logged-in user
    user = request.user

    # Get all lessons for the specified course and lesson ID
    lessons = Lesson.objects.filter(course_id=course_id, pk=lesson_id)

    # Handle the case where the lesson is not found
    if not lessons.exists():
        return HttpResponse("Lesson not found")

    # If the user is an instructor, grant access
    if Instructor.objects.filter(user=request.user).exists():
        context = {
            'user': user,
            'lesson': lessons.first(),  # You may need to add additional logic to select the correct lesson
        }
        return render(request, "lessons/enrolled_course_subject_details.html", context)

    # If the user is not an instructor, try to get the enrollments for the specified user and course
    enrollments = Enrollment.objects.filter(user=user, course_id=course_id)

    # Handle the case where the user is not enrolled in the specified course
    if not enrollments.exists():
        return HttpResponse("You do not have permission to view this lesson.")

    # Filter lessons based on the user's enrollments
    lesson = lessons.filter(course=enrollments.first().course).first()

    if lesson:
        # Now, you have the details of the enrolled lesson
        context = {
            'user': user,
            'enrollment': enrollments.first(),
            'lesson': lesson,
        }
        return render(request, "lessons/enrolled_course_subject_details.html", context)

    return HttpResponse("Lesson not found")

    #get the logged in user
    user = request.user

    # get all lessons for specified course
    lessons = Lesson.objects.filter(course_id=course_id, id=lesson_id)

    # handle the case where the lesson is not found
    if not lessons.exists():
        return HttpResponse()

    # If the user is an instructor, grant access
    if Instructor.objects.filter(user=request.user).exists():
        context = {
            'user': user,
            'lesson': lessons.first(),  # You may need to add additional logic to select the correct lesson
            
        }
        return render(request, "lessons/enrolled_course_subject_details.html", context)
    # If the user is not an instructor, try to get the enrollment for the specified user and course
    enrollments = Enrollment.objects.filter(user=user, course_id=course_id)

    # Handle the case where the user is not enrolled in the specified course
    if not enrollments.exists():
        return HttpResponse("You do not have permission to view this lesson.")

    # Filter lessons based on the user's enrollment
    lesson = lessons.filter(course=enrollments.course).first()

    if lesson:
        # Now, you have the details of the enrolled lesson
        context = {
            'user': user,
            'enrollment': enrollment,
            'lesson': lesson,
        }

        return render(request, "lessons/enrolled_course_subject_details.html", context)
    return HttpResponse("Lesson not found")