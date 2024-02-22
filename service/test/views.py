from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Employee,Client,Order
from rest_framework.views import APIView
from rest_framework.response import Response



def employee_stats(request, id):
    month = request.GET.get('month')
    year = request.GET.get('year')

    employee = get_object_or_404(Employee, id=id)
    statistics = employee.get_statistics(month, year)
    return JsonResponse(statistics)


class ClientStatisticsView(APIView):
    def get(self, request, client_id):
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            raise Http404("Client does not exist")

        orders = Order.objects.filter(client=client, date__month=month, date__year=year)
        products = sum(order.products.count() for order in orders)
        sales = sum(order.price for order in orders)

        client_data = {
            'client_id': client.id,
            'full_name': client.full_name,
            'employee': {
                'employee_id': client.employee.id,
                'employee_full_name': client.employee.full_name,
            },
            'products': products,
            'sales': sales
        }

        return Response(client_data)

class EmployeeStatisticsView(APIView):
    def get(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        employees = Employee.objects.all()
        statistics = []

        for employee in employees:
            orders = Order.objects.filter(employee=employee, date__month=month, date__year=year)
            products = sum(order.products.count() for order in orders)
            sales = sum(order.price for order in orders)

            employee_data = {
                'employee_id': employee.id,
                'full_name': employee.full_name,
                'clients': orders.values('client').distinct().count(),
                'products': products,
                'sales': sales
            }

            statistics.append(employee_data)

        return Response(statistics)