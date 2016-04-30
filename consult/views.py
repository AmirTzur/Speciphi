from django.shortcuts import render
from collections import OrderedDict
from django.db import connection, Error
from consult.forms import AffiliationsForm
from consult.models import Affiliations


# Create your views here.

def home(request):
    pages = OrderedDict()
    pages['Home'] = [True, "home"]
    pages['Affil'] = [False, "affiliation"]
    pages['Appli'] = [False, "application"]
    pages['Focal'] = [False, "focalization"]
    pages['Compar'] = [False, "comparison"]
    pages['Results'] = [False, "results"]

    if 'entrance_id' not in request.session:
        # get user ip
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            user_ip = x_forwarded_for.split(',')[0]
        else:
            user_ip = request.META.get('REMOTE_ADDR')
        # connect to djarooDB
        try:
            cursor = connection.cursor()
            if not cursor:
                print("cursor was not defined")
            else:
                # Input: Entrance_ip, Entrance_country
                # Output: Creates new entry in “Entrances” Table, Entrance_id
                cursor.execute('call newEntrance(%s,"")', [user_ip])
                entrance_id = cursor.fetchone()
                cursor.close()
                if entrance_id:
                    request.session['entrance_id'] = entrance_id[0]
                    print("new Entrance, entrance_id set to " + str(request.session['entrance_id']))
        except Error as e:
            print(e)
    else:
        print("entrance_id was already set to " + str(request.session['entrance_id']))
    context = {
        "pages": pages,
        "product": "None",
    }
    return render(request, "index.html", context)


# return results as a dict with key names
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]


def affiliation(request, product=None):
    pages = OrderedDict()
    pages['Home'] = [False, "home"]
    pages['Affil'] = [True, "affiliation"]
    pages['Appli'] = [False, "application"]
    pages['Focal'] = [False, "focalization"]
    pages['Compar'] = [False, "comparison"]
    pages['Results'] = [False, "results"]

    # form = AffiliationsForm(request.POST or None)
    # if form.Student:
    #     print('form')
    # else:
    #     print('!form')
    # for f in form:
    #     print(f)

    context = {
        "pages": pages,
        "product": product,
        # "form": form,
    }
    if product == 'Laptop':
        productID = 2  # Laptop product ID
        # connect to djarooDB
        try:
            cursor = connection.cursor()
            if not cursor:
                print("cursor was not defined")
            else:
                # Input: Product_id
                # Output: Affiliations names, descriptions and images
                cursor.execute('CALL getProductAffiliations(%s)', [productID])
                affiliations = dictfetchall(cursor)
                cursor.close()

            cursor = connection.cursor()
            if not cursor:
                print("cursor was not defined")
            else:
                # Input: Entrance_id, Product_id
                # Output: Creates new entry in "consultationProcesses" Table
                cursor.execute('CALL setNewConsultationProcess(%s,%s)', [request.session['entrance_id'], productID])
                cursor.close()

            cursor = connection.cursor()
            if not cursor:
                print("cursor was not defined")
            else:
                # Input: Entrance_id
                # Output: ConsultationProcess_id
                cursor.execute('CALL getConsultationProcessId(%s)', [request.session['entrance_id']])
                consultationProcess_id = cursor.fetchone()
                cursor.close()
        except Error as e:
            print(e)
        request.session['productID'] = productID
        context.update({
            "productID": productID,
            "affiliationsLength": len(affiliations),
            "affiliations": affiliations,
            "consultationProcess_id": consultationProcess_id[0],
        })
    return render(request, "affiliation.html", context)

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.


# https://docs.djangoproject.com/en/1.8/intro/tutorial04/

def application(request, product=None):
    if request.method == "POST":
        print("post method submitted " + product)
        # affs = Affiliations.objects.all()
        # for aff in affs:
        #     print(aff.name+"_box")
    elif request.method == "GET":
        print("get method submitted " + product)
    pages = OrderedDict()
    pages['Home'] = [False, "home"]
    pages['Affil'] = [False, "affiliation"]
    pages['Appli'] = [True, "application"]
    pages['Focal'] = [False, "focalization"]
    pages['Compar'] = [False, "comparison"]
    pages['Results'] = [False, "results"]
    context = {
        "pages": pages,
        "product": product,
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


def success_close(request):
    context = {
    }
    return render(request, "success_close.html", context)
