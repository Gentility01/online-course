from django import forms 
from .models import Course, Enrollment
from users.models import Instructor

class CourseForm(forms.ModelForm):
    pub_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Date Created', 'type': 'date'})
    )

    class Meta:
        model = Course
        fields = ['name',  'image', 'description', 'pub_date', 'instructors']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update({"class": "form-control", "placeholder": " Course Name"})
        self.fields["image"].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs.update({"class": "form-control description", "placeholder": " Course Description"})
        self.fields["pub_date"].widget.attrs.update({"class": "form-control", "placeholder": " Date Created"})
        # self.fields["instructors"].widget.attrs.update({"class": "form-control col-sm-10 custom-width"})

        # Use ModelMultipleChoiceField for the instructors field
        self.fields["instructors"] = forms.ModelMultipleChoiceField(
            queryset=Instructor.objects.all(),  # Replace with the actual queryset for your instructors
            widget=forms.SelectMultiple(attrs={"class": "form-control col-sm-10 custom-width"}),
        )

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ["mode", "rating", "feedback"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["mode"].widget.attrs.update({"class":"form-control col-sm-10 custom-width"})
        self.fields["rating"].widget.attrs.update({"class":"form-control", "placeholder":" Rate Course"})
        self.fields["feedback"].widget.attrs.update({"class":"form-control", "placeholder":"Add Feedback (Optional)"})
