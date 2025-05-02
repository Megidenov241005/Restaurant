from django.contrib import admin
# from django.contrib.auth.models import User
from .models import *


# admin.site.register(User)

admin.site.register(Manager)
admin.site.register(Client)
admin.site.register(Table)
admin.site.register(Reserve)