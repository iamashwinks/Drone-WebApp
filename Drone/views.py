from django.shortcuts import render, redirect
from .models import VictimDetails

def index(request):
	if request.method == 'POST':
		name = request.POST.get('name')
		latitude = request.POST.get('lat')
		longitude = request.POST.get('long')
		phoneno = request.POST.get('phone')
		image = request.FILES.get('image')
		print(name, phoneno)
		details = VictimDetails(name = name, phoneno = phoneno, latitude= latitude, longitude = longitude, image = image)
		details.save()
		return redirect('/home/')

	return render(request, "index.html")

def droneadmin(request):
	dronedetails = VictimDetails.objects.all()
	return render(request, "admin.html", {"dronedetails":dronedetails})