from django.shortcuts import render



def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def admission(request):
    return render(request, 'Admission.html')


def activities(request):
    return render(request, 'activities.html')


def announcements(request):
    return render(request, 'announcements.html')


def fees(request):
    return render(request, 'fees.html')

def contact(request):
    return render(request,'ContactUs.html')

