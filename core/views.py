from django.shortcuts import render
from .models import Artifact
import json 

def home(request):
    artifacts = [{"title": x.title, "description": x.description, "descriptionWC": x.descriptionWC}for x in Artifact.objects.all()]
    artifacts_json = json.dumps(artifacts)
    context = {'artifacts': artifacts_json}
    return render(request, 'core/index.html', context)