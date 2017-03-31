from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from MainPage.models import Document
from MainPage.models import Result
from MainPage.forms import DocumentForm
import TextParsing
import Analyze

import json
import numpy as np
import matplotlib.pyplot as plt

arr = []

"""
This method handles any requests to load our home page. It handles when the user uploads a document and passes along
the document to the results page.
"""
def main(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            parser = TextParsing.TextParsing(request.FILES['docfile'].name)
            # Redirect to the document list after POST
            # return HttpResponseRedirect('MainPage.views.main')
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        'appTemps/main.html',
        {'documents': documents, 'form': form},
    )

"""
This method handles any requests to load the results page. It takes in the document passed from main method and passes
it through our parser (TextParsing.csvparse()). It creates the analyze object and begins the analysis over the given
conversation. It passes all of our analysis information into the results page. IMPORTANT FOR PLOTLY GRAPHS
"""
def results(request):
    # Handle file upload
    if request.method == 'POST':
        # print "Results being called"
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            parser = TextParsing.TextParsing(request.FILES['docfile'].name)
            analyzer = Analyze.Analyze()
            analyzer.popDialogEmotion(parser)
            analyzer.setDialogSentiment(parser)
            p = json.dumps(analyzer.getPersonData(parser), separators=(',', ':'))
            arr2 = parser.plotlyBarFreqDist("everyone")
            score = analyzer.getAverageConversationScores(parser)
            convo = analyzer.getConversationScore(parser)["trust"]
            cwords = parser.getNCommonWords(50)
            # print freqdist
            anger = analyzer.plotlyEmotion(parser, parser.speakerDict.keys(), "anger")
            anticipation = analyzer.plotlyEmotion(parser, parser.speakerDict.keys(), "anticipation")
            disgust = analyzer.plotlyEmotion(parser, parser.speakerDict.keys(), "disgust")
            fear = analyzer.plotlyEmotion(parser, parser.speakerDict.keys(), "fear")
            joy = analyzer.plotlyEmotion(parser, parser.speakerDict.keys(), "joy")
            sadness = analyzer.plotlyEmotion(parser, parser.speakerDict.keys(), "sadness")
            trust = analyzer.plotlyEmotion(parser, parser.speakerDict.keys(), "trust")
            arr = [anger, anticipation, disgust, fear, joy, sadness, trust]

    else:
        form = DocumentForm() # A empty, unbound form

    return render(request, 'appTemps/results.html', {'arr': arr, 'score':score, 'convo':convo, 'cwords':cwords, 'arr2':arr2, "person": p})

"""
This method takes the person of interest to be inspected from the results page, as well as the "person" object
(which holds personalized data for each spealer) and sends this data to the person page.
"""
def person(request):
    if request.method == 'POST':
        print "Person being called"
        print(request.POST)
        prePerson = request.POST.get('person')
        person = json.loads(prePerson)
        emotBar = person['emotBar']
        name = person['pname']
    return render(
        request,
        'appTemps/person.html',
        {'person': prePerson, 'emotionJSON':emotBar, 'pname':name}
    )

def tags(request):
    print "Tags being called"
    if request.method == 'GET':
        tags = {
            'Anger': {},
            'Anticipation': {},
            'Disgust': {},
            'Fear': {},
            'Joy': {},
            'Sadness': {},
            'Trust': {},
        }
        tag_model = Result(tags=json.dumps({'tags': tags}))
        return HttpResponse(tag_model.tags, content_type='application/json')

def about(request):
    return render(request, 'appTemps/about.html')
