from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date

from .models import Course, Enrollment
from lessons.forms import LessonForm
from .forms import EnrollmentForm, CourseForm
from users.models import Instructor, CustomUser


class CourseModelTest(TestCase):
    def setUp(self):
        # Create test data for the Course model
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.course = Course.objects.create(
            name="Test Course",
            image="course_images/test_image.jpg",
            description="Test description",
            pub_date=date.today(),
            created_by=self.user,
            total_enrollment=0,
        )

    def test_course_str_method(self):
        self.assertEqual(str(self.course), f"Name: {self.course.name}")


class EnrollmentModelTest(TestCase):
    def setUp(self):
        # Create test data for the Enrollment model
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.course = Course.objects.create(
            name="Test Course",
            image="course_images/test_image.jpg",
            description="Test description",
            pub_date=date.today(),
            created_by=self.user,
            total_enrollment=0,
        )
        self.enrollment = Enrollment.objects.create(
            user=self.user, course=self.course, mode="free", rating=4
        )

    def test_enrollment_str_method(self):
        expected_str = f"{self.user.username} enrolled in {self.course.name} on {self.enrollment.enrollment_date} (free mode) - Rating: {self.enrollment.rating}"
        self.assertEqual(str(self.enrollment), expected_str)

    def test_enrollment_defaults(self):
        self.assertEqual(self.enrollment.feedback, None)

    def test_enrollment_choices(self):
        self.assertEqual(
            self.enrollment.mode, "free"
        )  # Assuming default mode is 'free'


class CourseFormTest(TestCase):
    def setUp(self):
        # create a test user
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpassword"
        )

        # create an instructor assoicated with the user
        self.instructor = Instructor.objects.create(user=self.user, full_time=True)

    def test_valid_course_form(self):

        data = {
            "name": "Test Course",
            "image": "web.jpeg",
            "description": "Test description",
            "pub_date": "2023-12-13",
            "instructors": [self.instructor.id],
        }
        form = CourseForm(data=data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_blank_course_form(self):
        form = CourseForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["name"], ["This field is required."])
        self.assertEqual(form.errors["image"], ["This field is required."])
        self.assertEqual(form.errors["description"], ["This field is required."])
        self.assertEqual(form.errors["pub_date"], ["This field is required."])
        self.assertEqual(form.errors["instructors"], ["This field is required."])


class EnrollmentFormTest(TestCase):
    def test_valid_enrollment_form(self):
        data = {
            "mode": "free",
            "rating": 4,
            "feedback": "Test feedback",
        }
        form = EnrollmentForm(data=data)
        self.assertTrue(form.is_valid())

    def test_blank_enrollment_form(self):
        form = EnrollmentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["mode"], ["This field is required."])

    def test_invalid_rating(self):
        data = {
            "mode": "free",
            "rating": 6,  # Rating should be between 1 and 5
            "feedback": "Test feedback",
        }
        form = EnrollmentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["rating"], ["Ensure this value is less than or equal to 5."]
        )


# Add more tests for other functionalities as needed
