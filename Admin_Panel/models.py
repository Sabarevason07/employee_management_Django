from django.db import models
from decimal import Decimal 
from django.contrib.auth.models import User
from datetime import date
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Create your models here.
class Emp_Data(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    EmpId=models.IntegerField(default="")
    Email=models.EmailField(max_length=50,default="")
    FirstName=models.CharField(max_length=50,default="")
    LastName=models.CharField(max_length=50,default="")
    Age=models.IntegerField(default="")
    Department=models.CharField(max_length=50,default="")
    Address=models.CharField(max_length=100,default="")
    ProfilePicture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    CTC = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    GrossSalary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.FirstName} {self.LastName}"

    def calculate_net_salary(self):
        # Convert the float value 0.10 to Decimal
        deduction_percentage = Decimal('0.10')  
        deductions = (self.CTC - self.GrossSalary) * deduction_percentage
        net_salary = self.GrossSalary - deductions
        return net_salary

# LeaveRequest model
class LeaveRequest(models.Model):
    employee = models.ForeignKey(Emp_Data, on_delete=models.CASCADE)  # Link to employee
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    admin_comments = models.TextField(blank=True, null=True)  # Admin can leave comments when approving/rejecting

    def __str__(self):
        return f"Leave Request by {self.employee.FirstName} {self.employee.LastName} - Status: {self.status}"
    
# Task model
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ManyToManyField(User, related_name='tasks', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
    

    
# New DailyWages Model
class DailyWages(models.Model):
    employee = models.ForeignKey(Emp_Data, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    wage_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    awarded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # HR/admin who awards the wage

    def __str__(self):
        return f"Wage awarded to {self.employee.FirstName} on {self.date}"

    @staticmethod
    def calculate_monthly_wages(employee, month, year):
        total_wages = DailyWages.objects.filter(
            employee=employee, 
            date__year=year, 
            date__month=month
        ).aggregate(total=models.Sum('wage_amount'))['total'] or Decimal('0.00')
        return total_wages
    


# notification
class Notification(models.Model):
    employee = models.ForeignKey(Emp_Data, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.employee.FirstName} at {self.created_at}"
    
    


class EmployeeFeedback(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_text = models.TextField("Feedback", max_length=1000)
    rating = models.IntegerField("Rating (1-5)", choices=[(i, str(i)) for i in range(1, 6)])
    sentiment_level = models.CharField("Sentiment Level", max_length=10, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Analyze sentiment using VADER
        sid = SentimentIntensityAnalyzer()
        sentiment_score = sid.polarity_scores(self.feedback_text)['compound']
        
        if sentiment_score >= 0.05:
            self.sentiment_level = "Positive"
        elif sentiment_score <= -0.05:
            self.sentiment_level = "Negative"
        else:
            self.sentiment_level = "Neutral"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Feedback from {self.employee.username} - {self.sentiment_level}"
        super().save(*args, **kwargs)