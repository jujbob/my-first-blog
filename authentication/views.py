from authentication.forms import AccountForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import permissions, viewsets, status

from authentication.models import Account
from authentication.permissions import IsAccountOwner
from authentication.serializers import AccountSerializer
from rest_framework.response import Response

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash



def login_view(request):
    return render(request, 'blog/login_view.html')

def logout_user(request):
    logout(request)
    return redirect('blog.views.post_list')

def login_user(request):
    logout(request)
    email = password = ''
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        print(email)
        print(password)

        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                print("login success")

            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This authentication has been disabled.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            if request.user.is_active:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'Username/password combination invalid.'
                }, status=status.HTTP_401_UNAUTHORIZED)

    return redirect('blog.views.post_list')

def sign_up(request):

    if request.method =='POST':
        form = AccountForm()
        return HttpResponse("here is a test")
    else:
        form = AccountForm()
        return render(request, 'blog/sign_up.html', {'form': form})



#for restframework
class AccountViewSet(viewsets.ModelViewSet):
#    lookup_field = 'username'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), IsAccountOwner(),)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            Account.objects.create_user(**serializer.validated_data)

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Account could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

