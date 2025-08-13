from django.urls import path
from . import views  

urlpatterns = [
  
    path('', views.index, name='index'),
    path('departments/', views.viewDepartments, name='viewDepartments'),
    path('doctors/', views.viewDoctors,name='viewDoctors'),
    path('registeration/',views.registerPatients,name='registerPatients'),
    path('login/',views.loginUser, name='loginUser'),  # Assuming you have a login view
]
