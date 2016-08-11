from authentication.forms import AccountForm, AccountFormDetail, UserImageForm
from blog.models import Post
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.transaction import commit
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import permissions, viewsets, status

from authentication.models import Account, UserImage
from authentication.permissions import IsAccountOwner
from authentication.serializers import AccountSerializer
from rest_framework.response import Response

from django.contrib.auth import authenticate, login, logout



def login_view(request):
    return render(request, 'blog/login_view.html')

def profile(request, pk):

#    return render(request, 'blog/profile.html')
    page = request.GET.get('page')
    author = get_object_or_404(Account, pk=pk)
    page_data = Paginator(Post.objects.filter(author=author).order_by('-created_date'), 10)

    if page is None:
        page = 1
    else:
        page = int(page)

    try:
        posts = page_data.page(page)
    except PageNotAnInteger:
        posts = page_data.page(1)
    except EmptyPage:
        posts = page_data.page(page_data.num_pages)

    for post in posts:
        if len(post.text) > 300:
            post.text = post.text[1:300] + "..... 더보기(more)"

    return render(request, 'blog/profile.html', {'posts': posts, 'author': author, 'current_page': page, 'total_page': range(1, page_data.num_pages + 1)})

@login_required
def profile_edit(request):

    user = get_object_or_404(Account, pk=request.user.pk)
    if request.method == 'POST':
        accountForm = AccountFormDetail(request.POST, instance=request.user)
        print(accountForm.content)
        print(accountForm.content)
        print(accountForm.content)
        print(accountForm.content)
        print(accountForm.content)
        userImageForm = UserImageForm(request.POST, request.FILES)
        if accountForm.is_valid() and userImageForm.is_valid():
            user = accountForm.save(commit=False)
            userImage = userImageForm.save(commit=False)
            user.save()
            if 'user_image' in request.FILES:
                userImage.user_image = request.FILES['user_image']
                userImage.user = request.user
                userImage.save()
#                photo = UserImage(user=user, image_file=request.FILES['user_image'])
            print("save user")
            return redirect('authentication.views.profile', pk=request.user.pk)
        else:
            return render(request, "blog/profile_edit.html", {'accountForm': accountForm, 'userImageFrom': userImageForm, })

    elif request.method == 'GET':
        accountForm = AccountFormDetail(instance=request.user)
        userImageForm = UserImageForm(request.POST, request.FILES)
    return render(request, "blog/profile_edit.html", {'accountForm': accountForm, 'userImageFrom': userImageForm, })


#    for image in request.FILES.getlist("images", []):
#        photo = Resource(post=post, image_file=image)
#        photo.save()


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

    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            #user = form.save(commit=False)
            #user.email = form.cleaned_data['email']
            #user.save()
            return render(request, 'blog/sign_up_ok.html')

    elif request.method == "GET":
        form = AccountForm()

    return render(request, "blog/sign_up.html", {"form": form,})

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

