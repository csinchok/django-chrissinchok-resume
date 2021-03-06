import datetime

from django.db import models
from django.db.models import Sum
from django.contrib.sites.models import Site
from django.contrib.localflavor.us import models as usmodels
from django.contrib.auth.models import User

from mptt.models import MPTTModel, TreeForeignKey

class Skill(MPTTModel):
    """A skill the candidate has some experience in.
    
    A skill has a score, calculated against time. This calculation is based on experiences logged over
    a given duration of time.
    """
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    
    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['name']
    
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

class SkillVersion(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    skill = models.ForeignKey(Skill)
    
    def __unicode__(self):
        return "%s - %s" % (self.skill.name, self.name)

class Company(models.Model):
    """A company that the candidate has had some associate with"""
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=64)
    website = models.URLField(null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Companies"
    
    def __unicode__(self):
        return self.name


class Role(models.Model):
    """A role the candidateplayed at a Company."""
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    startdate = models.DateField()
    enddate = models.DateField(null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True)
    
    def __unicode__(self):
        return "%s at %s" % (self.title, self.company.name)


class Experience(models.Model):
    """Experience that the candidate has had."""
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    startdate = models.DateField()
    enddate = models.DateField(null=True, blank=True)
    role = models.ForeignKey(Role)
    
    def __unicode__(self):
        return self.title


class Effect(models.Model):
    """An effect on a skill."""
    effort = models.IntegerField()
    effected_skill = models.ForeignKey(Skill)
    experience = models.ForeignKey(Experience)
    version = models.ForeignKey(SkillVersion, null=True, blank=True)
    
    def __unicode__(self):
        return "%s/100 to %s during %s" % (self.effort, self.effected_skill, self.experience)
        
class SiteProfile(models.Model):
    """This is the profile for a candidate"""
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
    