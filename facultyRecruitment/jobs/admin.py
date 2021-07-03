from django.contrib import admin
from django.utils.html import format_html

from . import models

class JobsAdmin(admin.ModelAdmin):
	list_display = ("position",)

class ApplicantsAdmin(admin.ModelAdmin):
	list_display = ("name",)

class CollegeImagesAdmin(admin.ModelAdmin):
    list_display=['collegeName','image_display']
    def image_display(self, obj):
        return format_html('<img src="/media/{0}" style="width: 100px; \
                           height: 100px"/>'.format(obj.image))
    image_display.short_descripition = "image_display"

class ReminderAdmin(admin.ModelAdmin):
	list_display = ('userId','jobId')


admin.site.register(models.Jobs, JobsAdmin)
admin.site.register(models.Applicants, ApplicantsAdmin)
admin.site.register(models.CollegeImages,CollegeImagesAdmin)
admin.site.register(models.Reminder,ReminderAdmin)
