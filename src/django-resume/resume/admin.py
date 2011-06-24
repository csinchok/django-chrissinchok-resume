from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from models import *

class EffectInline(admin.StackedInline):
    model = Effect
    extra = 4
    
class ExperienceAdmin(admin.ModelAdmin):
    inlines = [EffectInline]
    
admin.site.register(Experience, ExperienceAdmin)


class SkillVersionInline(admin.StackedInline):
    model = SkillVersion
    extra = 1

class SkillAdmin(MPTTModelAdmin):
    inlines = [SkillVersionInline]

admin.site.register(Skill, SkillAdmin)

admin.site.register(Company)
admin.site.register(Role)
admin.site.register(Effect)
admin.site.register(SiteProfile)