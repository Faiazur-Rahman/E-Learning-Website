from django.contrib import admin

from .models import Dbtable
from .models import videoTable

# Register your models here.

admin.site.register(Dbtable)
admin.site.register(videoTable)
