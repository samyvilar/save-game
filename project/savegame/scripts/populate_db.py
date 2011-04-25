from BeautifulSoup import BeautifulSoup
from dateutil import parser

import random
import datetime

import socket
socket.setdefaulttimeout(60.0)

import urllib2
import sys, os

sys.path.append(os.path.abspath('../../..'))
os.environ['DJANGO_SETTINGS_MODULE'] ='project.settings'

from django.core.management import setup_environ
from project                import settings

setup_environ(settings)

from project.savegame.models import *

def populate_company():
    companies = ['Microsoft', 'Sony', 'Nintendo', 'Apple', 'Google']

    for company in companies:
        temp, created = Company.objects.get_or_create(name = company)
        temp.save()

def populate_platform():
    platforms = [['PC', u'Microsoft'], ['Xbox 360', 'Microsoft'], ['Wii', 'Nintendo'],
                 ['PS3', u'Sony'], ['PSP', 'Sony'], ['3DS', 'Nintendo'], ['DS', 'Nintendo'],
                 ['iPhone', u'Apple'], ['Android', 'Google']]

    for platform in platforms:
        temp, created = Platform.objects.get_or_create(name = platform[0], company = Company.objects.get(name = platform[1]))
        temp.save()


def populate_genre():
    genres = [
"Puzzle"
,"Action Adventure"
,"Action"
,"First-Person Shooters"
,"Tactical Shooters"
,"Other Shooters"
,"Role-Playing"
,"Massively Multiplayer"
,"Real-Time Strategy"
,"Turn-Based Strategy"
,"Other Strategy Games"
,"Racing"
,"Car Combat"
,"Other Driving"
,"Baseball"
,"Basketball"
,"Football"
,"Golf"
,"Hockey"
,"Soccer"
,"Alternative Sports"
,"Wrestling"
,"Other Sports Games"
,"Platformers"
,"Adventure"
,"Fighting"
,"Simulation"
,"Combat Sim"
,"Futuristic Combat Sim"
,"Rhythm"
,"Party"
,"Card Battle"
,"Virtual Life"
,"Parlor"
,"Compilations"
,"Miscellaneous"
]

    for genre in genres:
        temp, created = Genre.objects.get_or_create(name = genre)
        temp.save()


