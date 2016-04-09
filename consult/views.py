from django.shortcuts import render
from collections import OrderedDict
from django.db import connection, Error


# Create your views here.

def home(request):
    pages = OrderedDict()
    pages['Home'] = [True, "home"]
    pages['Affil'] = [False, "affiliation"]
    pages['Appli'] = [False, "application"]
    pages['Focal'] = [False, "focalization"]
    pages['Compar'] = [False, "comparison"]
    pages['Results'] = [False, "results"]
    # get user ip
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        user_ip = x_forwarded_for.split(',')[0]
    else:
        user_ip = request.META.get('REMOTE_ADDR')
    params = [user_ip]
    # connect to djaroo.db
    try:
        cursor = connection.cursor()
        cursor.execute('call newEntrance(%s,"")', [params])
        row_fetched = cursor.fetchone()
        if cursor:
            print("fetched row:")
            print(row_fetched)
            print("fetched row type:")
            print(type(row_fetched))
            request.session['user_id'] = row_fetched[0]
            print("home View, session['user_id']: ")
            print(request.session['user_id'])
        else:
            print("cursor is not defined")
    except Error as e:
        print(e)

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
    print('affiliation View, session["user_id"]:')
    print(request.session['user_id'])
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
