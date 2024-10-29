from django.contrib import admin
from django.urls import path,include
from Admin_Panel import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/',admin.site.urls),
    path("",include('Admin_Panel.urls')),
]


































# from Message import views
# urlpatterns = [
#     path('admin/',admin.site.urls),                  
#     path('',views.message,name="Message"),                  
#     path('success/',views.success,name="Success"),                  
#     path('info/',views.info,name="Info"),                  
#     path('error/',views.error,name="Danger"),                  
#     path('warning/',views.warning,name="Warning"),                  

#SQlite Registration
# urlpatterns = [
#     path('admin/',admin.site.urls),
#     path('',views.home,name="home"),# 127.0.0.1:8000/         
#     path('addData',views.addData,name="addData"),
#     path('updateData/<int:id>',views.updateData,name="updateData"),
#     path('deleteData/<int:id>',views.deleteData,name="deleteData"),
# ]


