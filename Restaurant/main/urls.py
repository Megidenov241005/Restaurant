from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *


urlpatterns = [
    path('', main, name = 'main'),
    path('reserve/time/', choose_time, name='reserve_table'),
    path('reserve/final/', finalize_reserve, name='finalize_reserve'),
    # path('my_reserves', my_reserves, name = 'my_reserves'),
    path('logout', logout_view, name = 'logout'),
    path('login', login_view, name = 'login'),
    path('register/', register_view, name = 'register'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)