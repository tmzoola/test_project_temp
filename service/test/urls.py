from django.urls import path
from .import views

urlpatterns = [
    path('statistics/employee/<int:id>/', views.employee_stats, name='employee_stats'),
    path('statistics/client/<int:client_id>/', views.ClientStatisticsView.as_view(), name='client_stats'),
    path('employee/statistics/', views.EmployeeStatisticsView.as_view(), name='all_employee_stats'),

]