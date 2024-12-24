from django.contrib import admin
from django.urls import path
from home import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('uploadfile/',views.uploadfile,name='uploadfile'),               
    path('deletefile/<int:id>',views.deletefile),       
    path('delete/',views.delete_all,name='deleteall'),  
    path('success.html',views.success,name='success')     
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)