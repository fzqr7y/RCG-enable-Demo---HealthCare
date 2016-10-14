from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment
from .models import Provider, Member, Provider_Member, Message
from .models import County_Data, County_Widget
# , UserProfile
# from .models import Rx_Claim, Claim_Line
# from .forms import ProviderForm
from .forms import PostForm, CommentForm
# from .forms import MessageForm
from .forms import SmsForm, County_DataForm

# https://github.com/twilio/twilio-python
# pip install twilio
from twilio.rest import TwilioRestClient
import twilio.twiml
from django_twilio.decorators import twilio_view
import phonenumbers

# to get env vars
import os

# import the logging library
import logging
# import datetime
# from datetime import datetime

# serialize the request dict
import json
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
# from django.core.serializers import serialize

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
    if request.user.__class__.__name__ == 'User':
        user = request.user
    if user.userprofile.safe_provider:
        provider_id = user.userprofile.safe_provider()
    if provider_id:
        return redirect('member_map', pk=provider_id)
    return render(request, 'healthcare/big_data.html', {})


@login_required
def rcg(request):
    return render(request, 'healthcare/rcg.html', {})


@login_required
def big_data(request):
    return render(request, 'healthcare/big_data.html', {})


@login_required
def members(request):
    members = Member.objects.order_by('alert')
    return render(request, 'healthcare/members.html', {'members': members})


@login_required
def providers(request):
    providers = Provider.objects.all
    return render(request, 'healthcare/providers.html', {'providers': providers})


@login_required
def member_map_county(request, pk, template_name):
    provider = get_object_or_404(Provider, pk=pk)
    members = Member.objects.filter(provider_member__provider_id=pk)
    # logger.error(members.count())
    provider = get_object_or_404(Provider, pk=pk)
    logger.error(provider.id)
    if request.method == "POST":
        rdict = request.POST
        # response_data = {}
        # response_data['dict'] = rdict
        # respond_with = HttpResponse(
        #     json.dumps(response_data),
        #     content_type="application/json"
        # )
        # return respond_with
        state = rdict['state']
        county = rdict['county']
        logger.error(rdict)
        # return county_lookup(request)
    else:
        state = provider.state
        county = provider.county
    logger.error(state + " " + county)
    form = County_DataForm()
    behaviors = County_Widget.objects.filter(
        widget_name='Health Behaviors').values(
        'category', 'measure_name', 'description', 'val1_ref',
        'val2_ref', 'val1_type', 'us_str',
        'us_val', 'us_val_type').order_by('display_order')
    clinical = County_Widget.objects.filter(
        widget_name='Clinical Care').values(
        'category', 'measure_name', 'description', 'val1_ref',
        'val2_ref', 'val1_type', 'us_str',
        'us_val', 'us_val_type').order_by('display_order')
    county_data = County_Data.objects.filter(
        state=state, county=county).first()
    return render(request, template_name, {
        'provider': provider, 'form': form,
        'behaviors': behaviors, 'clinical': clinical,
        'county_data': county_data, 'members': members})




@login_required
def map_county(request, pk):
    provider = get_object_or_404(Provider, pk=pk)
    members = Member.objects.filter(provider_member__provider_id=pk)
    # logger.error(members.count())
    provider = get_object_or_404(Provider, pk=pk)
    logger.error(provider.id)
    if request.method == "POST":
        rdict = request.POST
        # response_data = {}
        # response_data['dict'] = rdict
        # respond_with = HttpResponse(
        #     json.dumps(response_data),
        #     content_type="application/json"
        # )
        # return respond_with
        state = rdict['state']
        county = rdict['county']
        logger.error(rdict)
        # return county_lookup(request)
    else:
        state = provider.state
        county = provider.county
    logger.error(state + " " + county)
    form = County_DataForm()
    behaviors = County_Widget.objects.filter(
        widget_name='Health Behaviors').values(
        'category', 'measure_name', 'description', 'val1_ref',
        'val2_ref', 'val1_type', 'us_str',
        'us_val', 'us_val_type').order_by('display_order')
    clinical = County_Widget.objects.filter(
        widget_name='Clinical Care').values(
        'category', 'measure_name', 'description', 'val1_ref',
        'val2_ref', 'val1_type', 'us_str',
        'us_val', 'us_val_type').order_by('display_order')
    county_data = County_Data.objects.filter(
        state=state, county=county).first()
    return render(request, 'healthcare/map_county.html', {
        'provider': provider, 'form': form,
        'behaviors': behaviors, 'clinical': clinical,
        'county_data': county_data, 'members': members})


