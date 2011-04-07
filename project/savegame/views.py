from django.template import Context, loader
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello World")

def settings(request):
    t = loader.get_template('account/settings.html')
    c = Context({})
    return HttpResponse(t.render(c))

def signIn(request):
    signInTemplate = loader.get_template('account/signIn.html')
    signInContext = Context({})
    return HttpResponse(signInTemplate.render(signInContext))

def signOut(request):
    signOutTemplate = loader.get_template('account/signOut.html')
    signOutContext = Context({})
    return HttpResponse(signOutTemplate.render(signOutContext))