from django.shortcuts import render, redirect
from .models import VictimDetails
from django.core import serializers
from django.http import JsonResponse

import requests

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
		data_id = data.id
		name = data.name
		latitude = data.latitude
		longitude = data.longitude
		phoneno = data.phoneno
		if data.image:
			image = str('/media/'+str(data.image))
		else:
			image = str('/static/img/accident1.jpg')
		
		resJson.append([name,latitude,longitude,phoneno,image, data_id])

	return JsonResponse(resJson, safe=False)
	
def victim_page(request,details_id):
	return render(request, "victim_details.html", {"victim_details":details_id})


def victim_details(request, details_id):
	resJson=[]
	detailview = VictimDetails.objects.get(pk=details_id)
	data_id = detailview.id
	name = detailview.name
	latitude = detailview.latitude
	longitude = detailview.longitude
	phoneno = detailview.phoneno
	if detailview.image:
		image = str('media/'+str(detailview.image))
	else:
		image = str('static/img/accident1.jpg')
	url = 'https://app.nanonets.com/api/v2/ImageCategorization/LabelFile/'
	data = {'file': open(image, 'rb'), 'modelId': ('', 'deaea15e-1972-4b5d-9645-b514af09b3ca')}
	response = requests.post(url, auth= requests.auth.HTTPBasicAuth('L8pFSWMtPqAXddoDCP1OV34npFqPk2RH', ''), files=data).json()
	num1 = response['result'][0]['prediction'][0]['probability']
	num2 = response['result'][0]['prediction'][1]['probability']
	num3 = response['result'][0]['prediction'][2]['probability']
	
	if (num1 > num2) and (num1 > num3):
	   label = str('static/img/warning3.png')
	elif (num2 > num1) and (num2 > num3):
	   label = str('static/img/warning2.png')
	else:
	   label = str('static/img/warning1.png')
	resJson.append({'id':data_id,'name':name,'latitude':latitude,'longitude':longitude,'phoneno':phoneno,'image':image,'label':label })

	return JsonResponse(resJson, safe=False)

