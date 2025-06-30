"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

# myproject/urls.py
# myproject/urls.py
from django.contrib import admin
from django.urls import path
from myapp  import views
from myapp.views import index, send_email, verify_otp  # Importing views directly

urlpatterns = [
    path('', views.index, name='index'),
    path('send_email/', views.send_email, name='send_email'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),  # Add name here
]