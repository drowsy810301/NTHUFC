#-*- encoding=UTF-8 -*-
from django.shortcuts import render,  HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from .models import Marker
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

	Marker.objects.exclude(title__in=titleList).delete()

	for i in range(len(titleList)):
		try:
			marker = Marker.objects.get(title=titleList[i])
			marker.latitude = latList[i]
			marker.longitude = lngList[i]
			marker.save()
		except ObjectDoesNotExist:
			Marker.objects.create(title=titleList[i], latitude=latList[i], longitude=lngList[i]);

		allMarker.append({'title':titleList[i], 'latitude':latList[i], 'longitude':lngList[i]})

	fp = open('allMarker.json','w')
	fp.write(json.dumps(allMarker))
	fp.close()
	return  HttpResponseRedirect(reverse('locationMarker:editMarker'));
