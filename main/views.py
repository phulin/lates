from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.template import RequestContext
from lates.main.models import Late
import datetime, json

def todays_lates():
    return Late.objects.filter(request_date=datetime.date.today()).order_by('id');

def request_late(request):
    late = Late(name=request.POST['name'], refrigerated=request.POST.get('refrigerated', False))
    late.save()

    subject = request.POST['name'] + ' wants a late.'
    message = 'Late please!'
    from_addr = 'Auto-Late <phulin@mit.edu>'
    to_addrs = ['tepco@mit.edu']
    # send_mail(subject, message, from_addr, to_addrs, fail_silently=False)

    return HttpResponse(json.dumps(late.to_dict()))

def index(request):
    context = {'today' : datetime.date.today(), 'todays_lates' : todays_lates()}
    return render_to_response('index.html', context,
                              context_instance=RequestContext(request))

def make_json(request):
    return HttpResponse(json.dumps([late.to_dict() for late in todays_lates()]))

def cancel(request, id):
    result = {'success' : False}
    if request.method != 'DELETE':
        return HttpResponse(status=501)

    try:
        late = Late.objects.get(id=int(id))
        late.delete()
    except e:
        result['error'] = str(e)
        return HttpResponse(json.dumps(result))

    result['success'] = True
    return HttpResponse(json.dumps(result))
