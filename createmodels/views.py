from django.shortcuts import render

# Create your views here.


def create_model(request):
	return render(request,"createmodels.html")
