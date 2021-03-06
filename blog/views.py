
# coding: utf-8
import PIL
from PIL import Image
from django.core.checks import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comment, SubComment, Resource
from blog.forms import PostForm, CommentForm, SubCommentForm, ResourceForm
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.defaultfilters import pprint
from rest_framework import viewsets, permissions
from blog.serializers import PostSerializer, CommentSerializer, SubCommentSerializer
from blog.permissions import IsOwnerOrReadOnly


def post_list(request):

    category = request.GET.get('category')
    page = request.GET.get('page')
    if category == "my_post":
        page_data = Paginator(Post.objects.filter(author=request.user).order_by('-created_date'), 10)
    elif category == "news_feed":
        page_data = Paginator(Post.objects.order_by('-created_date'), 10)
    else:
        page_data = Paginator(Post.objects.order_by('-created_date'), 10)

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

    return render(request, 'blog/post_list.html', {'posts': posts, 'current_page': page, 'category': category, 'total_page': range(1, page_data.num_pages + 1)})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})

'''
def image_resizing(image):

    basewidth = 70
    img = Image.open(image)
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)

    return img
'''

@login_required
def post_new(request):

#    ImageFormSet = modelformset_factory(Resource, form=ResourceForm, extra=3)

    if request.method == "POST":
        postForm = PostForm(request.POST)
        formset = ResourceForm(request.POST, request.FILES)
        if postForm.is_valid():
            post = postForm.save(commit=False)
            post.author = request.user
            post.save()
            for image in request.FILES.getlist("images", []):
 #               img = image_resizing(image)
                photo = Resource(post=post, image_file=image)
                photo.save()
            return redirect('blog.views.post_detail', pk=post.pk)
        #        for form in formset.cleaned_data:
        #            image = form['image_file']
        #            photo = Resource(post=post, image_file=image)
        #            photo.save()

    else:
        postForm = PostForm()
        formset = ResourceForm()
        return render(request, 'blog/post_edit.html', {'postForm': postForm, 'formset': formset}, context_instance=RequestContext(request))
"""
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        resourceForm = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            resource = resourceForm.save()
            #resource = resourceForm.save(commit=False)
            resource.post = post
            resource.save()
        return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
        resourceForm = ResourceForm()
    return render(request, 'blog/post_edit.html', {'form': form, 'resourceForm': resourceForm})
"""


def errors(request):
#    if request.GET.error_code == 1:

    return render(request, 'blog/errors/permission.html')
       # return HttpResponse("you don't have permission to edit")



@login_required
def post_edit(request, pk):

    # To check that the post is existing or not
    post = get_object_or_404(Post, pk=pk)
#    post = Post.objects.get(pk=pk)
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
            if request.FILES.getlist("images", []):
                for resource in post.resources.all():
                    resource.delete()
                for image in request.FILES.getlist("images", []):
                    photo = Resource(post=post, image_file=image)
                    photo.save()
                return redirect('blog.views.post_detail', pk=post.pk)
            else:
                return redirect('blog.views.post_detail', pk=post.pk)
    else:
        postForm = PostForm(instance=post)
        formset = ResourceForm(instance=post)
    return render(request, 'blog/post_edit.html', {'postForm': postForm, 'formset': formset}, context_instance=RequestContext(request))

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

@login_required
def subComment_remove(request, pk):
    subComment = get_object_or_404(SubComment, pk=pk)
    post_pk = subComment.post.pk
    subComment.delete()
    return redirect('blog.views.post_detail', pk=post_pk)




def resource_detail(request, pk):
    image = get_object_or_404(Resource, pk=pk)
    message = '<p>포스트번호:{0}, img:{1}</p> <img src={1}></img>'.format(image.post_id, image.image_file.url)
    return HttpResponse(message)

def resource_new(request):
    if request.method == "GET":
        edit_form = ResourceForm()
        pprint('hewefre')
    elif request.method == "POST":
        pprint('heeeeeeewre')
        edit_form = ResourceForm(request.POST, request.FILES)

        if edit_form.is_valid():
            new_photo = edit_form.save()

            return redirect(new_photo.get_absolute_url())

    return render(
        request,
        'blog/resource_new.html',
        {
            'form': edit_form,
        }
    )

def resource_edit(request, pk):
    return HttpResponse("notting")







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