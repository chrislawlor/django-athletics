from datetime import datetime, timedelta
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings
from tagging.fields import TagField
from django.contrib.localflavor.us.models import PhoneNumberField, USStateField 

import tagging
import urllib

def get_lat_long(location):
    key = settings.GOOGLE_API_KEY
    output = "csv"
    location = urllib.quote_plus(location)
    request = "http://maps.google.com/maps/geo?q=%s&output=%s&key=%s" % (location, output, key)
    data = urllib.urlopen(request).read()
    dlist = data.split(',')
    if dlist[0] == '200':
        return "%s, %s" % (dlist[2], dlist[3])
    else:
        return ''


class StandardMetadata(models.Model):
    """
    A basic (abstract) model for metadata.
    
	Subclass new models from 'StandardMetadata' instead of 'models.Model'.
    """
    created = models.DateTimeField(default=datetime.now, editable=False)
    updated = models.DateTimeField(default=datetime.now, editable=False)
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        self.updated = datetime.now()
        super(StandardMetadata, self).save(*args, **kwargs)

class PublicManager(models.Manager):
    def get_query_set(self):
        return super(PublicManager, self).get_query_set().filter(public=True)


class Town(models.Model):
    name=models.CharField(_('name'), max_length=100)
    

    def __unicode__(self):
        return u'%s, %s %s' % (self.name, self.state, self.zipcode)
    
class Sport(StandardMetadata):
    """Sport model.
       A farily simple model to handle categorizing of teams into sports."""
    name=models.CharField(_('name'), max_length=100)
    slug=models.SlugField(_('slug'), unique=True) 

    def __unicode__(self):
        return self.name

class Position(StandardMetadata):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    game = models.ForeignKey(Sport)
    description = models.TextField()
    
    class Meta:
        unique_together = ['game', 'slug']
    
    def __unicode__(self):
        return self.name
    
    
class School(StandardMetadata):
    """School model.
       A meta model for Schools that contains basic info each school needs:

       name, slug, website, description, admins."""

    SCHOOL_TYPE_CHOICES = (
        ('K8', _('K-8 School')),
        ('HS', _('High School')),
        ('UN', _('University')),
    )
    name=models.CharField(_('name'), max_length=100)
    slug=models.SlugField(_('slug'), unique=True)
    administrators=models.ManyToManyField(User, null=True, blank=True, related_name='')
    description=models.CharField(_('description'), max_length=255)
    phone=PhoneNumberField(_('phone'), blank=True, null=True)
    website=models.URLField(_('website'), blank=True, null=True)
    address=models.CharField(_('address'), max_length=255)
    town=models.ForeignKey(Town)    
    mascot=models.CharField(_('mascot'), max_length=100, help_text="Please use the plural form of the mascot." )
    lat_long=models.CharField(_('coordinates'), max_length=255, blank=True)
    school_type=models.CharField(_('school type'), max_length=2, default="NA", choices=SCHOOL_TYPE_CHOICES)
    public=models.BooleanField(_('public'), default=False)

    objects=models.Manager()
    public_objects=PublicManager()
    
    class Meta:
        verbose_name = _('school')
        verbose_name_plural = _('schools')
        get_latest_by='created'

    def save(self):
        if not self.lat_long:
            location = "%s %s" % (self.address, self.town)
            self.lat_long = get_lat_long(location)
            if not self.lat_long:
                location = "%s" % (self.town)
                self.lat_long = get_lat_long(location)
        super(School, self).save()    
        
    def get_absolute_url(self):
        args=[self.slug]
        return reverse('school_detail', args=args)

    def __unicode__(self):
        return self.name


class Team(StandardMetadata):
    SPORT_TYPE_CHOICES=(
    ('NA', _('Not applicable')),
    ('VA', _('Varsity')),
    ('JV', _('Junior varsity')),
    ('A', _('A team')),
    ('B', _('B team')),
    )
    
    GENDER_CHOICES=(
        ('G', _('Girls')),
        ('B', _('Boys')),
        ('M', _('Mixed')),        
    )
    
    school=models.ForeignKey(School, blank=True, null=True)
    sport=models.ForeignKey(Sport)
    sport_type=models.CharField(_('sport type'), default="NA", choices=SPORT_TYPE_CHOICES, max_length=2)
    gender=models.CharField(_('gender'), default="M", choices=GENDER_CHOICES, max_length=1)
    public=models.BooleanField(_('public'), default=False)
    objects=models.Manager()
    public_objects=PublicManager()
    
    class Meta:
        verbose_name = _('team')
        verbose_name_plural = _('teams')
        get_latest_by='created'
    
    def __unicode__(self):
        if self.year == datetime.now().year:
            if self.sport_type != "NA":
                return u'%s %s %s' % (self.school, self.get_sport_type_display(), self.sport)
            else:
                return u'%s %s' % (self.school, self.sport)
        else:
            if self.sport_type != "NA":
                return u'%s %s %s %s' % (self.school, self.get_sport_type_display(), self.sport, self.year)
            else:
                return u'%s %s %s' % (self.school, self.sport, self.year)
    
    def get_absolute_url(self):
        args=[self.slug]
        return reverse('team_detail', args=args)
        
    #def save(self):
    #    if not self.mascot and self.organization.mascot:
    #        self.mascot = self.organization.mascot
    #    super(Team, self).save()        


