from django.template import Context, loader
from django.http import HttpResponse

def index(request):

    return HttpResponse("Hello World")

def settings(request):
    t = loader.get_template('account/settings.html')
    c = Context({})
    return HttpResponse(t.render(c))