def populate_game(root_page, total, platform):
    if type(total) == type([]):
        start = total[0]
        end   = total[1]
    else:
        start = 0
        end = total
    count = 0
    for index in xrange(start, end):
        url = root_page + str(index)
        print url
        try:
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page)
        except socket.timeout:
            print "Timed out, trying again ..."
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page)
        
        tbody = soup.findAll('tbody')
        assert len(tbody) == 1
        tbody = tbody[0]

        trs = tbody.findAll('tr')
        index = 0
        for tr in trs:
            print index
            index = index + 1
            
            if platform != 'iPhone' and platform != 'Android':
                th = tr.findAll('th')
                assert len(th) == 1
                th = th[0]
                a = th.findAll('a')
                assert len(a) == 1
                a = a[0]

                title = a.contents[0].strip()

            tds = tr.findAll('td')
            
            if platform == 'iPhone' or platform == 'Android':
                a = tds[1].findAll('a')[0]
                title = a.contents
                genre_name = tds[2].findAll('a')[0].contents
            else:
                genre_name = tds[0].contents[0]
                
            try:
                genre = Genre.objects.get(name = genre_name.strip())
            except Genre.DoesNotExist:
                genre = Genre.objects.create(name = genre_name.strip())                
                genre.save()

            try:
                release_date = parser.parse(tds[3].contents[0])
            except ValueError:
                release_date = None

            platform_obj = Platform.objects.get(name = platform)

            try:
                desc_page = urllib2.urlopen(a['href'])
                soup = BeautifulSoup(desc_page)
            except socket.timeout:
                print "Timed out, trying again ..."
                desc_page = urllib2.urlopen(a['href'])
                soup = BeautifulSoup(desc_page)
            except urllib2.HTTPError:
                print "Couldn't go to the details page ... so skipping"
                count = count + 1
                continue

            
            ps = soup.findAll('p')

            if ((ps[1].has_key('property') and (ps[1]['property'] == u'v:description' or ps[1]['property'] == u'v:summary')) or (ps[1].has_key('class') and ps[1]['class'] == u'product deck')):
                d = ps[1].contents[0]
            else:
                print "No summary found!"
                d = ""

            imgs = soup.findAll('img')

            img_url = ""
            for img in imgs:
                if img.has_key('property') and img['property'] == u'v:photo':
                    img_url = img['src']
                    break

                if img['src'].count(u'http://image.gamespotcdn.net/gamespot/images/2003/all/boxshots2/') == 1:
                    img_url = img['src']
                    break

                if img['src'].count('http://image.gamespotcdn.net/gamespot/images//2003/all/boxshots2/') == 1:
                    img_url = img['src']
                    break

                if img['src'].count('http://image.gamespotcdn.net/gamespot/shared/') == 1:
                    img_url = img['src']
                    break

            assert img_url != ""

            '''
            try:
                image = urllib2.urlopen(url).read()
            except socket.timeout:
                print "Timed out, trying again ..."
                image = urllib2.urlopen(url).read()
            except urllib2.URLError:
                try:
                    image = urllib2.urlopen(url).read()
                except urllib2.URLError:
                    print "I give up, skipping in it ..."
                    count = count + 1
                    continue
            
            name = url.split("/")[len(url.split("/")) - 1]
            open('../static/images/' + name, 'wb').write(image)
            '''

            try:
                game = Game.objects.get(title = title.strip(),
                                              release_date = release_date,
                                              platform = platform_obj,
                                              genre = genre,
                                              description = d.strip())
            except Game.DoesNotExist:
                game = Game.objects.create(title = title.strip(),
                                              release_date = release_date,
                                              platform = platform_obj,
                                              genre = genre,
                                              description = d.strip())


                game.smallcover.name = img_url
                game.save()
    print "Skipped " + str(count)



def populate_games_pc():
    totalpages = 288
    root_page = 'http://www.gamespot.com/games.html?type=games&platform=5&mode=all&sort=views&dlx_type=all&sortdir=asc&official=all&page='

    populate_game(root_page, [224, totalpages], 'PC')

def populate_xbox_360_games():
    totalpages = 73
    root_page = 'http://www.gamespot.com/games.html?type=games&platform=1029&mode=all&sort=views&dlx_type=all&sortdir=asc&official=all&page='

    populate_game(root_page, totalpages, 'Xbox 360')

def populate_Wii_games():
    totalpages = 53
    root_page = 'http://www.gamespot.com/games.html?type=games&platform=1031&mode=all&sort=views&dlx_type=all&sortdir=asc&official=all&page='

    populate_game(root_page, [46, totalpages], 'Wii')

def populate_PS3_games():
    totalpages = 31
    root_page = 'http://www.gamespot.com/games.html?type=games&platform=1028&mode=all&sort=views&dlx_type=all&sortdir=asc&official=all&page='

    populate_game(root_page, totalpages, 'PS3')

def populate_PSP_games():
    totalpages = 37
    root_page = 'http://www.gamespot.com/games.html?type=games&platform=1024&mode=all&sort=views&dlx_type=all&sortdir=asc&official=all&page='

    populate_game(root_page, totalpages, 'PSP')

def populate_3DS_games():
    totalpages = 4
    root_page = 'http://www.gamespot.com/games.html?type=games&platform=1068&mode=all&sort=views&dlx_type=all&sortdir=asc&official=all&page='

    populate_game(root_page, totalpages, '3DS')

def populate_DS_games():
    totalpages = 81
    root_page ='http://www.gamespot.com/games.html?type=games&platform=1026&mode=all&sort=views&dlx_type=all&sortdir=asc&official=all&page='

    populate_game(root_page, [46, totalpages], 'DS')

