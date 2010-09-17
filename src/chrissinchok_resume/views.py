from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from chrissinchok_resume.models import Skill, Role, Company
from django.http import HttpResponse
from chrissinchok_resume.models import Skill, Role, Company, Experience


def resume(request, template_name='chronological.html', type='chronological'):
    if 'skill_id' in request.GET:
        skill_list = request.GET['skill_id']
    else:
        skill_root_nodes = list(Skill.tree.root_nodes())
        skill_root_nodes.sort(key=lambda skill: -skill.score())
        
        skill_list = list(skill_root_nodes[0].get_leafnodes())
        skill_list.sort(key=lambda skill: -skill.score())
        
    experience_id_list = Effect.objects.filter(effected_skill__in=[skill.pk for skill in skill_list[:4]]).values_list('experience', flat=True) 
    experience_list = Experience.objects.filter(pk__in=experience_id_list)
    
    role_id_list = Experience.objects.filter(pk__in=experience_list).values_list('role', flat=True) 
    role_list = Role.objects.filter(pk__in=role_id_list).order_by('-startdate')
    
    context = {'skills': skills, 'roles' : roles}
    
    return render_to_response(template_name, context)