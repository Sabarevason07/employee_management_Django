from django.contrib import admin
from .models import Emp_Data,LeaveRequest,Task,DailyWages,Notification

data={Emp_Data,LeaveRequest,Task,DailyWages,Notification}

admin.site.register(data)

