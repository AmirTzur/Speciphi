from django.shortcuts import render
from collections import OrderedDict


# Create your views here.

def home(request):
    pages = OrderedDict()
    pages['Home'] = [True, "home"]
    pages['Affil'] = [False, "affiliation"]
    pages['Appli'] = [False, "application"]
    pages['Focal'] = [False, "focalization"]
    pages['Compar'] = [False, "comparison"]
    pages['Results'] = [False, "results"]

    context = {
        "pages": pages,
    }
    return render(request, "index.html", context)


def success_close(request):
    context = {
    }
    return render(request, "success_close.html", context)


def affiliation(request):
    pages = OrderedDict()
    pages['Home'] = [False, "home"]
    pages['Affil'] = [True, "affiliation"]
    pages['Appli'] = [False, "application"]
    pages['Focal'] = [False, "focalization"]
    pages['Compar'] = [False, "comparison"]
    pages['Results'] = [False, "results"]
    context = {
        "pages": pages,
    }
    return render(request, "affiliation.html", context)


def application(request):
    pages = OrderedDict()
    pages['Home'] = [False, "home"]
    pages['Affil'] = [False, "affiliation"]
    pages['Appli'] = [True, "application"]
    pages['Focal'] = [False, "focalization"]
    pages['Compar'] = [False, "comparison"]
    pages['Results'] = [False, "results"]
    context = {
        "pages": pages,
    }
    return render(request, "application.html", context)


def focalization(request):
    pages = OrderedDict()
    pages['Home'] = [False, "home"]
    pages['Affil'] = [False, "affiliation"]
    pages['Appli'] = [False, "application"]
    pages['Focal'] = [True, "focalization"]
    pages['Compar'] = [False, "comparison"]
    pages['Results'] = [False, "results"]
    context = {
        "pages": pages,
    }
    return render(request, "focalization.html", context)


def comparison(request):
    pages = OrderedDict()
    pages['Home'] = [False, "home"]
    pages['Affil'] = [False, "affiliation"]
    pages['Appli'] = [False, "application"]
    pages['Focal'] = [False, "focalization"]
    pages['Compar'] = [True, "comparison"]
    pages['Results'] = [False, "results"]
    context = {
        "pages": pages,
    }
    return render(request, "comparison.html", context)


def results(request):
    pages = OrderedDict()
    pages['Home'] = [False, "home"]
    pages['Affil'] = [False, "affiliation"]
    pages['Appli'] = [False, "application"]
    pages['Focal'] = [False, "focalization"]
    pages['Compar'] = [False, "comparison"]
    pages['Results'] = [True, "results"]
    context = {
        "pages": pages,
    }
    return render(request, "results.html", context)
