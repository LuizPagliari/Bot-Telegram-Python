from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, render, redirect
from api.models.client_model import Client
from rest_framework.test import APIRequestFactory
from api.serializers.serializers import ClientSerializer
from django.http import JsonResponse
import json

@swagger_auto_schema(method='get', responses={200: ClientSerializer(many=True)})
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def list_clients_view(request):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    clients = Client.objects.all().order_by('id')
    paginator = Paginator(clients, page_size)
    try:
        clients_page = paginator.page(page)
    except PageNotAnInteger:
        clients_page = paginator.page(1)
    except EmptyPage:
        clients_page = paginator.page(paginator.num_pages)
    serializer = ClientSerializer(clients_page, many=True)
    return Response({
        "clients": serializer.data,
        "page": clients_page.number,
        "pages": paginator.num_pages,
        "has_next": clients_page.has_next(),
        "has_previous": clients_page.has_previous(),
    })
    
@login_required
def client_edit_page(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == 'POST':
        data = request.POST.copy()

        # Converte `is_active` para booleano explicitamente
        if 'is_active' in data:
            data['is_active'] = data['is_active'] == 'True'  # Força `True` ou `False`

        serializer = ClientSerializer(client, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            client.refresh_from_db()  # Verifica se as mudanças foram persistidas
            return redirect('clients')
        else:
            print("Erros de validação:", serializer.errors)  # Log para possível diagnóstico
    else:
        serializer = ClientSerializer(client)

    return render(request, 'main/clients/edit.html', {
        'client': client,
        'serializer': serializer,
        'isLoggedIn': request.user.is_authenticated,
    })

@login_required
def clients(request):
    # Create a factory request to call the API view
    factory = APIRequestFactory()
    api_request = factory.get('/clients/', request.GET)

    # Call the API view
    response = list_clients_view(api_request)

    # Extract the clients data from the response
    clients_list = response.data['clients']

    return render(request, 'main/clients/all.html', {
        'isLoggedIn': request.user.is_authenticated,
        'clients': clients_list,
    })
@swagger_auto_schema(method='get', responses={200: ClientSerializer()})
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_client_view(request, pk):
    client = get_object_or_404(Client, id=pk)
    serializer = ClientSerializer(client)
    return Response(serializer.data)

@swagger_auto_schema(method='post', request_body=ClientSerializer, responses={201: ClientSerializer()})
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_client_view(request):
    serializer = ClientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='post', request_body=ClientSerializer, responses={200: ClientSerializer()})
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def update_client_view(request, pk):
    client = get_object_or_404(Client, id=pk)
    data = request.data.copy()  # Copia os dados recebidos para modificá-los

    # Log dos dados recebidos
    print("Dados recebidos no servidor:", json.dumps(data))
    
    # Converte `is_active` para booleano
    if 'is_active' in data:
        data['is_active'] = data['is_active'] == '1'
    
    serializer = ClientSerializer(client, data=data, partial=True)
    
    if serializer.is_valid():
        print("Dados validados com sucesso:", serializer.validated_data)  # Log dos dados validados
        
        # Atualiza manualmente cada campo para garantir a persistência
        for field, value in serializer.validated_data.items():
            setattr(client, field, value)
        client.save()  # Salva as mudanças no banco de dados
        client.refresh_from_db()  # Recarrega para garantir a atualização
        
        print("Cliente atualizado com sucesso:", client)  # Log final do cliente atualizado
        return JsonResponse({"message": "Client updated successfully"}, status=200)
    else:
        print("Erros de validação:", serializer.errors)  # Log de erros de validação, se houver
        return JsonResponse(serializer.errors, status=400)
    
    
@swagger_auto_schema(method='delete', responses={204: 'No Content'})
@api_view(['DELETE'])
@permission_classes([permissions.AllowAny])
def delete_client_view(request, pk):
    client = get_object_or_404(Client, id=pk)
    client.delete()
    return Response({"message": "Client deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
