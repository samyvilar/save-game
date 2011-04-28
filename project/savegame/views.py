from django.template import Context, RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
# Additional imports
import string
from savegame.forms import *
from savegame.models import *
from savegame.helpers import levenshtein
from django.core import serializers
from django.shortcuts import render_to_response, redirect
import os
import json
from datetime import datetime
from project.savegame.models import *

def mainpage(request):
    latest_ten = UploadedGame.objects.all().exclude(private=True).order_by('-datetime')[:10]
    loggedin = False
    fullname = ""
    t = loader.get_template('account/mainpage.html')
    if request.user.is_authenticated():
        loggedin = True;
        fullname = request.user.get_full_name()
    c = Context({'logged_in': loggedin, 'fullname': string.capwords(fullname),
                 'user_id': request.user.id, 'latest_ten': latest_ten})
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
    loggedin = False
    fullname = ""
    if request.user.is_authenticated():
        loggedin = True;
        fullname = request.user.get_full_name()
    t = loader.get_template('account/settings.html')
    c = Context({'logged_in': loggedin, 'user_id': request.user.id,
                 'fullname': string.capwords(fullname)})
    return HttpResponse(t.render(c))


def signIn(request):
    loggedin = False
    fullname = ""
    signInTemplate = loader.get_template('account/signIn.html')
    id = request.user.id
    if request.user.is_authenticated():
        # Case: User is already logged in.
        loggedin = True;
        fullname = request.user.get_full_name()
        signInContext = Context(
                {'logged_in': loggedin, 'fullname': string.capwords(fullname), 'user_id': id,
                 "logInMessage": "You are already signed in."})
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
                    return redirect('/')
                else:
                    # Case: User account disabled.
                    signInContext = Context(
                            {'logged_in': loggedin, 'fullname': fullname, 'user_id': id,
                             "logInMessage": "Your account has been disabled.",
                             'notLoggedIn': 'TRUE'})
                    return HttpResponse(signInTemplate.render(signInContext))
            else:
                # Case: Invalid credentials.
                signInContext = Context({
                    "logInMessage": "Invalid Username or Password: Please check your credentials.",
                    'notLoggedIn': 'TRUE', 'logged_in': loggedin, 'user_id': id,
                    'fullname': fullname})
                return HttpResponse(signInTemplate.render(signInContext))
        except:
            # Case: Default page with the sign-in form - user is NOT logged in yet.
            signInContext = Context({'logged_in': loggedin, 'fullname': fullname, 'user_id': id,
                                     "notLoggedIn": "TRUE"})
            return HttpResponse(signInTemplate.render(signInContext))


def signOut(request):
    logout(request)
    loggedin = False
    fullname = ""
    signOutTemplate = loader.get_template('account/signOut.html')
    signOutContext = Context(
            {'logged_in': loggedin, 'fullname': fullname, 'user_id': request.user.id})
    return HttpResponse(signOutTemplate.render(signOutContext))


def gamepage(request):
    loggedin = False
    fullname = ""
    if request.user.is_authenticated():
        loggedin = True;
        fullname = request.user.get_full_name()
    t = loader.get_template('gamepage/index.html')
    c = Context({'logged_in': loggedin, 'fullname': fullname, 'user_id': request.user.id})
    return HttpResponse(t.render(c))


def results(request):
    fullname = ""
    pglst = []
    e1, e2, loggedin = False, False, False
    if request.user.is_authenticated():
        loggedin = True;
        fullname = request.user.get_full_name()
    t = loader.get_template('results/index.html')
    search_res = {}
    qry = request.GET.get('search', '')
    if qry:
        s1 = UploadedGame.objects.filter(game__title__iexact=qry)
        s2 = UploadedGame.objects.filter(file__iexact='saved-file.bin')
        s3 = UploadedGame.objects.filter(user__username__iexact=qry)
        s4 = UploadedGame.objects.filter(description__iexact=qry)
        if not s1.exists():
            s1 = UploadedGame.objects.filter(game__title__icontains=qry)
        if not s2.exists():
            s2 = UploadedGame.objects.filter(file__icontains='static/saved_games/' + qry)
        if not s3.exists():
            s3 = UploadedGame.objects.filter(user__username__icontains=qry)
        if not s4.exists():
            s4 = UploadedGame.objects.filter(description__icontains=qry)

        search_res = (s1 | s2 | s3 | s4).distinct()
        pgr = Paginator(search_res, 12)
        tpages = pgr.num_pages
        try:
            pg = int(request.GET.get('page', '1'))
        except ValueError:
            pg = 1
        if pg > tpages:
            pg = tpages
        fpg = pg - 3 if (pg - 3 >= 3) else 1
        lpg = pg + 3 if (pg + 3 < tpages) else tpages
        e1 = True if (fpg > 1) else e1
        e2 = True if (lpg < tpages) else e2

        pglst = [str(i) for i in range(fpg, lpg + 1)]
        search_res = pgr.page(pg)
    c = Context({'logged_in': loggedin, 'fullname': string.capwords(fullname),
                 'user_id': request.user.id, 'search_res': search_res, 'qry': qry,
                 'page_list': pglst, 'ellipses1': e1, 'ellipses2': e2})
    return HttpResponse(t.render(c))


