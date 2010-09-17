import datetime

from django.db import models
from django.db.models import Sum
from django.contrib.sites.models import Site
from django.contrib.localflavor.us import models as usmodels

import mptt

from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    """A skill Chris Sinchok has some experience in.
    
    A skill has a score, calculated against time. This calculation is based on experiences logged over
    a given duration of time.
    """
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    
    def __unicode__(self):
        return self.name
    
    def score(self, startdate=None, enddate=None):
        effect_list = self.effect_list(startdate, enddate)
        
        if(len(effect_list) > 0):
            effect_sum = effect_list[0].effort
            for effect in effect_list[1:]:
                if effect.effort is not None and effect.effort > 0:
                    effect_sum += (((100 - effect_sum)/100.0) * effect.effort)
            return effect_sum
        else:
            return 0 
        
    def effect_list(self, startdate=None, enddate=None):
        effect_list=[]
        
        descendants = self.get_leafnodes(include_self=True)
        effect_list = Effect.objects.filter(effected_skill__in=[skill.pk for skill in descendants]).order_by('experience__enddate')
            
        if startdate is not None:
            effect_list = effect_list.filter(experience__enddate__gt=startdate)
            
        if enddate is not None:
            effect_list = effect_list.filter(experience__enddate__lt=enddate)
                
        return effect_list

mptt.register(Skill, order_insertion_by=['name'])


class Company(models.Model):
    """A company that Chris Sinchok has worked for."""
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=64)
    
    class Meta:
        verbose_name_plural = "Companies"
    
    def __unicode__(self):
        return self.name


class Role(models.Model):
    """A role Chris Sinchok played at a Company."""
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    startdate = models.DateField()
    enddate = models.DateField(null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True)
    
    def __unicode__(self):
        return "%s at %s" % (self.title, self.company.name)


class Experience(models.Model):
    """Experience that Chris Sinchok has had."""
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    startdate = models.DateField()
    enddate = models.DateField(null=True, blank=True)
    role = models.ForeignKey(Role)
    
    def __unicode__(self):
        return self.title


class Effect(models.Model):
    """An effect on a skill."""
    effort = models.IntegerField();
    effected_skill = models.ForeignKey(Skill);
    experience = models.ForeignKey(Experience);
    
    def __unicode__(self):
        return "%s/100 to %s during %s" % (self.effort, self.effected_skill, self.experience)
        
class SiteProfile(models.Model):
    """A profile for Chris Sinchok"""
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone = usmodels.PhoneNumberField()
    bio = models.TextField(null=True, blank=True)
    address1 = models.CharField(max_length=64)
    address2 = models.CharField(max_length=64, null=True, blank=True)
    state = usmodels.USStateField()
    zipcode = models.IntegerField()
    email = models.EmailField()
    website = models.URLField()
    site = models.OneToOneField(Site)
    
    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)
    