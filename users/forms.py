from django import forms
from .models import CustomUser, Instructor, Learner
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    full_name = forms.CharField(max_length=100)

    class Meta:
        model = CustomUser
        fields = ["full_name", "username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data["full_name"]
        first_name, last_name = full_name.split(" ", 1)
        user.first_name = first_name
        user.last_name = last_name
        if commit:
            user.save()
            # Check if the user is a learner before creating a Learner instance
            if hasattr(user, "learner"):
                Learner.objects.get_or_create(user=user)
            elif hasattr(user, "instructor"):
                Instructor.objects.get_or_create(user=user)
        return user

    # Adding widgets
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update({"placeholder": " Full Name"})
        self.fields["username"].widget.attrs.update({"placeholder": " Username"})
        self.fields["email"].widget.attrs.update({"placeholder": " Email"})
        self.fields["password1"].widget.attrs.update({"placeholder": " Password"})
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "Confirm Password"}
        )


class InstructorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ["full_time", "total_learners"]

    # adding widgets
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["total_learners"].widget.attrs.update(
            {"placeholder": " Total Learner"}
        )
        self.fields["full_time"].widget.attrs.update({"class": "form-check-input"})


class LearnerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Learner
        fields = ["occupation", "social_link"]

    # add widgets
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["occupation"].widget.attrs.update({"placeholder": " Occupation"})
        self.fields["social_link"].widget.attrs.update({"placeholder": " Social Link"})
