from django.shortcuts import render
# get_object_or_404
# from django.utils import timezone
# from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User

# from demo.models import Member
from .models import IntradayData

import logging
import json
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

# for env vars
from os import environ

# http://pdwhomeautomation.blogspot.co.uk/2016/01/fitbit-api-access-using-oauth20-and.html
import base64
# import urllib2
import urllib

# Get an instance of a logger
logger = logging.getLogger(__name__)


@login_required
def home(request):
    return render(request, 'fitbit/home.html', {})


@login_required
def get_heartrate(request):
    response_data = {}
    response_data['message'] = 'No Data'
    respond_with = HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )
    if request.method == "POST" and request.is_ajax():
        rdict = request.POST
    elif request.method == "GET":
        rdict = request.GET
    else:
        return respond_with

    response_data['dict'] = rdict
    respond_with = HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )
    if not('member_id' in rdict and 'from' in rdict and 'to' in rdict):
        return respond_with

    # logger.error('urlencode: ' + request.GET.urlencode())

    # member = Member.objects.get(id=rdict['member_id'])
    member_id = rdict['member_id']
    query_min = rdict['from']
    query_max = rdict['to']
    api_data = IntradayData.objects.filter(
        # record_date__range=["2016-09-11 20:00:00", "2016-09-12 00:00:00"],
        # record_date__range=["2016-09-10T20:00:00.000Z", "2016-09-12T20:00:00.000Z"],
        record_date__range=[query_min, query_max],
        member_id=member_id).values('record_date', 'value').order_by('record_date')
    # member=member).values('record_date', 'value'
    serial_data = list(api_data)

    # user = request.user if (
    #     request.user.__class__.__name__ == 'User') else User.objects.order_by('id').first()
    # response_data['serial_data'] = serial_data
    # # response_data['api_data'] = api_data.first().id
    # response_data['api_data'] = api_data.first()['value']
    # response_data['member'] = member.id
    # response_data['user'] = user.id
    # response_data['message'] = 'Heartrate Data'
    # response_data['data'] = [50, 60, 70]
    # response_data['dict'] = rdict
    # rdata = json.dumps(response_data, cls=DjangoJSONEncoder)
    rdata = json.dumps(serial_data, cls=DjangoJSONEncoder)
    return HttpResponse(
        rdata,
        content_type="application/json"
    )


@login_required
def callback(request):
    response_data = {}
    response_data['message'] = 'No Data'
    respond_with = HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )
    if request.method == "POST":
        rdict = request.POST
    elif request.method == "GET":
        rdict = request.GET
    else:
        return respond_with

    response_data['message'] = 'OK'
    response_data['dict'] = rdict
    respond_with = HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )
    return respond_with


@login_required
def get_access(request):

    # These are the secrets etc from Fitbit developer
    OAuthTwoClientID = environ.get('FITBIT_CLIENT_ID')
    ClientOrConsumerSecret = environ.get('FITBIT_CLIENT_SECRET')

    # This is the Fitbit URL
    TokenURL = "https://api.fitbit.com/oauth2/token"

    # I got this from the first verifier part when authorising my application
    # Have to get this within 10 minutes of running this view
    AuthCode = "9ca29f04ada8604193799fc33f13eac728c6b560"

    # Form the data payload
    BodyText = {'code': AuthCode,
                # 'redirect_uri': 'http://pdwhomeautomation.blogspot.co.uk/',
                'redirect_uri': 'http://127.0.0.1/fitbit/callback/',
                'client_id': OAuthTwoClientID,
                'grant_type': 'authorization_code'}

    BodyURLEncoded = urllib.parse.urlencode(BodyText)
    print(BodyURLEncoded)

    # Start the request
    # req = urllib.request.Request(TokenURL, BodyURLEncoded)
    binary_data = BodyURLEncoded.encode('utf8')
    req = urllib.request.Request(TokenURL, binary_data)
    # req = request.Request(TokenURL, binary_data)
    # Add the headers, first we base64 encode the client id
    # and client secret with a : inbetween and create the authorisation header
    # req.add_header('Authorization', 'Basic ' + base64.b64encode(
    # OAuthTwoClientID + ":" + ClientOrConsumerSecret))
    b = bytes(OAuthTwoClientID + ":" + ClientOrConsumerSecret, 'utf8')
    bb = base64.b64encode(b)
    # req.add_header('Authorization', bb.decode('utf-8'))
    req.add_header('Authorization', 'Basic ' + bb.decode('utf-8'))
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')

    # response_data = {}

    # Fire off the request
    try:
        response = urllib.request.urlopen(req)
        FullResponse = response.read()
        print("Output >>> " + FullResponse)
        # response_data['message'] = 'success'
        # response_data['FullResponse'] = FullResponse
        response_text = 'success: ' + FullResponse
        # response_text = 'success: '
    except urllib.error.URLError as e:
        print(e.code)
        print(e.read())
        # response_data['message'] = 'error'
        # response_data['FullResponse'] = e.read()
        # response_text = 'Error: ' + e.read()
        response_text = 'Error: '

    respond_with = HttpResponse(
        response_text,
        content_type="text/plain"
    )
    return respond_with
