from django.template import Context, RequestContext, loader
from django.http import HttpResponse
from savegame.models import User
#from savegame.models import savefiles

def mainpage(request):
	#Will try to use Django forms later. Search redirects to /resultspage
	#May need to handle CSFRF cookies later
	#If AJAX/JQuery is used: http://docs.djangoproject.com/en/dev/ref/contrib/csrf/
	
	#latest_ten = savefiles.objects.all().order_by('datetime-uploaded')[:10]
	t = loader.get_template('account/mainpage.html')
	logged_in = False
	if request.user.is_authenticated():
		logged_in = True;
	c = RequestContext(request, {'logged_in':logged_in})
	return HttpResponse(t.render(c))

def regpage(request):
	t = loader.get_template('account/regpage.html')
	c = Context({})
	return HttpResponse(t.render(c))

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


def gamepage(request):
    t = loader.get_template('gamepage/index.html')
    c = Context({})
    return HttpResponse(t.render(c))