class Membership(StandardMetadata):
    user = models.ForeignKey(User)
    teamseason = models.ForeignKey('TeamSeason')
    positions = models.ManyToManyField(Position, blank=True, null=True)


class CoachingPosition(StandardMetadata):
    user = models.ForeignKey(User)
    teamseason = models.ForeignKey('TeamSeason')


class LeagueMembership(StandardMetadata):
    league = models.ForeignKey('League')
    team = models.ForeignKey('Team')
    joined = models.DateField()
    left = models.DateField(blank=True, null=True)


class League(StandardMetadata):
    name = models.CharField(max_length=100)
    acryonym = models.CharField(max_length=10, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    teams = models.ManyToManyField(Team, through=LeagueMembership)
    

class Season(StandardMetadata):
    """
    A collection of games.
    """
    year = models.PositiveIntegerField()
    sport = models.ForeignKey(Sport)


class TeamSeason(StandardMetadata):
    """
    The makeup of a team for a particular season.
    """
    season = models.ForeignKey(Season)
    team = models.ForeignKey(Team)
    roster = models.ManyToManyField(User, through=Membership, related_name='playing_seasons')
    year = models.PositiveIntegerField()
    coaches = models.ManyToManyField(User, through=CoachingPosition, related_name='coaching_seasons')
    
    def __unicode__(self):
        return "%d %s" % (self.year, self.team.name)
    

class Location(StandardMetadata):
    name=models.CharField(_('name'), max_length=100)
    slug=models.SlugField(_('slug'), unique=True)
    school=models.ForeignKey(School, blank=True, null=True)
    address=models.CharField(_('address'), max_length=255)
    city=models.CharField(_('city'), max_length=100)
    state=USStateField(_('state'))
    zipcode=models.CharField(_('zip'), max_length=10)
    state=USStateField()
    lat_long=models.CharField(_('coordinates'), max_length=255, blank=True)
    public=models.BooleanField(_('public'), default=False)

    objects=models.Manager()
    public_objects=PublicManager()

    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')
        get_latest_by='created'
        
    def __unicode__(self):
        return self.name
        
    def get_absolute_url(self):
        args=[self.slug]
        return reverse('location_detail', args=args)
        
    def save(self):
        if not self.lat_long:
            location = "%s %s" % (self.address, self.town)
            self.lat_long = get_lat_long(location)
            if not self.lat_long:
                location = "%s" % (self.town)
                self.lat_long = get_lat_long(location)
        super(Location, self).save()


class Game(StandardMetadata):
    start = models.DateTimeField(_("start"))
    end = models.DateTimeField(_("end"),help_text=_("The end time must be later than the start time."))
    home_team=models.ForeignKey(Team, related_name="home_team")
    away_team=models.ForeignKey(Team, related_name="away_team")
    location=models.ForeignKey(Location)
    home_team_score = models.PositiveIntegerField(blank=True, null=True)
    away_team_score = models.PositiveIntegerField(blank=True, null=True)
    season = models.ForeignKey(Season)
    summary = models.TextField()
    
    class Meta:
        verbose_name = _('game')
        verbose_name_plural = _('games')
        get_latest_by='created'

    def __unicode__(self):
        return u'%s v %s - %s' % (self.home_team, self.away_team, self.start.date())
        
    def get_absolute_url(self):
        args=[self.slug]
        return reverse('team_detail', args=args)
        
    def save(self):
        title = "%s v %s - %s" % (self.home_team, self.away_team, self.start)
        if not self.title or self.title != title:
            title = "%s v %s - %s" % (self.home_team, self.away_team, self.start)
            self.title=title
        if not self.end:
            self.end = self.start + timedelta(hours=1.5)
        super(Game, self).save()

