from django.shortcuts import render

from .forms import FeedbackForm
# Create your views here.

def test(request):
	if request.method=='POST':
		form = FeedbackForm(request.POST)
		if form.is_valid():
			print form.cleaned_data['email']
			print form.cleaned_data['type']
			print form.cleaned_data['message']
	else:
		form = FeedbackForm()

	return render(request,"feedback/test.html",{'form':form})
