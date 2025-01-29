from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .forms import loginForm
from django.contrib.auth import views as auth_views
from .views import (index, 
                    full, 
                    buscar, 
                    Registro, 
                    CustomLoginView, 
                    solicitudes, 
                    solicitudes_2, 
                    success,copy, 
                    form_registro, 
                    success2,
                    full_solicitud, 
                    metricas, 
                    get_chart,
                    delete_form,
                    delete_form_solicitud,
                    delete_form_registro,
                    modify_form_registro,
                    update_registro)

urlpatterns = [
    path('', index, name='inicio'),
    path('busqueda/', full, name='full'), 
    path('buscar/', buscar, name='buscar'),
    path('solicitudes/', solicitudes, name='solicitudes'),   
    path('solicitud/', solicitudes_2, name='solicitudes_2'),
    path('success/', success, name='success'),
    path('success2/', success2, name='success2'),
    path('copy/', copy, name='copy'),
    path('registrar/', form_registro, name='registrar'),
    path('full_solicitud/', full_solicitud, name='full_solicitud'),
    path('metricas/', metricas, name='metricas'),
    path('get_chart/', get_chart, name="get_chart"),
    path('delete_form/', delete_form, name='delete_form'),
    path('delete_form_solicitud/', delete_form_solicitud, name='delete_form_solicitud'),
    path('delete_form_registro/', delete_form_registro, name='delete_form_registro'),
    path('modify_form_registro/', modify_form_registro, name='modify_form_registro'),
    path('update_registro/<int:id>/', update_registro, name='update_registro'),

    path('registro/', Registro.as_view(), name='registro'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='app/pages/login.html',authentication_form=loginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='app/pages/logout.html'), name='logout'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)