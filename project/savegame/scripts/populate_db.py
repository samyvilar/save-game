from BeautifulSoup import BeautifulSoup
from dateutil import parser

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

    populate_game(root_page, [44, totalpages], 'PC')

def populate_xbox_360_games():
    totalpages = 73
    root_page = 'http://www.gamespot.com/games.html?type=games&platform=1029&mode=all&sort=views&dlx_type=all&sortdir=asc&official=all&page='

    populate_game(root_page, totalpages, 'Xbox 360')

def populate_Wii_games():
    totalpages = 53
    root_page = 'http://www.gamespot.com/games.html?type=games&platform=1031&mode=all&sort=views&dlx_type=all&sortdir=asc&official=all&page='

    populate_game(root_page, totalpages, 'Wii')

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

    populate_game(root_page, totalpages, 'DS')

def populate_iPhone_games():
    totalpages = 278
    root_page = 'http://www.gamespot.com/iphone/index.html?navclk=iphone&tag=nav-top%3Biphone&page='

    populate_game(root_page, totalpages, 'iPhone')

def populate_Android_games():
    totalpages = 2
    root_page = 'http://www.gamespot.com/android/index.html?navclk=android&tag=nav-top%3Bandroid&page='

    populate_game(root_page, totalpages, 'Android')
            


if __name__ == "__main__":
    print "Populating company ..."
    populate_company()
    print "done"
    print "Populating platform ..."
    populate_platform()
    print "done"
    print "Populating genre ..."
    populate_genre()
    print "done"

    print "Populating games pc ..."
    populate_games_pc()
    print "done"

    print "Populating games Xbox 360 ..."
    populate_xbox_360_games()
    print "done"

    print "Populating games Wii ..."
    populate_Wii_games()
    print "done"

    print "Populating games PS3 ..."
    populate_PS3_games()
    print "done"

    print "Populating games PSP ..."
    populate_PSP_games()
    print "done"

    print "Populating games 3DS ..."
    populate_3DS_games()
    print "done"

    print "Populating games DS ..."
    populate_DS_games()
    print "done"

    print "Populating games iphone ..."
    populate_iPhone_games()
    print "done"

    print "Populating games Android ..."
    populate_Android_games()
    print "done"



