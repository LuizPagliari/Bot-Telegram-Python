from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from api.models.order_model import Order
from api.serializers.serializers import OrderSerializer
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

@login_required
@swagger_auto_schema(method='get', responses={200: OrderSerializer(many=True)})
@api_view(['GET'])
def orders(request):
    list_orders_view = Order.objects.all()
    return render(request, 'main/orders/all.html', {
        'orders': list_orders_view,
        'isLoggedIn': request.user.is_authenticated,
    })

@swagger_auto_schema(method='get', responses={200: OrderSerializer(many=True)})
@api_view(['GET'])
def list_orders_view(request):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    orders = Order.objects.all().order_by('id')
    paginator = Paginator(orders, page_size)
    try:
        orders_page = paginator.page(page)
    except PageNotAnInteger:
        orders_page = paginator.page(1)
    except EmptyPage:
        orders_page = paginator.page(paginator.num_pages)
        
    serializer = OrderSerializer(orders_page, many=True)
    return Response({
        "orders": serializer.data,
        "page": orders_page.number,
        "pages": paginator.num_pages,
        "has_next": orders_page.has_next(),
        "has_previous": orders_page.has_previous(),
    })

@swagger_auto_schema(method='get', responses={200: OrderSerializer()})
@api_view(['GET'])
def get_order_view(request, pk=None):
    order = get_object_or_404(Order, pk=pk)
    serializer = OrderSerializer(order)
    return Response(serializer.data)

@swagger_auto_schema(method='post', request_body=OrderSerializer, responses={201: OrderSerializer(), 400: 'Bad Request'})
@api_view(['POST'])
def create_order_view(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='put', request_body=OrderSerializer,responses={200: OrderSerializer(), 400: 'Bad Request'})
@swagger_auto_schema(method='patch', request_body=OrderSerializer, responses={200: OrderSerializer(), 400: 'Bad Request'})
@api_view(['PUT', 'PATCH'])
def update_order_view(request, pk=None):
    order = get_object_or_404(Order, pk=pk)
    serializer = OrderSerializer(order, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='delete', responses={204: 'No Content', 400: 'Bad Request', 404: 'Not Found'})
@api_view(['DELETE', 'POST'])  # Suporta DELETE e POST para simular DELETE
@permission_classes([IsAuthenticated])
def delete_order_view(request, pk=None):
    """
    Deleta um pedido pelo ID.
    """
    if request.method == 'POST' and request.POST.get('_method') == 'DELETE':
        order = get_object_or_404(Order, pk=pk)
        try:
            order.delete()
            messages.success(request, 'Order deleted successfully.')
            return redirect('orders')
        except Exception as e:
            messages.error(request, f'Failed to delete order: {str(e)}')
            return redirect('orders')
    messages.error(request, 'Invalid request method.')
    return redirect('orders')


def orders_kanban_view(request):
    orders_by_status = {
        'new': Order.objects.filter(status=Order.Status.NEW),
        'in_process': Order.objects.filter(status=Order.Status.IN_PROCESS),
        'sent': Order.objects.filter(status=Order.Status.SENT),
        'delivered': Order.objects.filter(status=Order.Status.DELIVERED),
    }
    return render(request, 'main/orders/kanban.html', {'orders_by_status': orders_by_status})

@login_required
def edit_order_page(request, pk=None):
    """
    Renderiza a página de edição de um pedido existente.
    """
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        serializer = OrderSerializer(order, data=request.POST, partial=True)
        if serializer.is_valid():
            serializer.save()
            return redirect('orders')
    else:
        serializer = OrderSerializer(order)
    status_choices = Order.Status.choices

    return render(request, 'main/orders/edit.html', {
        'order': order,
        'serializer': serializer,
        'status_choices': status_choices,  
        'isLoggedIn': request.user.is_authenticated,
    })