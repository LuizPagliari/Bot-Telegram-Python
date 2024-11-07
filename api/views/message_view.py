from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from api.models.message_model import Message
from api.services.message_service import create_message, get_message_by_id, update_message, delete_message, list_messages_paginated
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def message(request):
    return render(request, 'main/broadcasts/add.html')

@require_http_methods(["POST"])
def create_message_view(request):
    name = request.POST.get('name')
    description = request.POST.get('description')
    text = request.POST.get('text')
    message = create_message(name, description, text)
    return render(request, 'main/broadcasts/all.html', {'id': message.id, 'name': message.name, 'description': message.description, 'text': message.text})

@require_http_methods(["GET"])
def get_message_view(request, message_id):
    try:
        message = get_message_by_id(message_id)
        return JsonResponse({'id': message.id, 'name': message.name, 'description': message.description, 'text': message.text})
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)

@require_http_methods(["GET"])
def list_messages_view(request):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    
    messages = list_messages_paginated(page, page_size)
    messages_data = [{"id": message.id, "name": message.name, "description": message.description, "text": message.text} for message in messages]
    
    return JsonResponse({
        "messages": messages_data,
        "page": page,
        "page_size": page_size,
        "total": len(messages_data)
    }, safe=False)

@require_http_methods(["PUT"])
def update_message_view(request, message_id):
    name = request.PUT.get('name')
    description = request.PUT.get('description')
    text = request.PUT.get('text')
    try:
        message = update_message(message_id, name, description, text)
        return JsonResponse({'id': message.id, 'name': message.name, 'description': message.description, 'text': message.text})
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)

@require_http_methods(["DELETE"])
def delete_message_view(request, message_id):
    try:
        delete_message(message_id)
        return JsonResponse({'status': 'Message deleted'})
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Message not found'}, status=404)