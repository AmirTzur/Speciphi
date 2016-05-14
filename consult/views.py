from django.shortcuts import render
from collections import OrderedDict
from django.db import connection, Error
from django.utils.datastructures import OrderedSet

from consult.forms import AffiliationsForm, UsesForm
from django.http import HttpResponse
from consult.models import Levelofuse
import json


def home(request):
    print('home|')
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
                # Output: Creates new entry in Entrances Table, Entrance_id
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
    print('affiliation|')
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
        Product_id = 1  # Laptop product ID

    if Product_id:
        # connect to djarooDB
        try:
            cursor = connection.cursor()
            if not cursor:
                print("cursor was not defined")
            else:
                # Input: Product_id
                # Output: Affiliations - id, Affiliations names, descriptions and images
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

        if Product_id:
            request.session['Product_id'] = Product_id
        if affiliations:
            form = AffiliationsForm(affiliations_dict=affiliations)
            # copy form input tags to Affiliations dict
            # check if instead of double loop, first take out the name attr from the input using xml parsing
            for f in form:
                for a in affiliations:
                    if str(a['name']) in str(f):
                        a['form_input'] = str(f)
            context.update({
                "affiliations": affiliations,
            })
        if ConsultationProcess_id:
            request.session['ConsultationProcess_id'] = ConsultationProcess_id[0]

    return render(request, "affiliation.html", context)

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    # https://docs.djangoproject.com/en/1.8/intro/tutorial04/


def application(request, product=None):
    if request.method == "POST":
        print("application| POST")
    elif request.method == "GET":
        print("Application| GET")
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

    # get Uses ids (change to SQL exec)
    uses_ids_string = "1,2,3,4,5,7,9,11"
    uses_ids = uses_ids_string.split(",")

    # get Uses values (change to SQL exec)
    uses_values_string = "12312312"
    uses_values = list(uses_values_string)

    # get relevant Uses (by id) from db
    uses = ValuesQuerySetToDict(Levelofuse.objects.all().filter(Uses_id__in=uses_ids).values())
    if uses:
        # create inputs
        form = UsesForm(uses_dict=uses)
        # take form inputs and append them to relevant uses
        for f in form:
            for use in uses:
                if str(use['Uses_name'] + str(use['value'])) in str(f):
                    use['form_input'] = str(f)
        # create data structure to present uses on template
        template_uses = []
        i = 0
        j = 0
        for use in uses:
            if i % 3 == 0:
                # insert 3 uses with different values
                template_uses.append({
                    "Uses_id": use['Uses_id'],
                    "Uses_name": use['Uses_name'],
                    "show_level": uses_values[j],  # approximate use by taltul
                    "levels": [
                        {
                            "id": uses[i]['id'],
                            "value": uses[i]['value'],
                            "description": uses[i]['description'],
                            "form_input": uses[i]['form_input']
                        },
                        {
                            "id": uses[i + 1]['id'],
                            "value": uses[i + 1]['value'],
                            "description": uses[i + 1]['description'],
                            "form_input": uses[i + 1]['form_input']
                        },
                        {
                            "id": uses[i + 2]['id'],
                            "value": uses[i + 2]['value'],
                            "description": uses[i + 2]['description'],
                            "form_input": uses[i + 2]['form_input']
                        },
                    ],
                })
                j += 1
            i += 1
        context.update({
            "template_uses": template_uses,
        })

    return render(request, "application.html", context)


def focalization(request, product=None):
    pages = OrderedDict()
    pages['Home'] = [False, "home"]
    pages['Affil'] = [False, "affiliation"]
    pages['Appli'] = [False, "application"]
    pages['Focal'] = [True, "focalization"]
    pages['Compar'] = [False, "comparison"]
    pages['Results'] = [False, "results"]
    context = {
        "pages": pages,
        "product": product,
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
    print('success_close|')
    context = {
    }
    return render(request, "success_close.html", context)


def ValuesQuerySetToDict(vqs):
    return [item for item in vqs]


# return results as a dict with key names
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]


def NewConsulteeAffiliation(request):
    print('NewConsulteeAffiliation|')
    if request.method == 'POST':
        Affiliation_id = request.POST.get('Affiliation_id')
        checked = request.POST.get('checked')
        response_data = {}  # hold the data that will send back to client (for future use)
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
