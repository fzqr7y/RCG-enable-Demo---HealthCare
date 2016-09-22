from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import logging
import json
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

import calendar
import dateutil.parser
# import time
import datetime
# for env vars
from os import environ
# cloudera
from impala.dbapi import connect

from fitbit.models import IntradayData

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.


@login_required
def home(request):
    return render(request, 'cloudera/home.html', {})


@login_required
def impyla(request):
    conn = connect(host='quickstart.cloudera', port=21050)
    cursor = conn.cursor()
    # cursor.execute('SELECT * FROM categories LIMIT 100')
    cursor.execute('SELECT * FROM fitbit_intradaydata LIMIT 100')
    print(cursor.description)  # prints the result set's schema
    results = cursor.fetchall()

    jresults = json.dumps(results)
    return HttpResponse(
        jresults,
        content_type="application/json"
    )


@login_required
def get_heartrate(request):
    use_cloudera = environ.get('CLOUDERA')
    print(use_cloudera)
    if (use_cloudera == 'TRUE'):
        print('cloudera')
        return get_cloudera_heartrate(request)
    else:
        print('fitbit')
        return get_pg_heartrate(request)


@login_required
def get_pg_heartrate(request):
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

    logger.error('urlencode: ' + request.GET.urlencode())

    # member = Member.objects.get(id=rdict['member_id'])
    member_id = rdict['member_id']
    query_min = rdict['from']
    query_max = rdict['to']
    today = datetime.date.today()
    delta = (today - datetime.date(2016, 9, 16)).days
    qmin_dt = dateutil.parser.parse(query_min)
    qmax_dt = dateutil.parser.parse(query_max)
    logger.error(str(delta) + " " + str(qmax_dt) + " " + str(qmin_dt))
    qmin_adj = qmin_dt - datetime.timedelta(days=delta)
    qmax_adj = qmax_dt - datetime.timedelta(days=delta)
    logger.error(str(delta) + " " + str(qmax_adj) + " " + str(qmin_adj))

    api_data = IntradayData.objects.filter(
        # record_date__range=["2016-09-11 20:00:00", "2016-09-12 00:00:00"],
        # record_date__range=["2016-09-10T20:00:00.000Z",
        # "2016-09-12T20:00:00.000Z"],
        # record_date__range=[query_min, query_max],
        record_date__range=[qmin_adj, qmax_adj],
        member_id=member_id).values('record_date', 'value').order_by(
            'record_date')

    logger.error(api_data.count())
    logger.error(json.dumps(rdict))

    # serial_data = list(api_data)
    # rdata = json.dumps(serial_data, cls=DjangoJSONEncoder)

    rlist = []
    for item in api_data:
        t = item['record_date']
        t = t + datetime.timedelta(days=delta)
        # tt = (time.mktime(t.timetuple()) - (5 * 3600)) * 1000
        tz = calendar.timegm(t.timetuple()) * 1000
        v = item['value']
        # rlist.append(['{:.0f}'.format(tt), '{:.1f}'.format(v)])
        rlist.append([int(tz), float(v), t.isoformat()])
    # print(rlist)
    jresults = json.dumps(rlist)  # , cls=DjangoJSONEncoder)

    return HttpResponse(
        jresults,
        # rdata,
        content_type="application/json"
    )


