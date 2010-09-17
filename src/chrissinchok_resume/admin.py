from chrissinchok_resume.models import *
from django.contrib import admin

class EffectInline(admin.StackedInline):
    model = Effect
    extra = 4
    
class ExperienceAdmin(admin.ModelAdmin):
    inlines = [EffectInline]


admin.site.register(Skill)
admin.site.register(Company)
admin.site.register(Role)
admin.site.register(Experience, ExperienceAdmin)
admin.site.register(Effect)
admin.site.register(SiteProfile)