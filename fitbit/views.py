from django.shortcuts import render
# get_object_or_404
# from django.utils import timezone
# from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User

from demo.models import Member
from .models import IntradayData

import logging
import json
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.

# Get an instance of a logger
logger = logging.getLogger(__name__)


# class MyJsonEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, decimal.Decimal):
#             return float(o)
#         if isinstance(o, datetime):
#             return o.isoformat()
#         super(MyJsonEncoder, self).default(o)


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

    member = Member.objects.get(id=rdict['member_id'])
    api_data = IntradayData.objects.filter(
        record_date__range=["2016-09-11 00:00:00", "2016-09-12 00:00:00"], member=member).values('record_date', 'value')
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
