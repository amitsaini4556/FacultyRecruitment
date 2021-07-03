from django.urls import path
from django.conf.urls import handler404
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	path('',views.jobs,name='jobs'),
	path('addJob/', views.addJob, name="addJob"),
	path('applyJob/<int:id>', views.applyJob, name="applyJob"),
	path('jobDetails/<int:id>', views.showJobDetails, name = "jobDetails"),
	path('dashboard/', views.dashboard, name = 'dashboard'),
	path('updateStatus/<int:applicatId>/<int:jobId>/<str:type>', views.updateStatus, name = 'updateStatus'),
	path('download/<int:applicatId>/<int:jobId>', views.download, name = 'download'),
	path('updateJob/<int:jobId>', views.updateJob, name = 'updateJob'),
	path('deleteJob/<int:jobId>', views.deleteJob, name = 'deleteJob'),
	path('search', views.search, name = 'search'),
	path('reminder/<int:applicatId>/<int:jobId>', views.reminder, name = 'reminder'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
