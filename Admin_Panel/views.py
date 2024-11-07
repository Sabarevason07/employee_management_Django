from django.shortcuts import render,redirect,get_object_or_404
from .models import Emp_Data,LeaveRequest,Task,DailyWages,Notification,EmployeeFeedback
from .forms import CreateUserForm,TaskForm,AwardWagesForm,EmployeeFeedbackForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as log
import face_recognition
import cv2
import numpy as np
import os
import csv
from datetime import datetime,date, timedelta
from django.conf import settings
from django.http import JsonResponse
from decimal import Decimal
from django.db.models import Avg
from django.core.mail import send_mail
import qrcode
from io import BytesIO
import base64
from collections import Counter

 


# Create your views here.

def register(request):    
    if request.method=='POST':
        name=request.POST["username"]
        email=request.POST["email"]
        password1=request.POST["password1"]
        password2=request.POST["password2"]

        if password1==password2:        
            user=User.objects.create_user(username=name,email=email,password=password1)
            user.is_staff=True
            # user.is_superuser=True
            user.save()
            messages.success(request,'Your account has been created! You are able to login')
            return redirect('Login')
        else:
            messages.warning(request,'Password Mismatching...!!!')
            return redirect('Register')        
    else:
        form=CreateUserForm()        
        return render(request,"register.html",{'form':form})
    

def profile(request):
    user_email = request.user.email
    net_salary = None 

    employee = None

    try:
        employee = Emp_Data.objects.get(Email=user_email)
        net_salary = employee.calculate_net_salary()  
    except Emp_Data.DoesNotExist:
        pass

    return render(request, 'profile.html',{'employee': employee, 'net_salary': net_salary})
    
def logout(request):
    log(request)
    return render(request,"logout.html")

@login_required
def add_employee(request):
    return render(request,'add_employee.html')

@login_required
def add(request):
    if request.method == 'POST':
        empid = request.POST.get('empid')
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        age = request.POST.get('age')
        department = request.POST.get('department')
        address = request.POST.get('address')
        profilepicture = request.FILES.get('profilepicture')
        
        ctc = Decimal(request.POST.get('CTC')) if request.POST.get('CTC') else None
        gross = Decimal(request.POST.get('GrossSalary')) if request.POST.get('GrossSalary') else None

        # Create a new employee instance
        new_employee = Emp_Data(
            EmpId=empid,
            Email=email,
            FirstName=firstname,
            LastName=lastname,
            Age=age,
            Department=department,
            Address=address,
            CTC=ctc,
            GrossSalary=gross
        )

        # Handle profile picture if provided
        if profilepicture:
            new_employee.ProfilePicture = profilepicture

        # Save the new employee instance to the database
        new_employee.save()

        messages.success(request, 'Employee added successfully')
        return redirect('Home')  # Redirect to the success page
    else:
        return render(request, 'add_employee.html')

@login_required
def update(request, id):
    employee = get_object_or_404(Emp_Data, id=id)

    if request.method == 'POST':
        empid = request.POST['empid']
        email = request.POST['email']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        age = request.POST['age']
        department = request.POST['department']
        address = request.POST['address']
        profilepicture = request.FILES.get('profilepicture')
        ctc = request.POST.get('CTC')
        gross = request.POST.get('GrossSalary')
        

        # Update the employee fields
        employee.EmpId = empid
        employee.Email = email
        employee.FirstName = firstname
        employee.LastName = lastname
        employee.Age = age
        employee.Department = department
        employee.Address = address
        employee.ProfilePicture = profilepicture
        employee.CTC = ctc
        employee.GrossSalary = gross

        if profilepicture:
            employee.ProfilePicture = profilepicture

        # Save the changes to the database
        employee.save()

        messages.success(request, 'Employee updated successfully')
        return redirect('Home')

    return render(request, 'edit_employee.html', {'data': employee})

@login_required
def delete(request,id):
    employee=get_object_or_404(Emp_Data,id=id)
    employee.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('Home')

