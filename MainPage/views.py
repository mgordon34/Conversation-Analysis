from django.http import HttpResponse
from django.shortcuts import render
import analyzer

def index(request):
    return render(request, 'main/index.html')

def results(request):
    output = analyzer.echo(request.POST['info'])
    return HttpResponse(output)
