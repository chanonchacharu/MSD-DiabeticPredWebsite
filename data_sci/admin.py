from django.contrib import admin
from data_sci.models import PimaIndianDiabetic

@admin.register(PimaIndianDiabetic)
class PimaIndianDiabeticAdmin(admin.ModelAdmin):
    pass