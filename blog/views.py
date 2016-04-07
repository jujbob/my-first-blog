from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comment, SubComment
from blog.forms import PostForm, CommentForm, SubCommentForm
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, permissions
from blog.serializers import PostSerializer, CommentSerializer, SubCommentSerializer
from blog.permissions import IsOwnerOrReadOnly


def post_list(request):

    page_data = Paginator(Post.objects.all(), 5)
    page = request.GET.get('page')

    if page is None:
        page = 1

    try:
        posts = page_data.page(page)
    except PageNotAnInteger:
        posts = page_data.page(1)
    except EmptyPage:
        posts = page_data.page(page_data.num_pages)

    return render(request, 'blog/post_list.html', {'posts': posts, 'current_page': page, 'total_page': range(1, page_data.num_pages + 1)})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
#            post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def errors(request):
#    if request.GET.error_code == 1:

    return render(request, 'blog/errors/permission.html')
       # return HttpResponse("you don't have permission to edit")



@login_required
def post_edit(request, pk):

    # To check that the post is existing or not
    post = get_object_or_404(Post, pk=pk)

    # To check about user
    if request.user != post.author:
        return redirect('blog.views.errors')

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
#            post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog.views.post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # To check about user
    if request.user != post.author:
        return redirect('blog.views.errors')

    if post:
        post.delete()
    else:
        return redirect('blog.views.post_list')
    return redirect('blog.views.post_list')



### for Comment part
@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
        return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = CommentForm()
        return render(request, 'blog/add_comment_to_post.html', {'form': form})

#@login_required
#def comment_approve(request, pk):
#    comment = get_object_or_404(Comment, pk=pk)
#    comment.approve()
#    return redirect('blog.views.post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog.views.post_detail', pk=post_pk)

@login_required
def add_subComment_to_post(request, post_pk, comment_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == "POST":
        form = SubCommentForm(request.POST)
        if form.is_valid():
            subComment = form.save(commit=False)
            subComment.post = post
            subComment.comment = comment
            subComment.author = request.user
            subComment.save()
        return redirect('blog.views.post_detail', pk=post_pk)
    else:
        form = SubCommentForm()
        return render(request, 'blog/add_subComment_to_post.html', {'form': form})


### for rest framework api  ###

# APIs for reading and a set of Users
#class UserViewSet(viewsets.ModelViewSet):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

class SubCommentViewSet(viewsets.ModelViewSet):
    serializer_class = SubCommentSerializer
    queryset = SubComment.objects.all()