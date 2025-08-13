from django.db import models

# Create your models here.
class Dept_tbl(models.Model):
    dept_name=models.CharField(max_length=50)
    description=models.CharField(max_length=100)

    def __str__(self):
        return self.dept_name
    

# create a doctor table
class Doctor_tbl(models.Model):
    doctor_name=models.CharField(max_length=50)
    doctor_img=models.FileField(upload_to="pictures" )     
    dept_name=models.ForeignKey(Dept_tbl, on_delete=models.CASCADE)


    def __str__(self):
        return self.doctor_name
    
#create a user registeration table 

class reg_tbl(models.Model):
    name=models.CharField(max_length=50)
    phone=models.IntegerField()
    email=models.EmailField()
    password=models.CharField(max_length=50)
    cnpassword=models.CharField(max_length=50)
    user_type=models.CharField(max_length=50, default='admin')

    def __str__(self):
        return self.name