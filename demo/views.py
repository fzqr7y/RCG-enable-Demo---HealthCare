from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Provider, Member
from .forms import PostForm, CommentForm

# http://stackoverflow.com/questions/5871730/need-a-minimal-django-file-upload-example
# https://github.com/axelpale/minimal-django-file-upload-example/blob/master/src/for_django_1-9/myproject/myproject/myapp/views.py
# from django.template import RequestContext
# from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse
# from .models import UserProfile
# from .forms import UserProfileForm

# Create your views here.


@login_required
def home(request):
    return render(request, 'demo/home.html', {})


@login_required
def members(request):
    members = Member.objects.all
    return render(request, 'demo/members.html', {'members': members})


@login_required
def providers(request):
    providers = Provider.objects.all
    return render(request, 'demo/providers.html', {'providers': providers})


@login_required
def member_detail(request, pk):
    # post = get_object_or_404(Comment, pk=pk)
    return render(request, 'demo/member_detail.html', {'comment': Comment})

# @login_required
# def member1_detail(request):
#     return render(request, 'demo/member1_detail.html', {})


def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(
        published_date__isnull=True).order_by('-created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


def post_detail(request, pk):
    # Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_new(request):
    # form = PostForm()
    # return render(request, 'blog/post_edit.html', {'form': form})
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
#             post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    # Post.objects.get(pk=pk)
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
#             post.published_date = timezone.now()
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog.views.post_detail', pk=pk)


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog.views.post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog.views.post_detail', pk=post_pk)


# @login_required
# def user_profile_upload(request):
#     # Handle file upload
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES)
#         if form.is_valid():
#             newdoc = UserProfile(picture=request.FILES['picture'])
#             newdoc.phone = form.cleaned_data["phone"]
#             newdoc.save()
#             # profile = Profile()
#             # profile.name = MyProfileForm.cleaned_data["name"]
#             # profile.picture = MyProfileForm.cleaned_data["picture"]
#             # profile.save()

#             # Redirect to the document list after POST
#             return HttpResponseRedirect(reverse('user_profile_upload'))
#     else:
#         form = UserProfileForm()  # A empty, unbound form

#     # Load documents for the list page
#     documents = UserProfile.objects.all()

#     # Render list page with the documents and the form
#     return render(
#         request, 'demo/user_profile_upload.html',
#         {'documents': documents, 'form': form}
#     )


# @login_required
# def user_profile_edit(request, pk):
#     profile = get_object_or_404(UserProfile, pk=pk)
#     # Handle file upload
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             profile.picture = request.FILES['picture']
#             profile.phone = form.cleaned_data["phone"]
#             profile.save()
#             # Redirect to the document list after POST
#             # return HttpResponseRedirect(reverse('user_profile_upload'))
#             return redirect('home')
#     else:
#         form = UserProfileForm()  # A empty, unbound form

#     # Load documents for the list page
#     documents = UserProfile.objects.all()

#     # Render list page with the documents and the form
#     return render(
#         request, 'demo/user_profile_upload.html',
#         {'documents': documents, 'form': form}
#     )

