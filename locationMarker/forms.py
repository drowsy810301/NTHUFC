from django import forms
from .models import Marker
from photos.models import Photo

def getAllMarker():
	marker_list = []
	for obj in  Marker.objects.all():
		marker_list.append((obj.id,obj.title))
	return marker_list

class LocationForm(forms.Form):
	choices = [(1,'one'), (2,'two')]
	location = forms.ChoiceField(label='Location Marker',help_text='click the map or select a label\n',choices=getAllMarker())

class PhotoModelForm(forms.ModelForm):
	class Meta:
		model = Photo
		fields = ['title', 'content', 'owner', 'tags', 'location_marker','image']

	def __init__(self, *args, **kwargs):
		super(PhotoModelForm, self).__init__(*args, **kwargs)
		self.fields['tags'].widget = forms.HiddenInput()