@login_required
def get_cloudera_heartrate(request):
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
    logger.error('from: ' + query_min)
    # logger.error('from2: ' + time.mktime(query_min))
    max_time = dateutil.parser.parse(query_max)
    # logger.error('to: ' + time.mktime(max_time))
    max_jsts = round(max_time.timestamp() * 1000)
    min_time = dateutil.parser.parse(query_min)
    min_jsts = round(min_time.timestamp() * 1000)
    logger.error('from: ' + '{:d}'.format(min_jsts))
    logger.error('to: ' + '{:d}'.format(max_jsts))
    # conn = connect(host='quickstart.cloudera', port=21050)
    host = environ.get('CLOUDERA_HOST')
    port = int(float(environ.get('CLOUDERA_PORT')))
    # logger.error(host)
    # logger.error(port)
    conn = connect(host=host, port=port)
    cursor = conn.cursor()

    # now = datetime.datetime.now()
    # logger.error(now)
    # logger.error(now.timestamp())
    # select = "select (cast(now() - interval 1 minute as bigint)
    # * 1000) - min(record_date) as diff from fitbit_intradaydata"
    # cursor.execute(select)
    # print(cursor.description)  # prints the result set's schema
    # results = cursor.fetchall()
    # diff = results[0][0] + (4 * 3600 * 1000)
    # print("-" + '{:d}'.format(diff))
    # my_tuple = ('world', '.')
    # "Hello {}{}".format(*my_tuple)
    # my_dict = {'subs': 'world', 'period': '.'}
    # "Hello {subs}{period}".format(**my_dict)
    # cursor.execute('SELECT * FROM categories LIMIT 100')
    # stmt = "SELECT record_date, value FROM fitbit_intradaydata LIMIT 100"
    # my_dict = {'member_id': member_id, 'max_jsts': max_jsts}
    # where2 = "and record_date < {max_jsts} ".format(**my_dict)
    # select = "SELECT record_date, value "
    select = "SELECT unix_timestamp(cast(record_date "
    select = select + "as timestamp))*1000, value "
    # test_date = "(id + cast(now() + interval 4 hour - interval
    # 1 minute as bigint)) * 1000 "
    # test_date = "record_date + {diff}".format(**{'diff': diff})
    # test_select = "SELECT " + test_date + ", value "
    # from_clause = "FROM fitbit_intradaydata "
    # from_clause = "FROM fitbit2 "
    from_clause = "FROM fitbit3 "
    where1 = "where member_id = {mem_id} ".format(**{'mem_id': member_id})
    # where2 = "and record_date > {min_jsts} ".format(**{'min_jsts': min_jsts})
    # where3 = "and record_date < {max_jsts} ".format(**{'max_jsts': max_jsts})
    wstr2 = "and cast(record_date as timestamp) "
    wstr2 = wstr2 + "> cast('{query_min}' as timestamp) "
    where2 = wstr2.format(**{'query_min': query_min})
    # where3 = "and record_date < {query_max} "
    # .format(**{'query_max': query_max})
    wstr3 = "and cast(record_date as timestamp) "
    wstr3 = wstr3 + "<= cast('{query_max}' as timestamp) "
    # where3 = "and cast(record_date as timestamp) < cast('{query_max}'
    # as timestamp) ".format(**{'query_max': query_max})
    where3 = wstr3.format(**{'query_max': query_max})
    where = where1 + where2 + where3
    # where = where1
    # test_where2 = "and record_date > 1473796199000 "
    # test_where3 = "and record_date < 1473796211000 "
    # test_where = where1  # + test_where2 + test_where3
    order_by = "order by record_date "
    limit = ""
    # limit = "LIMIT 100"
    # stmt_dict = {'select': select, 'where': where, 'limit': limit}
    # stmt = "{select} {where} {limit}".format(**stmt_dict)
    stmt = select + from_clause + where + order_by + limit
    # test_stmt = test_select + from_clause + test_where + order_by + limit
    logger.error("live: " + stmt)
    # logger.error("test: " + test_stmt)
    cursor.execute(stmt)
    # cursor.execute(test_stmt)
    # print(cursor.description)  # prints the result set's schema
    results = cursor.fetchall()
    # row = [item for item in results]
    # print(row)

    jresults = json.dumps(results)
    return HttpResponse(
        jresults,
        content_type="application/json"
    )


