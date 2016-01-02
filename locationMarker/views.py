#-*- encoding=UTF-8 -*-
from django.shortcuts import render,  HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from random import randrange
from .forms import LocationForm,PhotoModelForm
from .models import Marker, DemoPhoto
from photos.models import Tag
import json

# Create your views here.
def editMarker (request):
	context = { 'marker_list':Marker.objects.all()};
	return render(request,'locationMarker/editMarker.html', context);

def post (request):

	titleList = request.POST.getlist('title');
	latList = request.POST.getlist('lat');
	lngList = request.POST.getlist('lng');
	allMarker = []
	if len(titleList) > 0:
		Marker.objects.all().delete();
	for i in range(len(titleList)):
		Marker.objects.create(title=titleList[i], latitude=latList[i], longitude=lngList[i]);
		allMarker.append({'title':titleList[i], 'latitude':latList[i], 'longitude':lngList[i]})
	context = {'pack':Marker.objects.all()};
	fp = open('allMarker.json','w')
	fp.write(json.dumps(allMarker))
	fp.close()
	return  HttpResponseRedirect(reverse('locationMarker:editMarker'));

def demo(request):
	url = 'https://farm6.staticflickr.com/5776/22094071913_a6f5c32200_z.jpg';
	DemoPhoto.objects.all().delete();
	markers = Marker.objects.order_by('?');
	for i in range(int(len(markers)*0.8)):
		DemoPhoto.objects.create(title='photo_{}'.format(i), url=url, marker=markers[i]);

	context = {'photoList':DemoPhoto.objects.all()};
	return  render(request, 'locationMarker/demo.html',context);

def test(request):

	marker_list = Marker.objects.all()
	form = PhotoModelForm()
	return render(request,'locationMarker/test.html',{'marker_list':marker_list,'form':form})

def ajax_getTagHint(request):
	context={}
	hotTags = Tag.objects.order_by('-tag_count')[0:5]
	recentTags = Tag.objects.order_by('-update_time')[0:5]
	context['hotTags'] = [(x.tag_name,x.tag_count) for x in hotTags]
	context['recentTags'] = [(x.tag_name,x.update_time) for x in recentTags]
	if request.method == 'POST':
		word = request.POST.get('word','')
		print word
		if word != '':
			similarTags = sorted(Tag.objects.all(),reverse=True, key= lambda x : x.similarity(word))
			index = 0;
			for i in range(5):
				if similarTags[i].similarity(word) <= 0:
					break;
				index=i+1
			context['similarTags'] = [(x.tag_name,x.similarity(word) )for x in similarTags[0:index]]
	return JsonResponse(context)
