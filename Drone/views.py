from django.shortcuts import render, redirect
from .models import VictimDetails
from django.core import serializers
from django.http import JsonResponse


def index(request):
	if request.method == 'POST':
		name = request.POST.get('name')
		latitude = request.POST.get('lat')
		longitude = request.POST.get('long')
		phoneno = request.POST.get('phone')
		image = request.FILES.get('image')
		# print(name, latitude, longitude, phoneno, image)
		details = VictimDetails(name = name, phoneno = phoneno, latitude= latitude, longitude = longitude, image = image)
		details.save()
		return redirect('/')

	return render(request, "index.html")

def droneadmin(request):
	dronedetails = VictimDetails.objects.all()
	return render(request, "admin.html", {"dronedetails":dronedetails})

def admin_page_data(request):
	dronedetails = VictimDetails.objects.all().order_by('-published')
	data = serializers.serialize('json', dronedetails)
	resJson=[]
	for data in dronedetails:
		name = data.name
		latitude = data.latitude
		longitude = data.longitude
		phoneno = data.phoneno
		if data.image:
			image = str('/media/'+str(data.image))
		else:
			image = str('/static/img/accident1.jpg')
		
		resJson.append([name,latitude,longitude,phoneno,image])

	return JsonResponse(resJson, safe=False)