@login_required
def get_heartrate_save(request):
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
    # logger.error('from: ' + query_min)
    # logger.error('from2: ' + time.mktime(query_min))
    max_time = dateutil.parser.parse(query_max)
    # logger.error('to: ' + time.mktime(max_time))
    max_jsts = round(max_time.timestamp() * 1000)
    min_time = dateutil.parser.parse(query_min)
    min_jsts = round(min_time.timestamp() * 1000)
    logger.error('from: ' + '{:d}'.format(min_jsts))
    logger.error('to: ' + '{:d}'.format(max_jsts))
    # conn = connect(host='quickstart.cloudera', port=21050)
    host = environ.get('CLOUDERA_HOST')
    port = int(float(environ.get('CLOUDERA_PORT')))
    # logger.error(host)
    # logger.error(port)
    conn = connect(host=host, port=port)
    cursor = conn.cursor()

    # now = datetime.datetime.now()
    # logger.error(now)
    # logger.error(now.timestamp())
    # select = "select (cast(now() - interval 1 minute as bigint) * 1000)"
    #  - min(record_date) as diff from fitbit_intradaydata"
    # cursor.execute(select)
    # print(cursor.description)  # prints the result set's schema
    # results = cursor.fetchall()
    # diff = results[0][0] + (4 * 3600 * 1000)
    # print("-" + '{:d}'.format(diff))
    # my_tuple = ('world', '.')
    # "Hello {}{}".format(*my_tuple)
    # my_dict = {'subs': 'world', 'period': '.'}
    # "Hello {subs}{period}".format(**my_dict)
    # cursor.execute('SELECT * FROM categories LIMIT 100')
    # stmt = "SELECT record_date, value FROM fitbit_intradaydata LIMIT 100"
    # my_dict = {'member_id': member_id, 'max_jsts': max_jsts}
    # where2 = "and record_date < {max_jsts} ".format(**my_dict)
    select = "SELECT record_date, value "
    # test_date = "(id + cast(now() + interval 4 hour - interval
    # 1 minute as bigint)) * 1000 "
    # test_date = "record_date + {diff}".format(**{'diff': diff})
    # test_select = "SELECT " + test_date + ", value "
    # from_clause = "FROM fitbit_intradaydata "
    # from_clause = "FROM fitbit2 "
    from_clause = "FROM fitbit "
    where1 = "where member_id = {mem_id} ".format(**{'mem_id': member_id})
    where2 = "and record_date > {min_jsts} ".format(**{'min_jsts': min_jsts})
    where3 = "and record_date < {max_jsts} ".format(**{'max_jsts': max_jsts})
    where = where1 + where2 + where3
    # test_where2 = "and record_date > 1473796199000 "
    # test_where3 = "and record_date < 1473796211000 "
    # test_where = where1  # + test_where2 + test_where3
    order_by = "order by record_date "
    # limit = "LIMIT 100"
    limit = ""
    # stmt_dict = {'select': select, 'where': where, 'limit': limit}
    # stmt = "{select} {where} {limit}".format(**stmt_dict)
    stmt = select + from_clause + where + order_by + limit
    # test_stmt = test_select + from_clause + test_where + order_by + limit
    logger.error("live: " + stmt)
    # logger.error("test: " + test_stmt)
    cursor.execute(stmt)
    # cursor.execute(test_stmt)
    # print(cursor.description)  # prints the result set's schema
    results = cursor.fetchall()
    # row = [item for item in results]
    # print(row)

    jresults = json.dumps(results)
    return HttpResponse(
        jresults,
        content_type="application/json"
    )


@login_required
def get_heartrate_orig(request):
    conn = connect(host='quickstart.cloudera', port=21050)
    cursor = conn.cursor()
    # cursor.execute('SELECT * FROM categories LIMIT 100')
    cursor.execute('SELECT * FROM fitbit_intradaydata LIMIT 100')
    print(cursor.description)  # prints the result set's schema
    results = cursor.fetchall()

    jresults = json.dumps(results)
    return HttpResponse(
        jresults,
        content_type="application/json"
    )
