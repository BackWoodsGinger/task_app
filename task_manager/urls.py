from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from tasks import views as task_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')),
    path('', task_views.home, name='home'), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)