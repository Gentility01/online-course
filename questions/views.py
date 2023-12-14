from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from lessons.models import Lesson
from courses.models import Course, Enrollment
from .forms import QuestionForm, ChoiceForm, SubmissionForm
from .models import Question, Submission, Choice
from django.contrib import messages
# Create your views here.


def student_askquestion(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.lesson = lesson
            question.save()
            messages.success(request, 'Your question was submitted successfully...')
    else:
        form = QuestionForm()
        
    return render(request, "questions/student_askquestion.html", {"form":form})



def lesson_questions(request, course_id, lesson_id):
    # get the course id and lesson id
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id)

    # Check if the user is authenticated and is an instructor for the specific course
    if (not request.user.is_authenticated or not
            course.instructors.filter(user=request.user).exists()):
        messages.error(request, "You do not have permission to set questions for this lesson")
        return redirect("login_user")

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            # Ensure the user is set before saving the question
            question = form.save(commit=False)
            question.user = request.user  
            question.lesson = lesson
            question.save()
            messages.success(request, "Question was Created Successfully")
    else:
        form = QuestionForm()

    context = {
        "form": form,
        "lesson": lesson
    }

    return render(request, "questions/lesson_question.html", context)


def set_question_choices(request, lesson_id):
    """Sets the question choices for a specific lesson."""
    lesson = get_object_or_404(Lesson, id=lesson_id)

    # Check if the user is authenticated and is an instructor for the specific course
    if not (request.user.is_authenticated and lesson.course.instructors.filter(user=request.user).exists()):
        messages.error(request, "You do not have permission to set options for this lesson")
        return redirect("login_user")

    # Get questions for the specific lesson and user
    questions = Question.objects.filter(lesson=lesson, user=request.user)

    # get the choice form
    if request.method == "POST":
        form = ChoiceForm(request.POST)
        form.fields['question'].queryset = questions  # Filter available questions in the form

        if form.is_valid():
            question = form.cleaned_data["question"]
                

            choice = form.save(commit=False)
            choice.lesson = lesson
            choice.question = question
            choice.user = request.user
            choice.save()  
            
            messages.success(request, "Choice was created successfully")
            return redirect(request.path_info)  # Redirect to the appropriate view after successful submission
    else:
        form = ChoiceForm()
        form.fields['question'].queryset = questions  # Filter available questions in the form
    
    context = {
        "form": form,
        "lesson": lesson,
    }

    return render(request, "questions/choice_question.html", context)


def lesson_question_lists(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    # Retrieve the instructor for the course
    instructor = lesson.course.instructors.first()

   
    # Retrieve questions in the specified lesson asked by the instructor
    questions_in_lesson_by_instructor = Question.objects.filter(
        lesson=lesson, user=instructor.user
    )

    # Create a list to store whether the user has submitted a response for each question
    user_has_submitted = []

    for question in questions_in_lesson_by_instructor:
        # Check if the user has submitted a response for the current question
        user_submission = Submission.objects.filter(user=request.user, question=question).first()
        user_has_submitted.append(user_submission is not None)

    # get the total score for the lesson questions by a particular user
    total_score = Submission.objects.filter(question__lesson=lesson, user=request.user).aggregate(Sum('score'))['score__sum']
    
    context = {
        'questions': zip(questions_in_lesson_by_instructor, user_has_submitted),
        'lesson': lesson,
        # "is_correct": is_correct, 
        "total_score":total_score, 
    }

    return render(request, "questions/lesson_question_list.html", context)

def enrolled_student_course_list(request):
    # Assuming the user is authenticated
    user = request.user

    # Retrieve all enrollments for the current user
    user_enrollments = Enrollment.objects.filter(user=user)

    # Extract the courses from the enrollments
    enrolled_courses = [enrollment.course for enrollment in user_enrollments]

    # Pass the enrolled courses to the template
    context = {
        'user': user,
        'enrolled_courses': enrolled_courses,
    }
    return render(request, "questions/enrolled_studentcourselist.html", context)


def review_and_submit_question(request,  lesson_id, question_id):
    lesson = Lesson.objects.get(id=lesson_id)
    question = Question.objects.get(id=question_id)
    is_correct = False
    
    # filter choice base on the current question
    choices = Choice.objects.filter(question=question)

    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():
          user = request.user
          selected_choice = form.cleaned_data["choices"]  

          #save the submission to the database
          submission = Submission.objects.create(
              user=user, question=question, 
          )
          submission.choices.set(selected_choice)

          #grade the submission and save
          is_correct = submission.grade_submission()
          return redirect("lesson_question_lists", lesson_id=lesson_id)
    else:
        form = SubmissionForm()

        # Limit the choices for the 'choices' field to the provided choices
        form.fields['choices'].queryset = choices

    context = {
        "form": form,
        "lesson": lesson,
        "question": question,
        "choices": choices,
        "is_correct": is_correct,
    }
    return render(request, "questions/review_and_submit_question.html", context )
