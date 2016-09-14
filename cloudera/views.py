from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import logging
import json
from django.http import HttpResponse
# from django.core.serializers.json import DjangoJSONEncoder

# cloudera
from impala.dbapi import connect

# from .models import IntradayData

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
