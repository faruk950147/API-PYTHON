from django import  forms
from api.models import Task

class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'cols': '6', 'rows': '4', 'placeholder': 'Ádd Task'})
            
    class Meta:
        model = Task
        fields = (
            '__all__'
        )
        #exclude = ('completed',)
        widgets = {
            'title': forms.TextInput(attrs={
                'id': 'title',
                'class': 'form-control',
            }),
        }
        