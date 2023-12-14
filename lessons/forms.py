from django import forms
from .models import Lesson


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["title", "order",  "content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class":"form-control", "placeholder":" Subject Name"})
        self.fields["order"].widget.attrs.update({"class":"form-control", "placeholder":" Order"})
       
