from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse

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
   
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cnpassword = request.POST.get('cnpassword')
        
        if password != cnpassword:
            messages.error(request, "Passwords do not match.")
        
        new_patient = reg_tbl(
            name=name,
            phone=phone,
            email=email,
            password=password,
            cnpassword=cnpassword,
            user_type='patient'  # force user_type as 'patient'
        )
        new_patient.save()
      
       
         # Show success message and redirect to login
        messages.success(request, "Registration successful! Please log in.")
        return redirect('loginUser')  
    
    return render(request, 'regform.html')  



def loginUser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Get the single user matching credentials
            user = reg_tbl.objects.get(email=email, password=password)

            # Save details to session
            request.session['id1'] = user.id
            request.session['name'] = user.name
            request.session['email'] = user.email
            request.session['password'] = user.password  # not recommended for security
            request.session['user_type'] = user.user_type

            # Redirect based on user type
            if user.user_type.lower() == "admin":
                return render(request, 'admin.html')
            else:
                return render(request, 'patient.html')

        except reg_tbl.DoesNotExist:
            return HttpResponse("Invalid email or password.")

    # For GET request, show the login page
    return render(request, 'login.html')