@login_required
def member_map(request, pk):
    return member_map_county(request, pk, 'healthcare/member_map.html')


# @login_required
# def map_county2(request, pk):
#     provider = get_object_or_404(Provider, pk=pk)
#     members = Member.objects.filter(provider_member__provider_id=pk)
#     # logger.error(members.count())
#     return render(request, 'healthcare/map_county2.html', {
#         'provider': provider, 'members': members})


# @login_required
# def map_county3(request, pk):
#     provider = get_object_or_404(Provider, pk=pk)
#     members = Member.objects.filter(provider_member__provider_id=pk)
#     # logger.error(members.count())
#     return render(request, 'healthcare/map_county3.html', {
#         'provider': provider, 'members': members})


@login_required
def provider_members(request, pk):
    provider = get_object_or_404(Provider, pk=pk)
    logger.error(provider.id)
    members = Member.objects.filter(provider_member__provider_id=pk).values(
        'id', 'first_name', 'last_name', 'address', 'city', 'state', 'zip')
    serial_data = list(members)
    rdata = json.dumps(serial_data, cls=DjangoJSONEncoder)
    return HttpResponse(
        rdata,
        content_type="application/json"
    )


@login_required
def county_lookup(request):
    if request.method == "POST":
        state = request.POST['state']
        counties = County_Data.objects.filter(
            state=state).values_list(
            "county").distinct().order_by('county')
        rdata = json.dumps(list(counties), cls=DjangoJSONEncoder)
        # counties = County_Data.objects.filter(
        #     state=state).distinct().order_by('county')
        # rdata = serialize('json', counties, fields=('county', 'county'))
        return HttpResponse(
            rdata,
            content_type="application/json"
        )


# @login_required
# def county_data(request, pk):
#     provider = get_object_or_404(Provider, pk=pk)
#     members = Member.objects.filter(provider_member__provider_id=pk)
#     logger.error(provider.id)
#     if request.method == "POST":
#         rdict = request.POST
#         # response_data = {}
#         # response_data['dict'] = rdict
#         # respond_with = HttpResponse(
#         #     json.dumps(response_data),
#         #     content_type="application/json"
#         # )
#         # return respond_with
#         state = rdict['state']
#         county = rdict['county']
#         logger.error(rdict)
#         # return county_lookup(request)
#     else:
#         state = provider.state
#         county = provider.county
#     logger.error(state + " " + county)
#     form = County_DataForm()
#     behaviors = County_Widget.objects.filter(
#         widget_name='Health Behaviors').values(
#         'category', 'measure_name', 'description', 'val1_ref',
#         'val2_ref').order_by('display_order')
#     clinical = County_Widget.objects.filter(
#         widget_name='Clinical Care').values(
#         'category', 'measure_name', 'description', 'val1_ref',
#         'val2_ref').order_by('display_order')
#     county_data = County_Data.objects.filter(
#         state=state, county=county).first()
#     return render(request, 'healthcare/county_data.html', {
#         'provider': provider, 'form': form,
#         'behaviors': behaviors, 'clinical': clinical,
#         'county_data': county_data, 'members': members})


# @login_required
# def county_data2(request, pk):
#     provider = get_object_or_404(Provider, pk=pk)
#     logger.error(provider.id)
#     if request.method == "POST":
#         rdict = request.POST
#         # response_data = {}
#         # response_data['dict'] = rdict
#         # respond_with = HttpResponse(
#         #     json.dumps(response_data),
#         #     content_type="application/json"
#         # )
#         # return respond_with
#         state = rdict['state']
#         county = rdict['county']
#         logger.error(rdict)
#         # return county_lookup(request)
#     else:
#         state = provider.state
#         county = provider.county
#     logger.error(state + " " + county)
#     form = County_DataForm()
#     behaviors = County_Widget.objects.filter(
#         widget_name='Health Behaviors').values(
#         'category', 'measure_name', 'description', 'val1_ref',
#         'val2_ref').order_by('display_order')
#     clinical = County_Widget.objects.filter(
#         widget_name='Clinical Care').values(
#         'category', 'measure_name', 'description', 'val1_ref',
#         'val2_ref').order_by('display_order')
#     county_data = County_Data.objects.filter(
#         state=state, county=county).first()
#     return render(request, 'healthcare/county_data.html', {
#         'provider': provider, 'form': form,
#         'behaviors': behaviors, 'clinical': clinical,
#         'county_data': county_data})


