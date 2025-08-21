from django.contrib import admin

# Register your models here.
from .models import Dept_tbl,Doctor_tbl,reg_tbl,book_tbl
admin.site.register(Dept_tbl) 
admin.site.register(Doctor_tbl) 
admin.site.register(reg_tbl)
admin.site.register( book_tbl)