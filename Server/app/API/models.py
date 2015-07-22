from django.db import models
from django.contrib import admin
import time
# Create your models here.
class user_info(models.Model):
    username = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)
    location = models.CharField(max_length = 50)
    sub_topic = models.CharField(max_length = 500)

class user_infoAdmin(admin.ModelAdmin):
    list_display = ('username','location','sub_topic')

admin.site.register(user_info,user_infoAdmin)

class device_data(models.Model):
    device_id = models.CharField(max_length = 50)
    hrm = models.CharField(max_length = 50)
    date = models.DateTimeField(auto_now_add=True)


class device_dataAdmin(admin.ModelAdmin):
    list_display = ('device_id','hrm','date')

admin.site.register(device_data,device_dataAdmin)


