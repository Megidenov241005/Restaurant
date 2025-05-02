from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *


urlpatterns = [
    path('', main_view, name = 'main'),
    path('tables/', edit_tables, name='edit_tables'),
    path('tables/add/', add_table, name='add_table'),
    path('tables/delete/<int:table_id>/', delete_table, name='delete_table'),
    path('tables/edit/<int:table_id>/', edit_table, name='edit_table'),
    path('reserve/time/', choose_time, name='reserve_table'),
    path('reserve/final/', finalize_reserve, name='finalize_reserve'),
    path('logout', logout_view, name = 'logout'),
    path('login', login_view, name = 'login'),
    path('register/', register_view, name = 'register'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)