@login_required
def view(request,id):
   
    employee = get_object_or_404(Emp_Data,id=id)
    net_salary = employee.calculate_net_salary()
    return render(request, 'view.html',{'employee': employee,'net_salary': net_salary})


def home(request):
    if request.user.is_superuser:
        mydata = Emp_Data.objects.all()
        return render(request, 'home.html', {'data': mydata})
    else:
        # Get the employee based on the logged-in user's email
        employee = get_object_or_404(Emp_Data, Email=request.user.email)
        
        # Get today's wage for the employee
        today_wage = DailyWages.objects.filter(employee=employee, date=date.today()).first()

        # Get all employee data
        mydata = Emp_Data.objects.all()

        # Count leave requests for the employee
        leave_requests = LeaveRequest.objects.filter(employee=employee).count()

        # Get wage history for the line chart
        wage_history = DailyWages.objects.filter(employee=employee).order_by('date')
        wage_dates = [wage.date.strftime('%Y-%m-%d') for wage in wage_history]
        wage_amounts = [wage.wage_amount for wage in wage_history]

        # Render the template with the data
        return render(request, 'home.html', {
            'data': mydata,
            'today_wage': today_wage,
            'count': leave_requests,
            'wage_dates': wage_dates,
            'wage_amounts': wage_amounts,
        })

def main(request):
    return render(request,'main.html')

@login_required
def about(request):
    return render(request,'about.html')

from django.db.models import Count, Avg,Sum
def dashboard(request):
    # Employee Salary Aggregation
    users = User.objects.all()  #fetch all users
    employees = Emp_Data.objects.all()
    total_employees = employees.count()
    total_salary = employees.aggregate(total_salary=Sum('CTC'))['total_salary']
    average_salary = total_salary / total_employees if total_employees > 0 else 0
    end_date = datetime.today()
    start_date = end_date - timedelta(days=30)
    daily_wages = DailyWages.objects.filter(date__range=[start_date, end_date])

    # Prepare the data for the line chart (dates and wages)
    dates = [wage.date for wage in daily_wages]
    wages = [wage.wage_amount for wage in daily_wages]

    # Department Aggregation
    departments = Emp_Data.objects.values('Department').annotate(count=Count('Department'))

    # LeaveRequest Aggregation
    leave_status_count = LeaveRequest.objects.values('status').annotate(status_count=Count('status'))
    
    # Prepare context for template
    context = {
        'users':users,
        'employees': employees,
        'total_employees': total_employees,
        'average_salary': average_salary,
        'departments': departments,
        'leave_status_count': leave_status_count,
        'daily_wages_dates': dates,
        'daily_wages_amounts': wages,
    }

    return render(request, 'dashboard.html', context)
 
@login_required
def update_user(request,id):
        user = get_object_or_404(User,id=id)
        if request.method=='POST':
            uname=request.POST["username"]
            email=request.POST["email"]

            user.username=uname
            user.email=email
            user.save()

            messages.success(request, 'updated successfully')
            return redirect('Dashboard') 
    
        return render(request,'edit_user.html',{'data':user})
        
@login_required
def delete_user(request,id):
    user=get_object_or_404(User,id=id)
    user.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('Dashboard')



@login_required
def apply_leave(request):
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        reason = request.POST['reason']
        employee = Emp_Data.objects.get(Email=request.user.email)

        leave_request = LeaveRequest(
            employee=employee,
            start_date=start_date,
            end_date=end_date,
            reason=reason
        )
        leave_request.save()

        messages.success(request, 'Your leave request has been submitted successfully!')
        return redirect('leave_status')
    
    return render(request, 'apply_leave.html')

# Employee views their leave status
@login_required
def leave_status(request):
    employee = Emp_Data.objects.get(Email=request.user.email)
    leave_requests = LeaveRequest.objects.filter(employee=employee)
    action = 'reject'
    return render(request, 'leave_status.html', {'leave_requests': leave_requests,'is_reject':action})

