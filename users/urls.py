from django.urls import path
from users.views import user_list, user_ranking, user_detail, dashboard

app_name = 'users'

urlpatterns = [
    path('', user_list, name='user_list'),
    path('ranking/', user_ranking, name='ranking'),
    path('dashboard/', dashboard, name='dashboard'),
    path('<str:email>/', user_detail, name='user_detail'),
]