def profile(request, user_id=None):
    loggedin = False
    fullname = ""
    if user_id == None or User.objects.filter(pk=user_id).count() == 0:
        return redirect('/invalid_user_id/') # if supplied an invalid user id
    elif request.user.is_authenticated() and request.user.id == int(
        user_id): # users profile ...
        user = User.objects.get(id=user_id)
        profile = user.get_profile()
        uploadsavegames = UploadedGame.objects.filter(user=user)
        form = UploadGameForm()
        comments = Comments.objects.filter(user=user)
        owner = True
        loggedin = True
        fullname = user.get_full_name()

        if request.method == "POST":
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.username = request.POST['username']
            user.set_password(request.POST['password'])
            user.email = request.POST['email']

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
                return HttpResponse(serializers.serialize('json', [user, profile]),
                                    mimetype='application/json')

        context = {'user': user,
                   'profile': profile,
                   'uploadsavegames': uploadsavegames,
                   'form': form,
                   'comments': comments,
                   'owner': owner,
                   'logged_in': loggedin,
                   'fullname': string.capwords(fullname),
                   'user_id': user.id}

        return render_to_response('account/profile.html',
                                  context,
                                  context_instance=RequestContext(request))
    elif User.objects.get(pk=user_id).get_profile().private: # if profile is private ..
        return redirect('/')
    else: # public profile viewed by anyone ...
        user = User.objects.get(id=user_id)
        profile = user.get_profile()
        uploadsavegames = UploadedGame.objects.filter(user=user, private=False)
        comments = Comments.objects.filter(user=user)
        loggedin = True
        fullname = user.get_full_name()

        context = {'logged_in': loggedin, 'fullname': string.capwords(fullname), 'user': user,
                   'profile': profile, 'uploadsavegames': uploadsavegames, 'comments': comments}

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


    game = UploadedGame.objects.get(id=uploaded_id)
    info['upvotes'] = str(game.upvote)
    info['downvotes'] = str(game.downvote)

    info['data_title'] = "f.zip"
    info[
    'date'] = '1/2/2222' #UploadedGame.objects.filter(user=user_id, id=uploaded_id).values()[0]['datetime']
    info['uploader'] = User.objects.filter(id=user_id).values()[0].get('username')
    info['profile_path'] = '/' + UserProfile.objects.filter(user=user_id).values()[0].get('avatar')
    info['download_link'] = UploadedGame.objects.filter(user=user_id, id=uploaded_id).values()[0][
                            'file']
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
    entry.user = user
    entry.comment = str(comment_data)
    entry.datetime = now

    entry.save()

    res = Comments.objects.filter(uploadedgame=17).values()
    info = {}


    # Just get the last comment, and then return it
    info['only'] = Comments.objects.filter(uploadedgame=17).values()[
                   len(Comments.objects.filter(uploadedgame=17).values()) - 1]
    info['only']['datetime'] = ''

    return HttpResponse(json.dumps(info))


def getvotedata(request):
    uploaded_id = request.GET.get('uploaded_game_id')
    upvoted = request.GET.get('upvote', '')
    downvoted = request.GET.get('downvote', '')
    info = {}
    game = UploadedGame.objects.get(id=uploaded_id)
    info['upvotes'] = game.upvote
    info['downvotes'] = game.downvote
    if upvoted:
        game.upvote = game.upvote + 1
        info['upvotes'] = game.upvote
    if downvoted:
        game.downvote = game.downvote + 1
        info['downvotes'] = game.downvote
    game.save()

    return HttpResponse(json.dumps(info))


def uploadHandler(saveFile):
    path = 'savegame/static/saved_games/' + saveFile.name

    existCount = 1
    fileName = saveFile.name.split(".")[0]
    fileExtension = saveFile.name.split(".")[1]

    # Check if the file already exists:
    while os.path.exists(path):
        # Stay in this loop until we find a path that does NOT exist.
        path = 'savegame/static/saved_games/' +\
               fileName + '_' + str(existCount) + '.' + fileExtension
        existCount += 1

    # Write the saveFile to some location.
    destination = open(path, 'wb+')
    for chunk in saveFile.chunks():
        destination.write(chunk)
    destination.close()
    return path


def upload(request):
    # Only allow the user to upload data if he or she has already logged in.
    if request.user.is_authenticated():
        if request.method == 'POST':
            # Case: User is logged in and had just submitted a save file:
            inUploadForm = UploadGameForm(request.POST, request.FILES)
            # if inUploadForm.is_valid():
            uploadedLocation = uploadHandler(request.FILES['file'])
            # Create the database entry for the saveFile

            uploadTemplate = loader.get_template('account/upload.html')
            uploadContext = RequestContext(request, {'accessDenied':\
                                                         "Your file has been successfully uploaded."})
            return HttpResponse(uploadTemplate.render(uploadContext))
        else:
            # Case: User logged in but had not submitted saved data for uploading:
            uploadForm = UploadGameForm()
            uploadTemplate = loader.get_template('account/upload.html')
            uploadContext = RequestContext(request, {'uploadForm': uploadForm})
            return HttpResponse(uploadTemplate.render(uploadContext))
    else:
        uploadTemplate = loader.get_template('account/upload.html')
        uploadContext = RequestContext(request,
                                       {'accessDenied': "You must be logged in to see this page."})
        return HttpResponse(uploadTemplate.render(uploadContext))