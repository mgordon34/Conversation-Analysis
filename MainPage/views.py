from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.urlresolvers import reverse

from MainPage.models import Document
from MainPage.models import Result
from MainPage.forms import DocumentForm
import TextParsing
import Analyze

import json
import numpy as np
import matplotlib.pyplot as plt

global arr, score, emoarr, cwords, arr2, p, cmpd
arr = None
score = None
emoarr = None
cwords = None
arr2 = None
p = None
cmpd = None
documents = None
form = None

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
    global arr, score, emoarr, cwords, arr2, p, cmpd
    if request.method == 'POST':
        # print "Results being called"
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            filename = (request.FILES['docfile'].name)
            parser = TextParsing.TextParsing(filename)
            analyzer = Analyze.Analyze()
            analyzer.popDialogEmotion(parser)
            analyzer.setDialogSentiment(parser)
            p = json.dumps(analyzer.getPersonData(parser), separators=(',', ':'))
            arr2 = parser.plotlyBarFreqDist("everyone")
            cmpd = analyzer.plotlyCompoundSenti(parser)
            score = analyzer.getAverageConversationScores(parser)
            emo1 = analyzer.getConversationScore(parser)["anger"]
            emo2 = analyzer.getConversationScore(parser)["anticipation"]
            emo3 = analyzer.getConversationScore(parser)["disgust"]
            emo4 = analyzer.getConversationScore(parser)["fear"]
            emo5 = analyzer.getConversationScore(parser)["joy"]
            emo6 = analyzer.getConversationScore(parser)["sadness"]
            emo7 = analyzer.getConversationScore(parser)["surprise"]
            emo8 = analyzer.getConversationScore(parser)["trust"]
            emoarr = [emo1, emo2, emo3, emo4, emo5, emo6, emo7, emo8]
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

    return render(request, 'appTemps/results.html', {'filename': filename, 'arr': arr, 'score':score, 'emoarr':emoarr, 'cwords':cwords, 'arr2':arr2, "person": p, "form": form, "documents": documents})

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

def doubleresults(request):
    global arr, score, emoarr, cwords, arr2, p, cmpd
    form = DocumentForm(request.POST, request.FILES)
    if form.is_valid():
        newdoc = Document(docfile = request.FILES['docfile'])
        newdoc.save()
        parser = TextParsing.TextParsing(request.FILES['docfile'].name)
        analyzer = Analyze.Analyze()
        analyzer.popDialogEmotion(parser)
        analyzer.setDialogSentiment(parser)
        anger = analyzer.plotlyEmotion(parser, parser.speakerDict.keys(), "anger")
        anticipation = analyzer.plotlyEmotion(parser, parser.speakerDict.keys(), "anticipation")
        disgust = analyzer.plotlyEmotion(parser, parser.speakerDict.keys(), "disgust")
        fear = analyzer.plotlyEmotion(parser, parser.speakerDict.keys(), "fear")
        joy = analyzer.plotlyEmotion(parser, parser.speakerDict.keys(), "joy")
        sadness = analyzer.plotlyEmotion(parser, parser.speakerDict.keys(), "sadness")
        trust = analyzer.plotlyEmotion(parser, parser.speakerDict.keys(), "trust")
        arr1 = [anger, anticipation, disgust, fear, joy, sadness, trust]
        cmpd1 = analyzer.plotlyCompoundSenti(parser)
    return render(request, 'appTemps/doubleresults.html', {'arr': arr, 'score':score, 'emoarr':emoarr, 'cwords':cwords, 'arr2':arr2, "person": p, 'arr1':arr1, 'cmpd1':cmpd1, 'cmpd':cmpd})

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

def save(request):
    print "Save being called"
    a = {'result': 'success'}
    if request.method == 'GET':
        print "Get request"
        data = {}
        try:
            with open('savedData.json') as f:
                data = json.load(f)
        except:
            pass
        with open('savedData.json', 'w') as f:
            print(type(request.GET))
            print(request.GET)
            data[request.GET['filename']] = request.GET
            f.write(json.dumps(data))
        return JsonResponse(a)

def doubletags(request):
    print "Double Tags being called"
    if request.method == 'GET':
        tags1 = {
            'Anger': {},
            'Anticipation': {},
            'Disgust': {},
            'Fear': {},
            'Joy': {},
            'Sadness': {},
            'Trust': {},
        }
        tag_model1 = Result(tags1=json.dumps({'tags1': tags1}))
        return HttpResponse(tag_model1.tags1, content_type='application/json')

def about(request):
    return render(request, 'appTemps/about.html')

def prevResults(request):
    with open('savedData.json') as data_file:
        data = json.load(data_file)
        convoData = data[request.POST.get('convoName')]
        arr=convoData['arr']
        score=convoData['score']
        emoarr=convoData['emoarr']
        cwords=convoData['cwords']
        arr2=convoData['arr2']
        p=convoData['person']
        return render(request, 'appTemps/results.html', {'arr': arr, 'score':score, 'emoarr':emoarr, 'cwords':cwords, 'arr2':arr2, "person": p})

