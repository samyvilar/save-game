from django.db                  import models
from django.contrib.auth.models import User
from django.db.models.signals   import post_save


max_length = 100
class Company(models.Model):
    name = models.CharField(max_length = max_length)

    def __unicode__(self):
        return  u'%s' % self.name

    class Meta:
        verbose_name = 'Companies'
        verbose_name_plural = 'Companies'

class Platform(models.Model):
    name     = models.CharField(max_length = max_length)
    company  = models.ForeignKey(Company)

    def __unicode__(self):
        return  u'%s' % self.name

    class Meta:
        verbose_name = 'Platforms'
        verbose_name_plural = 'Platforms'

class Genre(models.Model):
    name = models.CharField(max_length = max_length)

    def __unicode__(self):
        return  u'%s' % self.name

    class Meta:
        verbose_name = 'Genries'
        verbose_name_plural = 'Genries'

class Game(models.Model):
    title        = models.CharField(max_length = max_length)
    release_date = models.DateField(null = True)
    platform     = models.ForeignKey(Platform)
    genre        = models.ForeignKey(Genre)
    smallcover   = models.ImageField(upload_to = 'savegame/static/images')
    description  = models.TextField()

    def admin_image(self):
        return '<img src="%s"/>' % self.smallcover.name
    admin_image.allow_tags = True

    def __unicode__(self):
        return  u'%s' % self.title

    class Meta:
        verbose_name = 'Games'
        verbose_name_plural = 'Games'

class UserProfile(models.Model):
    user    = models.ForeignKey(User)
    avatar  = models.ImageField(upload_to = 'savegame/static/images')
    private = models.BooleanField()

    def __str__(self):
        return "%s's profile" % self.user

    def admin_image(self):
        return '<img src="/static/images/%s" />' % self.avatar.name
    admin_image.allow_tags = True





def create_user_profile(sender, instance, created, **kwargs):
    if created:
       profile, created = UserProfile.objects.get_or_create(user=instance)
       profile.save()

post_save.connect(create_user_profile, sender = User)

class UploadedGame(models.Model):
    game        = models.ForeignKey(Game)
    platform    = models.ForeignKey(Platform)
    file        = models.FileField(upload_to = 'savegame/static/saved_games')
    user        = models.ForeignKey(User)
    datetime    = models.DateTimeField()
    comment     = models.TextField()
    upvote      = models.IntegerField()
    downvote    = models.IntegerField()
    private     = models.BooleanField()

    def __unicode__(self):
        return  u'%s' % self.game.title

    class Meta:
        verbose_name = 'UploadedGames'
        verbose_name_plural = 'UploadedGames'

class Comments(models.Model):
    uploadedgame = models.ForeignKey(UploadedGame)
    user         = models.ForeignKey(User)
    comment      = models.TextField()
    datetime     = models.DateTimeField()

    def __unicode__(self):
        return  u'%s' % self.comment

    class Meta:
        verbose_name = 'Comments'
        verbose_name_plural = 'Comments'
