"""commed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

API_TITLE = "Commed Api"
API_DESCRIPTION = """ A REST API for using Commed"""
schema_view = get_schema_view(title=API_TITLE)

urlpatterns = [
    path('', lambda request: HttpResponse("Hello world!"), name="home"),
    path("admin/", admin.site.urls),
    path("docs/", include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)),
    path("user/", include("user.urls")),
    path("schema/", schema_view),
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path("enterprise/", include("enterprise.urls")),
    path("product/", include("product.urls"))
]