def populate_iPhone_games():
    totalpages = 278
    root_page = 'http://www.gamespot.com/iphone/index.html?navclk=iphone&tag=nav-top%3Biphone&page='

    populate_game(root_page, totalpages, 'iPhone')

def populate_Android_games():
    totalpages = 2
    root_page = 'http://www.gamespot.com/android/index.html?navclk=android&tag=nav-top%3Bandroid&page='

    populate_game(root_page, totalpages, 'Android')


def popuate_male_users():
    names = [
["Bradford", "Jensen"],
["Patrick", "Zimmerman"],
["Rudy", "Parks"],
["Trevor", "Aguilar"],
["Frank", "Ortiz"],
["Henry", "Riley"],
["Wayne", "Taylor"],
["Stewart", "Mcdaniel"],
["Rodolfo", "Stevens"],
["Adam", "Wagner"],
["Rudolph", "Miller"],
["Nathan", "Murphy"],
["Russell", "Walsh"],
["Shaun", "Carson"],
["Joseph", "Joseph"],
["Bennie", "Benson"],
["Gregory", "Torres"],
["Lloyd", "Ward"],
["Jose", "Phelps"],
["Cesar", "Barker"],
["Gregg", "Lindsey"],
["Alonzo", "Snyder"],
["Felix", "Lowe"],
["Alton", "Warren"],
["Darrin", "Hudson"],
["Claude", "Stone"],
["Rogelio", "Perry"],
["Willis", "Sullivan"],
["Roosevelt", "Bates"],
["Herman", "Fleming"],
["Darrel", "Poole"],
["Ruben", "Obrien"],
["Hugo", "Austin"],
["Alex", "Sparks"],
["Lawrence", "Freeman"],
["Ivan", "Bradley"],
["Rene", "Mcgee"],
["Kristopher", "Reynolds"],
["Shane", "Patterson"],
["Cody", "Peterson"],
["Neal", "Wise"],
["Keith", "Pearson"],
["Delbert", "Barnett"],
["Jesus", "Johnston"],
["Terence", "Watkins"],
["Doug", "Gibson"],
["Ricky", "Hayes"],
["Brian", "Gibbs"],
["Gustavo", "Moran"],
["Hubert", "Burton"],
["Jody", "Garrett"],
["Merle", "Shelton"],
["Alfred", "Ball"],
["Robin", "Bishop"],
["Clark", "Newton"],
["Carl", "Bryant"],
["Dean", "Evans"],
["Dwayne", "Myers"],
["Sam", "Pittman"],
["Bryan", "Greene"],
["Jaime", "Allen"],
["Luis", "Sandoval"],
["Ronnie", "Simon"],
["Saul", "Logan"],
["Bob", "Morales"],
["Conrad", "Washington"],
["Rufus", "Tyler"],
["Jermaine", "Graham"],
["Donnie", "Knight"],
["Jonathan", "Farmer"],
["Vernon", "Franklin"],
["Harvey", "Peters"],
["Ramiro", "Marshall"],
["Lorenzo", "Santiago"],
["Raymond", "Meyer"],
["Ian", "Mccoy"],
["Amos", "Wilkins"],
["Julian", "Bridges"],
["Percy", "Bowen"],
["Curtis", "Jenkins"],
["Jacob", "Chambers"],
["Lucas", "Salazar"],
["Jeffery", "Brewer"],
["Carlos", "Rogers"],
["Thomas", "Wells"],
["Carroll", "Ingram"],
["Arturo", "Boyd"],
["Bert", "Shaw"],
["Craig", "Hansen"],
["Ken", "Ramsey"],
["Guy", "Alexander"],
["Todd", "Lawson"],
["Austin", "Vaughn"],
["Wm", "Ross"],
["Glenn", "Haynes"],
["Hugh", "Dean"],
["Kim", "Sanders"],
["Kent", "Hicks"],
["Josh", "Richardson"],
["Phillip", "Williamson"]]

    for name in names:
        firstname = name[0]
        lastname = name[1]
        username = (firstname + '.' + lastname).lower()
        email = username + '@' + random.sample(["gmail.com", "yahoo.com", "hotmail.com"], 1)[0]
        try:
            user = User.objects.get(username = username)
        except Exception:
            user = User.objects.create(username = username, password = "", first_name = firstname, last_name = lastname,
                                        email = email)
            user.set_password(lastname)
            user.save()
            profile = user.get_profile()
            profile.private = random.sample([True, False], 1)[0]
            profile.avatar.name = 'static/images/facebook_non_male.gif'
            profile.save()

