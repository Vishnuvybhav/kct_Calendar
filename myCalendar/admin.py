from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Event)
admin.site.register(Category)
admin.site.register(Colabrations)
admin.site.register(AccessLevels)
