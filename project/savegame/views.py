from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
# Additional imports
from savegameforms import RegForm
import string

def mainpage(request):
	#Will try to use Django forms later. Search redirects to /resultspage
	#May need to handle CSRF cookies later
	#If AJAX/JQuery is used: http://docs.djangoproject.com/en/dev/ref/contrib/csrf/
	#latest_ten = savefiles.objects.all().order_by('datetime-uploaded')[:10]
	logged_in = False
	t = loader.get_template('account/mainpage.html')
	c = RequestContext(request, {'logged_in': logged_in})
	if request.user.is_authenticated():
		logged_in = True;
		fullname = request.user.get_full_name()
		if request.user.is_staff:
			fullname = request.user.username
		c = RequestContext(request, {'logged_in': logged_in, 'fullname': string.capwords(fullname)})
	return HttpResponse(t.render(c))


def regpage(request):
	#Currently Django wipes out the cleaned_data dictionary if any validation errors are raised
	if (request.method == 'POST'):
		reg = RegForm(request.POST)
		if reg.is_valid():
			un = reg.cleaned_data['username']
			pwd = reg.cleaned_data['password']
			email = reg.cleaned_data['email']

			msg = "Thank you for registering at Save-Game! \n Your username is: " + un
			sub = "Welcome to Save-Game!"
			send_mail(sub, msg, 'noreplysavegame@gmail.com', [str(email)])

			newacc = User.objects.create_user(un, email, pwd)
			newacc.first_name = un
			newacc.save()
			return HttpResponseRedirect('thanks/')
	else:
		reg = RegForm()

	t = loader.get_template('account/regpage.html')
	c = RequestContext(request, {'regform': reg})
	return HttpResponse(t.render(c))


def regthanks(request):
	t = loader.get_template('account/regthanks.html')
	c = Context({})
	return HttpResponse(t.render(c))


def settings(request):
	t = loader.get_template('account/settings.html')
	c = Context({})
	return HttpResponse(t.render(c))


def signIn(request):
	signInTemplate = loader.get_template('account/signIn.html')
	if request.user.is_authenticated():
		# Case: User is already logged in.
		signInContext = Context({"logInMessage": "You are already signed in."})
		return HttpResponse(signInTemplate.render(signInContext))
	else:
		# Case: User is NOT logged in yet.
		try:
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)

			if user is not None:
				if user.is_active:
					# Case: Credentials verified (access granted).
					login(request, user)
					signInContext = RequestContext(
							{"logInMessage": "You have been signed in successfully."})
					return HttpResponse(signInTemplate.render(signInContext))
				else:
					# Case: User account disabled.
					signInContext = Context({"logInMessage": "Your account has been "\
															 "disabled.", 'notLoggedIn': 'TRUE'})
					return HttpResponse(signInTemplate.render(signInContext))
			else:
				# Case: Invalid credentials.
				signInContext = Context({"logInMessage": "Invalid Username or Password: "\
														 "Please check your credentials.",
										 'notLoggedIn': 'TRUE'})
				return HttpResponse(signInTemplate.render(signInContext))
		except:
			# Case: Default page with the sign-in form - user is NOT logged in yet.
			signInContext = Context({"notLoggedIn": "TRUE"})
			return HttpResponse(signInTemplate.render(signInContext))


def signOut(request):
	logout(request)
	signOutTemplate = loader.get_template('account/signOut.html')
	signOutContext = Context({})
	return HttpResponse(signOutTemplate.render(signOutContext))


def gamepage(request):
	t = loader.get_template('gamepage/index.html')
	c = Context({})
	return HttpResponse(t.render(c))


def results(request):
	c = Context({})
	t = loader.get_template('results/index.html')
	return HttpResponse(t.render(c))