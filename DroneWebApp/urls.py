from django.contrib import admin
from django.urls import path
from Drone.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('droneadmin/', droneadmin, name='droneadmin'),
    path('admin-data/',admin_page_data, name = 'admin_page_data'),
    path('droneadmin/details/<int:details_id>',victim_page, name = 'victim_page'),
    path('droneadmin/victim-details/<int:details_id>',victim_details, name = 'victim_details'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
