"""sweclub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.swehome, name='swehome')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='swehome')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from account.views import StudentSignUpView
from django.contrib import admin
from swehome.views import SearchView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('swehome.urls')),
                  path('blood-donate/', include('blood_donation.urls')),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('accounts/signup/', StudentSignUpView.as_view(), name='signup'),
                  path('account/', include('account.urls')),
                  path('search/', SearchView.as_view(), name='search'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Software Engineering Club Administration'
admin.site.site_title = 'SWE CLUB'
