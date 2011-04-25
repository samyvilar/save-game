from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
# Additional imports
from savegameforms import RegForm
import string

from savegame.forms import *

from savegame.models import *
from django.core import serializers
from django.shortcuts import render_to_response, redirect

import os

import json

from datetime import datetime


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

def profile(request, user_id = None):    
    if user_id == None or User.objects.filter(pk = user_id).count() == 0:
        return redirect('/invalid_user_id/') # if supplied an invalid user id    
    elif request.user.is_authenticated() and request.user.id == int(user_id): # users profile ...                    
        user            = User.objects.get(id = user_id)
        profile         = user.get_profile()
        uploadsavegames = UploadedGame.objects.filter(user = user)
        form            = UploadGameForm()
        comments        = Comments.objects.filter(user = user)
        owner           = True

        if request.method == "POST":            
            user.first_name     = request.POST['first_name']
            user.last_name      = request.POST['last_name']
            user.username       = request.POST['username']
            user.set_password(request.POST['password'])
            user.email          = request.POST['email']

            user.save()
            
            if 'avatar' in request.FILES:
                file = request.FILES['avatar']
                try:
                    os.remove(os.getcwd() + '/savegame/' + profile.avatar.name)
                except Exception:
                    pass
                filename = 'static/images/' + getRandomString() + '.' + file.name.split('.')[-1:][0]                
                destination = open('savegame/' + filename, 'wb')
                for chunk in file.chunks():
                    destination.write(chunk)
                destination.close()
                profile.avatar.name = filename

            if 'private' in request.POST:
                profile.private = request.POST['private']
            profile.save()

            if request.is_ajax():                                  
                return HttpResponse(serializers.serialize('json', [user, profile]) ,
                                    mimetype = 'application/json')
                
            
                

        context = {'user':user,
                   'profile':profile,
                   'uploadsavegames':uploadsavegames,
                   'form':form,
                   'comments':comments,
                   'owner':owner}

        return render_to_response('account/profile.html',
                                   context,
                                   context_instance=RequestContext(request))
    elif User.objects.get(pk = user_id).get_profile().private: # if profile is private ..
        return redirect('/private_profile/')
    else: # public profile viewed by anyone ...
        user        = User.objects.get(id = user_id)
        profile     = user.get_profile()
        uploadsavegames = UploadedGame.objects.filter(user = user, private = False)
        comments        = Comments.objects.filter(user = user)
        
        context = {'user':user, 'profile':profile, 'uploadsavegames':uploadsavegames, 'comments':comments}

        return render_to_response('account/profile.html',
                                   context,
                                   context_instance=RequestContext(request))



def getUploadedFileData(request):

   
    info = {}    

    try:
        user_id = request.GET['user_id']
        uploaded_id = request.GET['uploaded_game_id']

    except:
        return HttpResponse("Error retrieving uploaded file data!");


    # Get stuff off the data base and pass it back to the client!

    info['data_title'] = "f.zip"
    info['date'] = '1/2/2222' #UploadedGame.objects.filter(user=user_id, id=uploaded_id).values()[0]['datetime']
    info['uploader'] = User.objects.filter(id=user_id).values()[0].get('username')
    info['profile_path'] = '/'+UserProfile.objects.filter(user=user_id).values()[0].get('avatar')
    info['download_link'] =  UploadedGame.objects.filter(user=user_id, id=uploaded_id).values()[0]['file']
    info['game_desc'] = UploadedGame.objects.filter(user=3, id=17).values()[0]['description']
    
    
    res = Comments.objects.filter(uploadedgame=uploaded_id).order_by('id').values()
    info2 = {}
    for i in res:
        i['datetime'] = ''  #this is a hack because datetime result is not serializable
        info2[i['id']] = i

    info['info2'] = info2;

    return HttpResponse(json.dumps(info))


def getCommentData(request):

    
    try:
        user_id = request.GET['user_id']   # This should be the currently logged in user
        uploaded_id = request.GET['uploaded_game_id']
        comment_data = request.GET['comment_data']

    except:
        return HttpResponse("Error retrieving uploaded file data for comments!");


    # Put the comment in the database now
    now = datetime.now()    
    date = str(now.month) + '/' + str(now.day) + '/' + str(now.year)
    print date

    entry = Comments()

    uploaded = UploadedGame(id=17)
    user = User(id=3)

    entry.uploadedgame = uploaded
    entry.user         = user
    entry.comment      = str(comment_data)
    entry.datetime     = now

    entry.save()
    
    res = Comments.objects.filter(uploadedgame=17).values()
    info = {}
    

    # Just get the last comment, and then return it
    info['only'] = Comments.objects.filter(uploadedgame=17).values()[len(Comments.objects.filter(uploadedgame=17).values()) - 1]
    info['only']['datetime'] = ''

    return HttpResponse(json.dumps(info))