def popuate_female_users():
    names = [
['Susan', 'Dennis'],
['Darlene', 'Webb'],
['Sharon', 'Blair'],
['Denise', 'Lucas'],
['Flora', 'Jones'],
['Virginia', 'Glover'],
['Eula', 'Cortez'],
['Chelsea', 'Cannon'],
['Esther', 'Bishop'],
['Katie', 'Duncan'],
['Wilma', 'Spencer'],
['Kayla', 'Pena'],
['Kathy', 'Burgess'],
['Rebecca', 'Adkins'],
['Ruth', 'James'],
['Georgia', 'Gross'],
['Mildred', 'Reese'],
['Elaine', 'Padilla'],
['Helen', 'Griffinv'],
['Juana', 'French'],
['Jeannette', 'Logan'],
['Beth', 'Martinez'],
['Julie', 'Fitzgerald'],
['Mae', 'Ingram'],
['Brandy', 'Schultz'],
['Anna', 'Powers'],
['Carol', 'Miles'],
['Joanna', 'Arnold'],
['Carole', 'Benson'],
['Dixie', 'Torres'],
['Joanne', 'Hughes'],
['Tabitha', 'Baker'],
['Lucille', 'Tucker'],
['Olga', 'Daniels'],
['Gina', 'Flores'],
['Mabel', 'Reed'],
['Ada', 'Simmons'],
['Lora', 'Watts'],
['Blanca', 'Warren'],
['Gladys', 'Drake'],
['Natasha', 'Pierce'],
['Cristina', 'Lawson'],
['Katrina', 'Ortiz'],
['Rosa', 'Rice'],
['Amy', 'Luna'],
['Cathy', 'Coleman'],
['Katherine', 'Jefferson'],
['Silvia', 'Frank'],
['Heidi', 'Hopkins'],
['Charlotte', 'Larson'],
['Glenda', 'Barker'],
['Maria', 'Lee'],
['Lorraine', 'Romero'],
['Josefina', 'Montgomery'],
['Jasmine', 'Newton'],
['Dora', 'Houston'],
['Kathryn', 'Snyder'],
['Marsha', 'Murray'],
['Louise', 'Carter'],
['Pam', 'Dixon'],
['Lucy', 'Swanson'],
['Annie', 'Green'],
['Deborah', 'Erickson'],
['Sylvia', 'Hunter'],
['Opal', 'Mccoy'],
['Tracy', 'Alvarado'],
['Marion', 'Rogers'],
['Nellie', 'Russell'],
['Guadalupe', 'Summers'],
['Emily', 'Underwood'],
['Antonia', 'Holland'],
['Pauline', 'Gibson'],
['Penny', 'Bradley'],
['Brenda', 'Sandoval'],
['Monique', 'Nelson'],
['Shirley', 'Mitchell'],
['Jeanette', 'Lawrence'],
['Maryann', 'Reeves'],
['Eva', 'Boone'],
['Ebony', 'Morrison'],
['Samantha', 'Ramirez'],
['Deanna', 'George'],
['Kristi', 'Stokes'],
['Charlene', 'Hines'],
['Amber', 'Payne'],
['Vicki', 'Stone'],
['Marta', 'Brown'],
['Audrey', 'Norris'],
['Alison', 'Owens'],
['Christy', 'Jenkins'],
['Phyllis', 'Morton'],
['Dana', 'Carpenter'],
['Lana', 'Williamson'],
['Angie', 'Yates'],
['Bernadette', 'Blake'],
['Shawna', 'Washington'],
['Ora', 'Wagner'],
['Sonja', 'Ferguson'],
['Irene', 'Marshall'],
['Sabrina', 'Wise']]

    for name in names:
        firstname = name[0]
        lastname = name[1]
        username = (firstname + '.' + lastname).lower()
        email = username + '@' + random.sample(["gmail.com", "yahoo.com", "hotmail.com"], 1)[0]
        try:
            user = User.objects.get(username = username)
        except Exception:
            user = User.objects.create(username = username, password = "", first_name = firstname, last_name = lastname,
                                        email = email)
            user.set_password(lastname)
            user.save()
            profile = user.get_profile()
            profile.private = random.sample([True, False], 1)[0]
            profile.avatar.name = 'static/images/facebook_non_female.gif'
            profile.save()


