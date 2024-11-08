from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from api.models.category_model import Category
from api.serializers.serializers import CategorySerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from api.models.user_model import User
from api.services.user_service import UserService

@login_required
def categories(request):
    user_service = UserService()
    list_categories = Category.objects.all()
    user_data = user_service.get_user_by_id(request.user.id)
    return render(request, 'main/categories/all.html', {
        'categories': list_categories,
        'isLoggedIn': request.user.is_authenticated,
    })

@swagger_auto_schema(method='get', responses={200: CategorySerializer(many=True)})
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def list_categories(request):
    page = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 10)
    categories = Category.objects.all().order_by('id')
    paginator = Paginator(categories, per_page)
    try:
        categories_page = paginator.page(page)
    except PageNotAnInteger:
        categories_page = paginator.page(1)
    except EmptyPage:
        categories_page = paginator.page(paginator.num_pages)
    serializer = CategorySerializer(categories_page, many=True)
    return Response({
        "categories": serializer.data,
        "page": categories_page.number,
        "pages": paginator.num_pages,
        "has_next": categories_page.has_next(),
        "has_previous": categories_page.has_previous(),
    })

@swagger_auto_schema(method='get', responses={200: CategorySerializer()})
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_category_by_id(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    except ObjectDoesNotExist:
        return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(method='post', request_body=CategorySerializer, responses={201: CategorySerializer()})
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='put', request_body=CategorySerializer, responses={200: CategorySerializer()})
@api_view(['PUT'])
@permission_classes([permissions.AllowAny])
def update_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ObjectDoesNotExist:
        return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(method='delete', responses={204: 'No Content'})
@api_view(['DELETE'])
@permission_classes([permissions.AllowAny])
def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        return Response({"message": "Category deleted."}, status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
    