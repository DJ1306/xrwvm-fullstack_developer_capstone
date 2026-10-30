from django.contrib import admin
from django.urls import path,re_path,include
from django.views.generic import TemplateView
urlpatterns=[
 path("admin/",admin.site.urls),
 path("djangoapp/",include("djangoapp.urls")),
 path("about",TemplateView.as_view(template_name="About.html")),
 path("contact",TemplateView.as_view(template_name="Contact.html")),
 re_path(r"^(?:|dealers/?|dealer/[0-9]+/?|postreview/[0-9]+/?|login/?|register/?)$",TemplateView.as_view(template_name="index.html")),
]