def populate_uploaded_game():
    users = User.objects.all()

    for user in users:
        number = random.randint(0, 10)
        for numberofuploads in xrange(number):
            game = Game.objects.get(pk = random.randint(1, 25))
            platform = Platform.objects.get(name = 'PC')
            dt = datetime.date.today()
            private = random.sample([True, False], 1)[0]
            title = random.sample([game.title + " rocks!", game.title + " working ...", game.title + " stil there ..."], 1)[0]
            description = random.sample(["Finnished the first level ...", "Got to the second level ...",
                "The third level was a real pain!", "Im stuck at this level, pls help me!!!",
                "Completely Finnished the game."], 1)[0]
            upload_game = UploadedGame.objects.create(game = game, platform = platform, user = user,
                datetime = dt, description = description, private = private, upvote = 0, downvote = 0)
            upload_game.file.name = '/static/saved_games/saved-file.bin'
            upload_game.save()

def populate_comments():
    uploaded_games = UploadedGame.objects.all()
    users = User.objects.all()

    for uploads in uploaded_games:
        numberofcomments = random.randint(0, 10)
        for _ in xrange(numberofcomments):
            comment = random.sample([["This saved-gamed saved me so much time thank you ...", 1],
                                     ["It was ok, though I've already reached this point.", 0],
                                     ["Umm this really isn't a saved-game, actually don't go near it!", -1]], 1)[0]
            comments = Comments.objects.create(uploadedgame = uploads, user = random.sample(users, 1)[0],
                        datetime = datetime.date.today(), comment = comment[0])
            
            comments.save()
            if comment[1] == 1:
                uploads.upvote = uploads.upvote + 1
            elif comment[1] == -1:
                uploads.downvote = uploads.downvote - 1

            uploads.save()
            

if __name__ == "__main__":
    print "Populating company ..."
    #populate_company()
    print "done"
    print "Populating platform ..."
    #populate_platform()
    print "done"
    print "Populating genre ..."
    #populate_genre()
    print "done"

    print "Populating games pc ..."
    #populate_games_pc()
    print "done"


    #popuate_male_users()
    #popuate_female_users()
    #populate_uploaded_game()
    #populate_comments()
    
    print "Populating games Xbox 360 ..."
    #populate_xbox_360_games()
    print "done"

    print "Populating games Wii ..."
    #populate_Wii_games()
    print "done"

    print "Populating games PS3 ..."
    #populate_PS3_games()
    print "done"

    print "Populating games PSP ..."
    #populate_PSP_games()
    print "done"

    print "Populating games 3DS ..."
    #populate_3DS_games()
    print "done"

    print "Populating games DS ..."
    populate_DS_games()
    print "done"

    #print "Populating games iphone ..."
    #populate_iPhone_games()
    #print "done"

    #print "Populating games Android ..."
    #populate_Android_games()
    #print "done"



