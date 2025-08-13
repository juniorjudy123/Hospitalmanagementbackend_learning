from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Dept_tbl, Doctor_tbl, reg_tbl

def index(request):
    return render(request, 'index.html')


def viewDepartments(request):
   data= Dept_tbl.objects.all()
   print(data)
   return render(request, 'viewDepartments.html', {'data': data})   

def viewDoctors(request):
    data = Doctor_tbl.objects.all()
    print(data)
    return render(request, 'viewdocs.html', {'data': data})
   
def registerPatients(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cnpassword = request.POST.get('cnpassword')
        
        if password != cnpassword:
            return HttpResponse("Passwords do not match.")
        
        new_patient = reg_tbl(
            name=name,
            phone=phone,
            email=email,
            password=password,
            cnpassword=cnpassword,
            user_type='patient'  # force user_type as 'patient'
        )
        new_patient.save()
      
       
        return HttpResponse("Registration successful!")
    
    return render(request, 'regform.html')  # Render the registration form template



def loginUser(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        try:
            user = reg_tbl.objects.get(email=email, password=password)
            
            if user:
                return HttpResponse(f"Welcome {user.name}!")
        
        except reg_tbl.DoesNotExist:
            return HttpResponse("Invalid email or password.")
   
    return render(request, 'login.html')  # Render the login form template      

