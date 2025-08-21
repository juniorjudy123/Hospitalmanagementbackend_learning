# Create your views here.
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponse
from .models import Dept_tbl, Doctor_tbl, reg_tbl,book_tbl

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



def bookappointment(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        gender=request.POST.get('gender')
        date=request.POST.get('date')
        test=request.POST.getlist('test')
        doctor_name=request.POST.get('doctor_name')

        user_id = request.session.get('id1')
        user = reg_tbl.objects.get(id=user_id)

        obj=book_tbl.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            gender=gender,
            date=date,
            test=",".join(test),
            doctor_name=doctor_name,
            user=user
            )

        obj.save()
        msg='Appointment booked'

        return render(request,'patient.html',{'msg':msg})

    user_name = request.session.get('name')
    user_email= request.session.get('email')
    user_mobile=request.session.get('mobile')


    data=Doctor_tbl.objects.all()
  
    return render(request, "bookings.html",{'data':data,'name':user_name,'email':user_email,'mobile':user_mobile})


def viewappointments(request):
    user_id = request.session.get("id1")
    if not user_id:
        return redirect("loginUser")

    user_type = request.session.get("user_type", "patient")

    if user_type.lower() == "admin":
        appointments = book_tbl.objects.all().order_by("-date")
    else:
        appointments = book_tbl.objects.filter(user_id=user_id).order_by("-date")

    return render(request, "appointments.html", {"appointments": appointments})



def logout_view(request):
    logout(request)
    return redirect(index)