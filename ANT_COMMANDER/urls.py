from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    re_path("^(?!admin)(?!api)(?!static).*$", TemplateView.as_view(template_name='index.html')),
]
