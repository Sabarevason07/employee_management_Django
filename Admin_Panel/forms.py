from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Emp_Data,Task,DailyWages
from .models import EmployeeFeedback
 
#users forms  
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        from .models import Emp_Data

#employees forms 
class EmpDataForm(forms.ModelForm):
    class Meta:
        model = Emp_Data
        fields = ['EmpId', 'Email', 'FirstName', 'LastName', 'Age', 'Department', 'Address', 'ProfilePicture', 'CTC', 'GrossSalary']
    CTC = forms.DecimalField(max_digits=10, decimal_places=2, required=True,
                             widget=forms.NumberInput(attrs={'placeholder': 'Enter CTC'}))
    GrossSalary = forms.DecimalField(max_digits=10, decimal_places=2, required=True,
                                      widget=forms.NumberInput(attrs={'placeholder': 'Enter Gross Salary'}))
    
#Tasks forms
class TaskForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.all(),  # Querying all users for individual selection
        widget=forms.Select,
        label="Assign To",
        required=False  # Make it optional since "Assign to All" can be selected
    )
    
    assign_to_all = forms.BooleanField(
        required=False,
        label="Assign to All Employees"
    )
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date', 'assign_to_all']

class AwardWagesForm(forms.ModelForm):
    class Meta:
        model = DailyWages
        fields = ['employee', 'date', 'wage_amount', 'awarded_by']

    employee = forms.ModelChoiceField(queryset=Emp_Data.objects.all(), label="Employee")
    wage_amount = forms.DecimalField(label="Wage Amount")
    date = forms.DateField(widget=forms.SelectDateWidget, label="Date")
    awarded_by = forms.HiddenInput() 

class EmailForm(forms.Form):
   email = forms.EmailField(label='Enter your email')   

   

class EmployeeFeedbackForm(forms.ModelForm):
    class Meta:
        model = EmployeeFeedback
        fields = ['feedback_text', 'rating']
        widgets = {
            'feedback_text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter your feedback here...'}),
            'rating': forms.Select()
        }
