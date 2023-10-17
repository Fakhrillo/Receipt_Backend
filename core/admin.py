from django.contrib import admin
from .models import *
# Register your models here.
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'created_at', ]

class WorkerAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'branch', 'phone_number', 'id_tg',]
    list_display_links = ['name', 'branch', ]
    list_filter = ['branch']

class ChecksAdmin(admin.ModelAdmin):
    list_display = ['check_num', 'sum', 'worker', 'branch', 'date', 'image', 'issubmitted',]
    list_filter = ['worker']

class DocsAdmin(admin.ModelAdmin):
    list_display = ['doc_num', 'sum', 'worker', 'branch', 'date', 'image', 'issubmitted',]
    list_filter = ['worker']

admin.site.register(Branches, BranchAdmin)
admin.site.register(Workers, WorkerAdmin)
admin.site.register(Checks, ChecksAdmin)
admin.site.register(Docs, DocsAdmin)