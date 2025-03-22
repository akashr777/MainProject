

from django import forms
from .models import employee_table, Role

class EmployeeForm(forms.ModelForm):
    date_of_joining = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = employee_table
        fields = ['full_name', 'email', 'phone', 'salary', 'department', 'role', 'date_of_joining', 'profileimage']

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['role'].queryset = Role.objects.none()  # Empty initially

        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['role'].queryset = Role.objects.filter(department_id=department_id)
            except (ValueError, TypeError):
                pass  # Handle invalid department selection


from django import forms
from .models import campaign_request

class CampaignRequestForm(forms.ModelForm):
    class Meta:
        model = campaign_request
        fields = ['campaign_name','start_date','end_date', 'primary_color', 'font_style', 'theme', 'campaign_text','additional_text','creative_requirements', 'ad_effects','ad_placement','estimated_budget']



from django import forms
from .models import Task

class CreativeUploadForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['creative_file']

class CreativeReviewForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['reviewed_by_cd', 'feedback']



from django import forms
from .models import Task, campaign_request, Role

class TaskForm(forms.Form):
    title = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    campaign = forms.ModelChoiceField(queryset=campaign_request.objects.filter(status="approved"))
    role_name = forms.ModelChoiceField(queryset=Role.objects.all(), label="Assign to Role")
    deadline = forms.DateField()









# from django import forms
# from .models import Task, employee_table, campaign_request, Department

# class TaskForm(forms.ModelForm):
#     campaign = forms.ModelChoiceField(
#         queryset=campaign_request.objects.filter(status="Accepted"),
#         empty_label="Select Campaign",
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )

#     department = forms.ModelChoiceField(
#         queryset=Department.objects.all(),
#         empty_label="Select Department",
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )

#     assigned_to = forms.ModelMultipleChoiceField(
#         queryset=employee_table.objects.none(),  # ✅ Dynamically set in `__init__`
#         widget=forms.SelectMultiple(attrs={'class': 'form-control'})
#     )

#     progress = forms.IntegerField(
#         initial=0,  # ✅ Default to 0% progress
#         required=True,  # Ensure it's submitted with the form
#         widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100})
#     )

#     class Meta:
#         model = Task
#         fields = ['campaign', 'department', 'assigned_to', 'task_name', 'description', 'priority', 'status', 'deadline', 'progress']
#         widgets = {
#             'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'status': forms.Select(attrs={'class': 'form-control'}),
#             'priority': forms.Select(attrs={'class': 'form-control'}),
#         }

#     def __init__(self, *args, **kwargs):
#         department_id = kwargs.pop('department_id', None)
#         super(TaskForm, self).__init__(*args, **kwargs)

#         self.fields['campaign'].label_from_instance = lambda obj: obj.campaign_name   

#         # ✅ Ensure `assigned_to` is filtered based on department
#         if department_id:
#             self.fields['assigned_to'].queryset = employee_table.objects.filter(department_id=department_id)
#         elif self.instance and self.instance.department:
#             self.fields['assigned_to'].queryset = employee_table.objects.filter(department=self.instance.department)
#         else:
#             self.fields['assigned_to'].queryset = employee_table.objects.none()  # Empty unless department selected












# from django import forms
# from .models import TaskComment

# class TaskCommentForm(forms.ModelForm):
#     class Meta:
#         model = TaskComment
#         fields = ['comment']
#         widgets = {
#             'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write a comment...'}),
#         }







# from django import forms
# from .models import AdCreative

# class AdCreativeForm(forms.ModelForm):
#     class Meta:
#         model = AdCreative
#         fields = ['creative_type', 'file', 'text_content']  # ✅ Use the correct field names

# from django import forms
# from .models import FinalAdSubmission

# class FinalAdSubmissionForm(forms.ModelForm):
#     class Meta:
#         model = FinalAdSubmission
#         fields = ['ad_creative', 'submitted_by', 'client', 'status']




# from django import forms
# from .models import FinalAdCreative

# class FinalCreativeUploadForm(forms.ModelForm):
#     text_content = forms.CharField(widget=forms.Textarea, required=False)  # Optional text

#     class Meta:
#         model = FinalAdCreative
#         fields = ['text_content']  # Exclude file field (handled separately)

