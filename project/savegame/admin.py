from savegame.models import *
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class Company_Admin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ['name']

class Platform_Admin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company')
    search_fields = ['name', 'company']

class Genre_Admin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class Game_Admin(admin.ModelAdmin):
    list_display = ('id', 'admin_image', 'title', 'release_date', 'platform', 'genre', 'description')
    search_fields = ('title', 'release_date', 'platform', 'genre', 'description')


admin.site.unregister(User)
class UserProfileInline(admin.StackedInline):
	model = UserProfile    

class UserProfileAdmin(UserAdmin):    
	inlines = [UserProfileInline]    

class UploadedGame_Admin(admin.ModelAdmin):
    list_display = ('id', 'game', 'platform', 'user', 'datetime', 'comment', 'upvote', 'downvote', 'private')
    search_fields = ['game', 'platform', 'user', 'datetime', 'comment', 'private']
    

class Comments_Admin(admin.ModelAdmin):
    list_display = ('id', 'uploadedgame', 'user', 'comment', 'datetime')
    search_fields = ['uploadedgamed', 'user', 'datetime', 'comment']
    
admin.site.register(Company,        Company_Admin)
admin.site.register(Platform,       Platform_Admin)
admin.site.register(User,           UserProfileAdmin)
admin.site.register(Genre,          Genre_Admin)
admin.site.register(Game,           Game_Admin)
admin.site.register(UploadedGame,   UploadedGame_Admin)
admin.site.register(Comments,       Comments_Admin)