@login_required
def member_detail_all(request, pk, template_name):
    member = get_object_or_404(Member, pk=pk)
    # providers = member.provider_set.order_by('id')
    # return render(request, 'healthcare/member_detail.html', {
    # 'member': member, 'providers': providers})
    provider_members = Provider_Member.objects.filter(member=member).order_by('id')
    # rx_claims = member.rx_claim_set.order_by('id')
    return render(request, template_name, {
        'member': member, 'provider_members': provider_members})


@login_required
def member_admin(request, pk):
    return member_detail_all(request, pk, 'healthcare/member_admin.html')


@login_required
def member_clinical(request, pk):
    return member_detail_all(request, pk, 'healthcare/member_clinical.html')


@login_required
def member_detail(request, pk):
    return member_detail_all(request, pk, 'healthcare/member_detail.html')


@login_required
def member_detail1(request, pk):
    member = get_object_or_404(Member, pk=pk)
    # providers = member.provider_set.order_by('id')
    # return render(request, 'healthcare/member_detail.html', {
    # 'member': member, 'providers': providers})
    provider_members = Provider_Member.objects.filter(member=member).order_by('id')
    return render(request, 'healthcare/member_detail1.html', {
        'member': member, 'provider_members': provider_members})


@login_required
def heartrate(request, pk):
    member = get_object_or_404(Member, pk=pk)
    # providers = member.provider_set.order_by('id')
    # return render(request, 'healthcare/member_detail.html', {
    # 'member': member, 'providers': providers})
    provider_members = Provider_Member.objects.filter(
        member=member).order_by('id')
    return render(request, 'healthcare/heartrate.html', {
        'member': member, 'provider_members': provider_members})


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
        from_parsed = phonenumbers.format_number(
            x, phonenumbers.PhoneNumberFormat.NATIONAL)
    except:
        from_parsed = message_from
    logger.error(rdict.get(
        'From', 'None') + " - " + message_from + " - " + from_parsed)
    sms.message_from = from_parsed
    message_to = rdict.get('To', '+18627728556')
    try:
        x = phonenumbers.parse(message_to, "US")
        to_parsed = phonenumbers.format_number(
            x, phonenumbers.PhoneNumberFormat.NATIONAL)
    except:
        to_parsed = message_to
    sms.message_to = to_parsed
    sms.text = rdict.get('Body', '-')
    sms.smssid = rdict.get('SmsSid')
    sms.smsstatus = rdict.get('SmsStatus')
    # This is the correct way to assign the member.
    # But for healthcare purposes we pick the last member this user messaged.
    member = Member.objects.filter(mobile_phone=from_parsed).first()
    if (member):
        logger.error("member: " + str(member.id))
    if (not(member) or member.id == 4):
        user_id = User.objects.filter(userprofile__mobile_phone=message_from).first()
        if (user_id):
            logger.error("user: " + str(user_id))
            last_sent = Message.objects.filter(
                user_id=user_id).order_by('-created_date').first()
            if (last_sent):
                member_id = last_sent.member_id
                logger.error("member2: " + str(member_id))
                member = Member.objects.get(pk=member_id)
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
    txt = "RCG Healthcare has received your message.  Thank you. "
    txt = txt + "A patient representative will respond as soon as possible."
    resp.message(txt)
    # return str(resp)
    # twiml = str(resp)
    # thanks to twilio_view don't have to do this:
    # return HttpResponse(resp, content_type='text/xml')
    # Can do this:
    return resp


