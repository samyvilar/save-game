from django.template import Context, RequestContext, loader
from django.http import HttpResponse
#from savegame.models import savefiles

def mainpage(request):
	#Will try to use Django forms later. Search redirects to /resultspage
	#May need to handle CSFRF cookies later
	#If AJAX/JQuery is used: http://docs.djangoproject.com/en/dev/ref/contrib/csrf/
	
	#latest_ten = savefiles.objects.all().order_by('datetime-uploaded')[:10]
	if request.user.is_authenticated():
		t = loader.get_template('mainpage/mainpage.html')
	else:
		t = loader.get_template('mainpage/mainpageguest.html')
	c = RequestContext(request, {})
	return HttpResponse(t.render(c))

#TEMPORARY VIEW to just see the logged in version of the page. mainpage func should work 
#correctly once log in system is in place.
def mainpageauth(request):
	t = loader.get_template('mainpage/mainpage.html')
	c = RequestContext(request, {})
	return HttpResponse(t.render(c))
#END TEMPORARY VIEW


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
