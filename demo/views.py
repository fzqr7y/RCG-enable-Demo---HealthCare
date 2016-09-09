from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment, Provider, Member, ProviderMember, Message
from .forms import PostForm, CommentForm, ProviderForm, MessageForm

# https://github.com/twilio/twilio-python
# pip install twilio
from twilio.rest import TwilioRestClient
import twilio.twiml
# from django.http import HttpResponse
from django_twilio.decorators import twilio_view
import phonenumbers

# import the logging library
import logging
# import datetime
# from datetime import datetime

# serialize the request dict
import json

# http://stackoverflow.com/questions/5871730/need-a-minimal-django-file-upload-example
# https://github.com/axelpale/minimal-django-file-upload-example/blob/master/src/for_django_1-9/myproject/myproject/myapp/views.py
# from django.template import RequestContext
# from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse
# from .models import UserProfile
# from .forms import UserProfileForm

# Create your views here.

# Get an instance of a logger
logger = logging.getLogger(__name__)


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
    member = get_object_or_404(Member, pk=pk)
    # providers = member.provider_set.order_by('id')
    # return render(request, 'demo/member_detail.html', {'member': member, 'providers': providers})
    providermembers = ProviderMember.objects.filter(member=member).order_by('id')
    return render(request, 'demo/member_detail.html', {
        'member': member, 'providermembers': providermembers})

# @login_required
# def member1_detail(request):
#     return render(request, 'demo/member1_detail.html', {})


# @login_required
@twilio_view
def receive_sms(request):
    # logger.error('dict: ' + request.GET.dict())
    if request.method == "POST":
        rdict = request.POST
    else:
        rdict = request.GET
    logger.info('Message received: ' + json.dumps(rdict.dict()))
    # logger.error('urlencode: ' + request.GET.urlencode())
    # for key, value in request.GET.items():
    #     logger.error("item: %s %s" % (key, value))
    # for key, value in request.GET.lists():
    #     logger.error("list: %s %s" % (key, value))
    # name = request.GET.get('name', None)
    # if not(name is None):
    #     logger.error('name: ' + name)
    # else:
    #     logger.error('no name')

    sms = Message()
    sms.message_type = 'SMS'
    sms.sent = False
    # sms.message_to = '+18627728556'
    # sms.message_from = "+19735688856"
    # now = datetime.now().strftime('%Y%m%d%H%M%S')
    # sms.text = 'test: ' + now
    # sms.query_url = request.GET.urlencode() + json.dumps(request.GET.dict())
    # member = Member.objects.get(pk=4)
    message_from = rdict.get('From', '+19735688856')
    try:
        x = phonenumbers.parse(message_from, "US")
        from_parsed = phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.NATIONAL)
    except:
        from_parsed = message_from
    sms.message_from = from_parsed
    message_to = rdict.get('To', '+18627728556')
    try:
        x = phonenumbers.parse(message_to, "US")
        to_parsed = phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.NATIONAL)
    except:
        to_parsed = message_to
    sms.message_to = to_parsed
    sms.text = rdict.get('Body', '-')
    sms.smssid = rdict.get('SmsSid')
    sms.smsstatus = rdict.get('SmsStatus')
    member = Member.objects.filter(mobile_phone=from_parsed).first()
    sms.member = member
    # logger.error('member: ' + str(sms.member_id))
    # logger.error('member: ' + sms.member.member_id)
    user = request.user if (
        request.user.__class__.__name__ == 'User') else User.objects.order_by('id').first()
    # logger.error('user: ' + user.__class__.__name__)
    # if user is None or not(user.__class__.__name__ == 'User'):
    #     user = User.objects.get(pk=1)
    sms.user = user
    # logger.error('user: ' + str(sms.user_id))
    sms.data = json.dumps(rdict.dict())

    sms.save()

    # return redirect('sms')
    """Respond to incoming calls with a simple text message."""
    resp = twilio.twiml.Response()
    resp.message("RCG has received your message.  Thank you. A patient representative will respond as soon as possible.")
    # return str(resp)
    # twiml = str(resp)
    # thanks to twilio_view don't have to do this:
    # return HttpResponse(resp, content_type='text/xml')
    # Can do this:
    return resp


@login_required
def sms(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            sms = form.save(commit=False)
            sms.user = request.user
            sms.sent = True
            sms.message_type = 'SMS'

            account = "AC652bccbad1784e6130f04ccadb530a04"
            token = "cec870e047ecc5e604c4596fd56f89c6"
            client = TwilioRestClient(account, token)
            message = client.messages.create(
                # to="+19735688856", from_="+18627728556",
                to=sms.message_to, from_="+18627728556",
                body=sms.text)
            logger.error('Sent: ' + message.body + ' to: ' + message.to)

            sms.save()
            return redirect('sms')
    else:
        member = Member.objects.get(pk=4)
        defaults = {
            'message_type': 'SMS', 'message_to': '+19735688856',
            'message_from': '+18627728556', 'member': member}
        form = MessageForm(initial=defaults)
    # return render(request, 'blog/post_edit.html', {'form': form})
    messages = Message.objects.filter(message_type='SMS').order_by('-created_date')
    return render(request, 'demo/sms.html', {
        'messages': messages, 'form': form})


@login_required
def provider_edit(request, pk):
    # Post.objects.get(pk=pk)
    # post = get_object_or_404(Post, pk=pk)
    provider = get_object_or_404(Provider, pk=pk)
    if request.method == "POST":
        form = ProviderForm(request.POST, instance=provider)
        if form.is_valid():
            provider = form.save(commit=False)
            # post.author = request.user
#             post.published_date = timezone.now()
            provider.save()

            # from_number = request.values.get('From', None)
            name = request.POST.get('name', None)
            # Log an error message
            logger.error('name: ' + name)
            # account = "AC652bccbad1784e6130f04ccadb530a04"
            # token = "cec870e047ecc5e604c4596fd56f89c6"
            # client = TwilioRestClient(account, token)
            # message = client.messages.create(
            #     to="+19735688856", from_="+18627728556",
            #     body=provider.description)
            # # body="Hello World!")
            # logger.error('Sent: ' + message.body + ' to: ' + message.to)

            return redirect('providers')
    else:
        # logger.error('dict: ' + request.GET.dict())
        rdict = request.GET.dict()
        logger.error('dict: ' + json.dumps(rdict))
        logger.error('urlencode: ' + request.GET.urlencode())
        for key, value in request.GET.items():
            logger.error("item: %s %s" % (key, value))
        for key, value in request.GET.lists():
            logger.error("list: %s %s" % (key, value))
        name = request.GET.get('name', None)
        if not(name is None):
            logger.error('name: ' + name)
        else:
            logger.error('no name')

        form = ProviderForm(instance=provider)
    return render(request, 'demo/provider_edit.html', {'form': form})


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

