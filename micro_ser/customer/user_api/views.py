from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email', '')
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username exists'}, status=400)
            
        user = User.objects.create_user(username=username, password=password, email=email)
        return JsonResponse({'message': 'User created', 'id': user.id})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            # Trong thực tế sẽ trả về Token (JWT), ở đây demo ta trả về ID để Cart Service dùng
            return JsonResponse({'message': 'Login successful', 'user_id': user.id, 'username': user.username})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

def get_user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        return JsonResponse({'id': user.id, 'username': user.username, 'email': user.email})
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)