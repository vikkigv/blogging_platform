from django.contrib import admin

# Register your models here.
from core.models import *

admin.site.register(Blog)
admin.site.register(Comments)