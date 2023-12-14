from django import forms
from .models import Question, Submission, Choice
class LessonQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['lesson', 'title', 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["lesson"].widget.attrs.update({"class":"form-control col-sm-10 custom-width", "placeholder":" Subject Name"})
        self.fields["title"].widget.attrs.update({"class":"form-control", "placeholder":" Order"})
        self.fields["content"].widget.attrs.update({"class":"form-control"})


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [  'title', 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["lesson"].widget.attrs.update({"class":"form-control col-sm-10 custom-width", "placeholder":" Question Title"})
        self.fields["title"].widget.attrs.update({"class":"form-control col-sm-10 custom-width", "placeholder":" Question Title"})
        self.fields["content"].widget.attrs.update({"class":"form-control col-sm-10 custom-width", "placeholder":" Question Content"})



class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['choices']
        widgets = {
            'choices': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, choices=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Pop 'choices' from kwargs
        choices = kwargs.pop('choices', None)

        # Limit the choices for the 'choices' field to the provided choices
        if choices is not None:
            self.fields['choices'].queryset = choices

        # Add Bootstrap styling and custom margins to the 'choices' field widget
        self.fields['choices'].widget.attrs.update({
            'class': 'form-check-input my-2',  # 'my-2' adds margin on the y-axis
        })




        
class ChoiceForm(forms.ModelForm):
    question = forms.ModelChoiceField(queryset=Question.objects.all())
    class Meta:
        model = Choice
        fields = ['question', 'content', 'is_correct']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["question"].widget.attrs.update({"class":"form-control col-sm-10 custom-width"})

