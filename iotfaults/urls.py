"""django_iot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from . import views
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# View sets for Django REST Framework
router = routers.DefaultRouter()
router.register(r'types', views.TypeViewSet)
router.register(r'components', views.ComponentViewSet)
router.register(r'events', views.EventViewSet)

# Schema view for 
# drf-yasg (Django REST Framework - Yet another Swagger generator)
schema_view = get_schema_view(
   openapi.Info(
      title="Iot Faults API",
      default_version='v1',
      description="Iot Faults API",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    
    
    ## RENDERS
    
    # General index. Real Time Graphics
    url(r'^$', views.index, name='index'),
    
    # Show all data in Events table
    url(r'^event-detail/(?P<id>\d+)/$', views.event_detail, name='event_detail'),
    
    # Show Real Time Graphs
    url(r'^real-time$', views.real_time, name='real_time'),
    
    # Show Analytics Graphs
    url(r'^analytics$', views.analytics, name='analytics'),
    
    # Show Analytics Graphs
    url(r'^node-failure-simulator$', views.node_failure_simulator, name='node_failure_simulator'),

    # Show Analytics Graphs
    url(r'^out-of-range-simulator$', views.out_of_range_simulator, name='out_of_range_simulator'),
    
    ## DATA
    
    # Get data of Fault types since start date to end date
    url(r'^data/fault-types/count/start/(?P<str_start_date>[^/]+)/end/(?P<str_end_date>[^/]+)$', views.json_fault_types_count_between, name='json_fault_types_count_between'),

    # Get data of Components with Faults since start date to end date
    url(r'^data/components/count/start/(?P<str_start_date>[^/]+)/end/(?P<str_end_date>[^/]+)$', views.json_components_count_between, name='json_components_count_between'),
    
    # Get data of Components with Faults last quantity of time
    url(r'^data/components/count/quantity/(?P<str_quantity>[^/]+)/date-type/(?P<str_date_type>[^/]+)$', views.json_components_count_last, name='json_components_count_last'),
    
    # Get data of Components with Location with Faults last quantity of time
    url(r'^data/components/detail/count/quantity/(?P<str_quantity>[^/]+)/date-type/(?P<str_date_type>[^/]+)$', views.json_components_detail_count_last, name='json_components_detail_count_last'),
    
    
    ## Django REST Frame work
    
    # Api Root
    url(r'^api/', include(router.urls)),
    
    ## drf-yasg (Django REST Framework - Yet another Swagger generator)
    
    # A JSON view of your API specification at /swagger.json
    # A YAML view of your API specification at /swagger.yaml
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # A swagger-ui view of your API specification at /swagger/
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # A ReDoc view of your API specification at /redoc/
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
]
