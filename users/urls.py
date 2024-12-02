from django.urls import path
from .views import register,success_view,login_view,fleet_manager_home_view,driver_home_view,introduction_to_ev,dataset,distribution,relationship,vehicle_status,prediction_view,relationship_view,home_view,predict_range,predict_electric_range,relationship_analysis,custom_logout_view

urlpatterns = [
    path("", home_view, name="home"),
    path("register/", register, name='register'),
    path('success/', success_view, name='success_url'),  # Success URL
    path('login/', login_view, name='login'),
    # Define other URLs for fleet manager and driver pages
    path('fleet_manager_home/', fleet_manager_home_view, name='fleet_manager_home'),
    path('driver_home/', driver_home_view, name='driver_home'),
    #Fleet Manager Dashboard
    path('introduction_to_ev/', introduction_to_ev, name='introduction_to_ev'),
    path('dataset/', dataset, name='dataset'),
    path('distribution/', distribution, name='distribution'),
    path('relationship/', relationship, name='relationship'),
    path('vehicle_status/', vehicle_status, name='vehicle_status'),
    path('prediction/', prediction_view, name='prediction'),
    path('relationship/', relationship_view, name='relationship'),
    path('predict/', predict_electric_range, name='predict_electric_range'),
    path('predict_range/',predict_range, name='predict_range'),
    path('relationship_analysis/', relationship_analysis, name='relationship_analysis'),
    path("logout/", custom_logout_view, name="logout")

]

