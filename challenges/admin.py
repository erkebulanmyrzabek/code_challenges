from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Challenge, Solution, Certificate

admin.site.register(Challenge)
admin.site.register(Solution)
admin.site.register(Certificate)