# Admin views all leave requests
@login_required
def manage_leave_requests(request):
    if not request.user.is_staff:  # Ensure only admin users can access
        return redirect('leave_status')
    
    leave_requests = LeaveRequest.objects.all()
    return render(request, 'manage_leave_requests.html', {'leave_requests': leave_requests})

# Admin approves/rejects leave
@login_required
def approve_reject_leave(request, leave_id, action):
    # Ensure the user is a staff member
    if not request.user.is_staff:
        return redirect('leave_status')

    leave_request = get_object_or_404(LeaveRequest, id=leave_id)

    # Update the leave request status based on action
    if action == 'approve':
        leave_request.status = 'Approved'
        messages.success(request, 'Leave request has been approved.')
    elif action == 'reject':
        leave_request.status = 'Rejected'
        leave_request.admin_comments = request.POST.get('admin_comments', '')  # Get comments from POST data
        messages.success(request, 'Leave request has been rejected with comments.')

    # Save the leave request
    leave_request.save()

    # Redirect to the manage leave requests page
    return redirect('manage_leave_requests')


# Function to load and convert the image to RGB
@login_required
def load_image_rgb(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image at {image_path}")
        return None
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

@login_required
def attendance_view(request):
    now = datetime.now()
    csv_filename = 'attendance_records.csv'  # Constant CSV filename for attendance records

    # Get media path where profile pictures are stored
    profile_pictures_path = os.path.join(settings.MEDIA_ROOT, 'profile_pictures')

    # Handle POST request for marking attendance
    if request.method == 'POST':
        known_face_encodings = []
        known_face_names = []

        # Load all images from profile_pictures directory and encode faces
        for filename in os.listdir(profile_pictures_path):
            if filename.endswith((".jpg", ".jpeg", ".png")):
                image_path = os.path.join(profile_pictures_path, filename)
                image = face_recognition.load_image_file(image_path)
                encoding = face_recognition.face_encodings(image)

                # Check if face was detected in the image
                if encoding:
                    known_face_encodings.append(encoding[0])
                    known_face_names.append(os.path.splitext(filename)[0])  

        # Initialize webcam
        video_capture = cv2.VideoCapture(0)

        attendance_records = []  # List to hold attendance records
        attendance_marked = False

        while True:
            ret, frame = video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = ""

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                if name in known_face_names and not attendance_marked:
                    current_time = now.strftime("%H:%M:%S")
                    attendance_records.append([name, current_time])  # Store the record
                    attendance_marked = True
                    break

            if attendance_marked:
                break

            cv2.imshow("Attendance System", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

        # Append the attendance record to the CSV file
        if attendance_marked:
            with open(csv_filename, 'a', newline='') as f:
                inwriter = csv.writer(f)
                inwriter.writerow([name, current_time])  # Write the new record

        # Return the attendance records in the response
        return JsonResponse({"status": "Attendance marked successfully.", "attendance": attendance_records})

    # Handle GET request to display attendance records
    attendance_records = []
    if os.path.exists(csv_filename):
        with open(csv_filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            attendance_records = list(reader)

    return render(request, 'attendance.html', {'attendance_records': attendance_records})


@login_required
def assign_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            assign_to_all = form.cleaned_data.get('assign_to_all')

            if assign_to_all:
                # Assign the task to all employees (ManyToMany relationship)
                all_employees = User.objects.all()
                task.save()  # First save the task itself
                task.assigned_to.set(all_employees)  # Use .set() for ManyToManyField

                # Send email to all assigned users
                for employee in all_employees:
                    send_mail(
                        subject=f"New Task Assigned: {task.title}",
                        message=f"Hello {employee.username},\n\nYou have been assigned a new task: {task.title}.\nDescription: {task.description}\nDue Date: {task.due_date}\n\nBest regards,\nYour Company",
                        from_email='admin@yourcompany.com',
                        recipient_list=[employee.email],
                    )

            else:
                # Assign the task to a specific user
                task.save()
                if form.cleaned_data['assigned_to']:
                    assigned_user = form.cleaned_data['assigned_to']
                    task.assigned_to.set([assigned_user])  # Use .set() for specific assignment

                    # Send email to the specific assigned user
                    send_mail(
                        subject=f"New Task Assigned: {task.title}",
                        message=f"Hello {assigned_user.username},\n\nYou have been assigned a new task: {task.title}.\nDescription: {task.description}\nDue Date: {task.due_date}\n\nBest regards,\nsabverse.pvt.Ltd",
                        from_email='admin@yourcompany.com',
                        recipient_list=[assigned_user.email],
                    )

            messages.success(request, 'Task assigned and email sent successfully.')
            return redirect('Home')  # Redirect to a success page after saving
    else:
        form = TaskForm()

    return render(request, 'assign_task.html', {'form': form})

@login_required
def task_list(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'task_list.html', {'tasks': tasks})



def award_wages(request):
    if request.method == 'POST':
        form = AwardWagesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'awarded successfully.')
            return redirect('Home')  
    else:
        form = AwardWagesForm()

    return render(request, 'award_wages.html', {'form': form})



def view_monthly_wages(request):
    employee = Emp_Data.objects.get(user=request.user)
    current_month = datetime.now().month
    current_year = datetime.now().year
    total_wages = DailyWages.calculate_monthly_wages(employee, current_month, current_year)
    
    return render(request, 'home.html', {'total_wages': total_wages})


def send_request(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        employee = Emp_Data.objects.get(id=employee_id)  # Fetch the employee instance
        # Create a notification
        Notification.objects.create(
            employee=employee,
            message="User requested profile update/removal."
        )
        messages.success(request, "Your request has been sent to the administrator.")
        return redirect('Profile') 
    
def notification(request):
        notifications = Notification.objects.all().order_by('-created_at')
        return render(request, 'notification.html', {'notifications': notifications})


@login_required
def generate_qr_code(request, employee_id):
    # Get employee details
    employee = get_object_or_404(Emp_Data,id=employee_id)

    # Compile profile details for QR code
    qr_data = f"Employee ID: {employee.EmpId}\n" \
              f"Email: {employee.Email}\n" \
              f"First Name: {employee.FirstName}\n" \
              f"Last Name: {employee.LastName}\n" \
              f"Age: {employee.Age}\n" \
              f"Department: {employee.Department}\n" \
              f"Address: {employee.Address}"


 # Generate QR code
    qr = qrcode.make(qr_data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Pass QR code as Base64 to the template
    return render(request, 'qr_page.html', {
        'employee': employee,
        'qr_image_base64': qr_image_base64,
    })

def visual(request):
    return render(request,'visualization.html')


@login_required
def employee_feedback(request):
    if request.method == "POST":
        form = EmployeeFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.employee = request.user
            feedback.save()
            return redirect('employee_feedback')  
    else:
        form = EmployeeFeedbackForm()
    return render(request, 'employee_feedback.html', {'form': form})

def feedback_list(request):
    feedbacks = EmployeeFeedback.objects.all().order_by('-submitted_at')
    total_feedbacks = feedbacks.count()

    # Calculate sentiment counts and percentages
    sentiments = [feedback.sentiment_level for feedback in feedbacks]
    sentiment_counts = Counter(sentiments)

    sentiment_percentages = {
        "Positive": (sentiment_counts.get("Positive", 0) / total_feedbacks) * 100 if total_feedbacks > 0 else 0,
        "Neutral": (sentiment_counts.get("Neutral", 0) / total_feedbacks) * 100 if total_feedbacks > 0 else 0,
        "Negative": (sentiment_counts.get("Negative", 0) / total_feedbacks) * 100 if total_feedbacks > 0 else 0,
    }

    context = {
        'feedbacks': feedbacks,
        'sentiment_counts': sentiment_percentages 
    }

    return render(request, 'feedback_list.html', context)