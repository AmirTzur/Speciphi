from random import random

from django.shortcuts import render
from collections import OrderedDict
from django.db import connection, Error
from consult.forms import AffiliationsForm
from django.http import HttpResponse
from consult.models import Affiliations
import xml.etree.ElementTree as ET
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
    print(product)
    if product:
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
                print()
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

        if Affiliations:
            form = AffiliationsForm(Affiliations_dict=Affiliations.objects.all())
        if ConsultationProcess_id:
            request.session['ConsultationProcess_id'] = ConsultationProcess_id[0]
        if Product_id:
            request.session['Product_id'] = Product_id

        # copy form input tags to Affiliations dict
        # check if instead of double loop, first take out the name attr from the input using xml parsing
        for f in form:
            for a in affiliations:
                if str(a['name']) in str(f):
                    a['form_input'] = str(f)
        # Get deals data for results feature and create dictionary of deals
        # for each results category: {sort_indicator: brand, model, image_url,
        #                                             offers[{deal_id, deal_url, vendor_name, price}, {}, ]}
        offers = [
            {'best_match': {'brand': 'Apple', 'model': 'Macbook Pro', 'image_url': 'http://ecx.images-amazon.com/images/I/41lmJ1hPMnL._SL160_.jpg',
                            'offers': [{'deal_id': 111, 'deal_url': 'http://www.amazon.com/gp/offer-listing/B00GZB8D0M%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-', 'vendor_name': 'Amazon',
                                        'price': 950}, {'deal_id': 222, 'deal_url': 'xxx', 'vendor_name': 'eBay',
                                                        'price': 1000}]
                            }
             },
            {'most_purchased': {'brand': 'Lenovo', 'model': 'Yoga 3', 'image_url': 'http://ecx.images-amazon.com/images/I/41238W8tcjL._SL160_.jpg',
                                'offers': [{'deal_id': 333, 'deal_url': 'http://www.amazon.com/gp/offer-listing/B00VQP3DNY%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-', 'vendor_name': 'Amazon',
                                           'price': 1050}, {'deal_id': 444, 'deal_url': 'xxx', 'vendor_name': 'eBay',
                                           'price': 1100}]
                                }
             },
            {'type_popular': {'brand': 'Dell', 'model': 'XPS', 'image_url': 'http://ecx.images-amazon.com/images/I/218dheiyUrL._SL160_.jpg',
                              'offers': [{'deal_id': 555, 'deal_url': 'http://www.amazon.com/gp/offer-listing/B00SQG3MQE%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-', 'vendor_name': 'Amazon',
                                         'price': 1150}, {'deal_id': 666, 'deal_url': 'xxx', 'vendor_name': 'eBay',
                                         'price': 1200}]
                              }
             },
            {'cost_effective': {'brand': 'Asus', 'model': 'Zenbook 133X', 'image_url': 'http://ecx.images-amazon.com/images/I/41-6oCGJqwL._SL160_.jpg',
                                'offers': [{'deal_id': 777, 'deal_url': 'http://www.amazon.com/gp/offer-listing/B01BLU6ERK%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-', 'vendor_name': 'Amazon',
                                           'price': 1250}, {'deal_id': 888, 'deal_url': 'xxx', 'vendor_name': 'eBay',
                                           'price': 1300}]
                                }
             },
            {'stylish': {'brand': 'Sony', 'model': 'Bomber 304', 'image_url': 'http://ecx.images-amazon.com/images/I/41sgEA0JL-L._SL160_.jpg',
                         'offers': [{'deal_id': 999, 'deal_url': 'http://www.amazon.com/gp/offer-listing/B018AX3YGU%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-', 'vendor_name': 'Amazon',
                                    'price': 1350}, {'deal_id': 121, 'deal_url': 'xxx', 'vendor_name': 'eBay',
                                    'price': 1400}]
                         }
             },
        ]
        total_results = 1435
        context.update({
            "Product_id": Product_id,
            "affiliationsLength": len(affiliations),
            "affiliations": affiliations,
            "ConsultationProcess_id": ConsultationProcess_id[0],
            "offers": offers,
            "total_results": total_results,
        })
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
    # Uses = OrderedDict()
    # for i in range(0, 8):
    #     Uses['id'] = i
    #     Uses['value'] = i
    #     Uses['name'] = 'Video editing ' + str(i)
    #     Uses[
    #         'description'] = 'A Person who selects and mixes dialogue, music and special audio effects in the preparation of an audio master for CDs' + i
    # context.update({'Uses': Uses})
    # value = models.IntegerField()
    # name = models.CharField(max_length=45, blank=True, null=True)
    # description = models.TextField()
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
    print('success_close|')
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
