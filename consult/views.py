from django.shortcuts import render
from collections import OrderedDict
from django.db import connection, Error
from consult.forms import AffiliationsForm
from django.http import HttpResponse
from consult.models import Affiliations
import xml.etree.ElementTree as ET
import json


def home(request):
    pages = OrderedDict()
    pages['Home'] = [True, "home"]
    pages['Affil'] = [False, "affiliation"]
    pages['Appli'] = [False, "application"]
    pages['Focal'] = [False, "focalization"]
    pages['Compar'] = [False, "comparison"]
    pages['Results'] = [False, "results"]

    if 'Entrance_id' not in request.session:
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
                Entrance_id = cursor.fetchone()
                cursor.close()
                if Entrance_id:
                    request.session['Entrance_id'] = Entrance_id[0]
                    print("new Entrance, Entrance_id set to " + str(request.session['Entrance_id']))
        except Error as e:
            print(e)
    else:
        print("Entrance_id was already set to " + str(request.session['Entrance_id']))
    context = {
        "pages": pages,
        "product": "None",
    }
    return render(request, "index.html", context)


def affiliation(request, product=None):
    pages = OrderedDict()
    pages['Home'] = [False, "home"]
    pages['Affil'] = [True, "affiliation"]
    pages['Appli'] = [False, "application"]
    pages['Focal'] = [False, "focalization"]
    pages['Compar'] = [False, "comparison"]
    pages['Results'] = [False, "results"]

    context = {
        "pages": pages,
        "product": product,
    }
    if product == 'Laptop':
        Product_id = 2  # Laptop product ID
        # connect to djarooDB
        try:
            cursor = connection.cursor()
            if not cursor:
                print("cursor was not defined")
            else:
                # Input: Product_id
                # Output: id, Affiliations names, descriptions and images
                cursor.execute('CALL getProductAffiliations(%s)', [Product_id])
                affiliations = dictfetchall(cursor)
                cursor.close()

            cursor = connection.cursor()
            if not cursor:
                print("cursor was not defined")
            else:
                # Input: Entrance_id, Product_id
                # Output: Creates new entry in "consultationProcesses" Table
                cursor.execute('CALL setNewConsultationProcess(%s,%s)', [request.session['Entrance_id'], Product_id])
                cursor.close()

            cursor = connection.cursor()
            if not cursor:
                print("cursor was not defined")
            else:
                # Input: Entrance_id
                # Output: ConsultationProcess_id
                cursor.execute('CALL getConsultationProcessId(%s)', [request.session['Entrance_id']])
                ConsultationProcess_id = cursor.fetchone()
                cursor.close()
        except Error as e:
            print(e)

        request.session['Product_id'] = Product_id
        if ConsultationProcess_id:
            request.session['ConsultationProcess_id'] = ConsultationProcess_id[0]

        form = AffiliationsForm(Affiliations_dict=Affiliations.objects.all())
        print("iterate form:")
        for f in form:
            print(type(f), f)
        # transfer form input tags through affiliations dict
        # check if instead of the following, first take out the name attr from the input using xml parsing
        for f in form:
            for a in affiliations:
                if str(a['name']) in str(f):
                    a['form_input'] = str(f)

        context.update({
            "Product_id": Product_id,
            "affiliationsLength": len(affiliations),
            "affiliations": affiliations,
            "ConsultationProcess_id": ConsultationProcess_id[0],
        })
    return render(request, "affiliation.html", context)

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.


# https://docs.djangoproject.com/en/1.8/intro/tutorial04/

def application(request, product=None):
    if request.method == "POST":
        print("Application|post method submitted")
        form = AffiliationsForm(request.POST)
        # if form.is_valid():
        # print(form)
        # form_str = '<div>' + str(form) + '</div>'
        # tree = ET.ElementTree(ET.fromstring(form_str))
        # for node in tree.getiterator():
        #     print(tree)
        # else:
        # print("form is not valid")
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


# return results as a dict with key names
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]


def NewConsulteeAffiliation(request):
    print('Views: NewConsulteeAffiliation')
    if request.method == 'POST':
        Affiliation_id = request.POST.get('Affiliation_id')
        checked = request.POST.get('checked')
        print('Affiliation_id: ' + Affiliation_id + '. checked: ' + checked)
        response_data = {}  # hold the data that will send back to client
        try:
            cursor = connection.cursor()
            if not cursor:
                print("cursor was not defined")
            else:
                # Input: Entrance_id, Product_id, ConsultationProcess_id, Affiliation_id , Checked
                # Output: Creates new entry in the: "consulteeAffiliations" Table
                cursor.execute('CALL setNewConsulteeAffiliation(%s,%s,%s,%s,%s)',
                               [request.session['Entrance_id'],
                                request.session['Product_id'],
                                request.session['ConsultationProcess_id'],
                                Affiliation_id,
                                checked])
                cursor.close()
        except Error as e:
            print(e)

        response_data['result'] = 'Create post successful!'
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"failed": "request POST didn't go through"}),
            content_type="application/json"
        )