@login_required
def sms(request, pk):
    member = get_object_or_404(Member, pk=pk)
    # user = request.user if (
    #     request.user.__class__.__name__ == 'User') else User.objects.order_by('id').first()
    user = request.user
    if request.method == "POST":
        form = SmsForm(request.POST)
        logger.error("posting text")
        logger.error(form.is_valid)
        if form.is_valid():
            account = os.environ.get('TWILIO_ACCOUNT_SID')
            token = os.environ.get('TWILIO_AUTH_TOKEN')
            sms = form.save(commit=False)
            sms.user = user
            sms.sent = True
            sms.message_type = 'SMS'
            # remove these from the form
            # force the message to go to the user
            sms.message_to = user.userprofile.mobile_phone
            sms.message_from = '+18627728556'
            sms.member_id = member.id
            text_body = "Message from RCG|enable™ Healthcare: " + sms.text

            client = TwilioRestClient(account, token)
            message = client.messages.create(
                # to=sms.message_to, from_="(862) 772-8556",
                # to=user.userprofile.mobile_phone, from_="+18627728556",
                # to="+19735688856", from_="+18627728556",
                to=sms.message_to, from_=sms.message_from,
                body=text_body)
            logger.error('Sent: ' + message.body + ' to: ' + str(
                message.to) + ' : ' + user.userprofile.mobile_phone)

            sms.save()
            return redirect('sms', pk=member.id)
    else:
        defaults = {
            # 'message_type': 'SMS', 'message_to': '+19735688856',
            'message_type': 'SMS', 'message_to': member.mobile_phone,
            # 'message_from': '+18627728556', 'member': member}
            'message_from': '(862) 772-8556', 'member': member}
        form = SmsForm(initial=defaults)
    # return render(request, 'blog/post_edit.html', {'form': form})
    # messages = Message.objects.filter(
    #     message_type='SMS').order_by('-created_date')
    # messages = member.smss
    return render(request, 'healthcare/sms.html', {
        'member': member,  # 'messages': messages,
        'form': form})


# @login_required
# def sms2(request):
#     if request.method == "POST":
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             sms = form.save(commit=False)
#             sms.user = request.user
#             sms.sent = True
#             sms.message_type = 'SMS'

#             account = os.environ.get('TWILIO_ACCOUNT_SID')
#             token = os.environ.get('TWILIO_AUTH_TOKEN')
#             client = TwilioRestClient(account, token)
#             message = client.messages.create(
#                 # to="+19735688856", from_="+18627728556",
#                 to=sms.message_to, from_="+18627728556",
#                 body=sms.text)
#             logger.error('Sent: ' + message.body + ' to: ' + message.to)

#             sms.save()
#             return redirect('sms')
#     else:
#         member = Member.objects.get(pk=4)
#         defaults = {
#             'message_type': 'SMS', 'message_to': '+19735688856',
#             'message_from': '+18627728556', 'member': member}
#         form = MessageForm(initial=defaults)
#     # return render(request, 'blog/post_edit.html', {'form': form})
#     messages = Message.objects.filter(
#         message_type='SMS').order_by('-created_date')
#     return render(request, 'healthcare/sms.html', {
#         'messages': messages, 'form': form})


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


def create_post(request):
    rdict = request.POST
    logger.error('Message received: ' + json.dumps(rdict.dict()))
    form = PostForm(request.POST)
    if form.is_valid():
        # logger.error('Form is valid')
        post = form.save(commit=False)
        if request.user.__class__.__name__ == 'User':
            user = request.user
        else:
            user = User.objects.order_by('id').first()
        # logger.error('User: ' + user.username)
        post.author = user
        # logger.error('Post Before: ' + str(post.id))
        post.save()
        # logger.error('Post after: ' + str(post.id))
        post.publish()
        logger.error('Post publish: ' + str(post.id))
        # return redirect('post_ajax')
    else:
        logger.error('Form NOT valid')
    return form, post


def post_ajax_create(request):
    if request.method == "POST":
        logger.error("post_ajax_create")
        form, post = create_post(request)
        if form.is_valid():
            # return redirect('post_ajax')
            response_data = {}
            response_data['result'] = 'Create post successful!'
            response_data['postpk'] = post.pk
            response_data['text'] = post.text
            response_data['created'] = post.published_date.strftime('%B %d, %Y %I:%M %p')
            response_data['author'] = post.author.username
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
    else:
        form = PostForm()
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'healthcare/post_ajax.html', {
        'form': form, 'posts': posts})


def post_ajax(request):
    logger.error("post_ajax")
    if request.method == "POST":
        form, post = create_post(request)
        if form.is_valid():
            logger.error("redirecting")
            return redirect('post_ajax_create')
    else:
        form = PostForm()
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'healthcare/post_ajax.html', {
        'form': form, 'posts': posts})


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
#         request, 'healthcare/user_profile_upload.html',
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
#         request, 'healthcare/user_profile_upload.html',
#         {'documents': documents, 'form': form}
#     )

