from django.core.files import File
from django.shortcuts import render, redirect
from django.db import connection, Error
from django.template.loader import get_template
from django.template import RequestContext, Template
from django.core.mail import EmailMessage
from django.template import Context
from consult.forms import AffiliationsForm, UsesForm, QuestionsForm, ContactForm, FilterForm
from django.http import HttpResponse
# from consult.models import Levelofuse
from collections import OrderedDict
import urllib.request
import json
import pickle
import string
from consult.utils import Classifier
import pandas as pd


def home(request):
    print('home|')
    pages = OrderedDict()
    pages['Home'] = [True, "home"]
    pages['Affil'] = [False, "affiliation"]
    pages['Appli'] = [False, "application"]
    pages['Focal'] = [False, "focalization"]
    pages['Compar'] = [False, "comparison"]
    pages['Results'] = [False, "results"]

    # new user
    user_location = None
    if 'Entrance_id' not in request.session:
        # get user ip
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            user_ip = x_forwarded_for.split(',')[0]
        else:
            user_ip = request.META.get('REMOTE_ADDR')
        f = urllib.request.urlopen('http://ip-api.com/json/' + str(user_ip))
        # get location by ip
        geo_data = f.read()
        f.close()
        geo_dict = json.loads(geo_data.decode('UTF-8'))
        if geo_dict['status'] == 'success':
            user_location = str(geo_dict['country'] + ', ' + geo_dict['city'])

        # connect to djarooDB
        try:
            cursor = connection.cursor()
            if not cursor:
                print("cursor was not defined")
            else:
                # Input: Entrance_ip, Entrance_country
                # Output: Creates new entry in Entrances Table, Entrance_id
                if user_location:
                    cursor.execute('call newEntrance(%s,%s)', [user_ip, user_location])
                else:
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
        # copy form input tags to Affiliations dict
        # check if instead of double loop, first take out the name attr from the input using xml parsing
        for f in form:
            for a in affiliations:
                if str(a['name']) in str(f):
                    a['form_input'] = str(f)
        # Get deals data for results feature and create dictionary of deals
        # for each results category: {sort_indicator: brand, model, image_url,
        # offers[{deal_id, deal_url, vendor_name, price}, {}, ]}
        offers = [
            {'sort_indicator': 'Best Match', 'brand': 'Apple', 'model': 'Macbook Pro',
             'image_url': 'http://ecx.images-amazon.com/images/I/41lmJ1hPMnL._SL160_.jpg',
             'offers': [{'deal_id': 111,
                         'deal_url': 'http://www.amazon.com/gp/offer-listing/B00GZB8D0M%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-',
                         'vendor_name': 'Amazon',
                         'price': 950}, {'deal_id': 222, 'deal_url': 'xxx', 'vendor_name': 'eBay', 'price': 1000}]
             },
            {'sort_indicator': 'Most Purchased', 'brand': 'Lenovo', 'model': 'Yoga 3',
             'image_url': 'http://ecx.images-amazon.com/images/I/41238W8tcjL._SL160_.jpg',
             'offers': [{'deal_id': 333,
                         'deal_url': 'http://www.amazon.com/gp/offer-listing/B00VQP3DNY%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-',
                         'vendor_name': 'Amazon',
                         'price': 1050}, {'deal_id': 444, 'deal_url': 'xxx', 'vendor_name': 'eBay', 'price': 1100}]
             },
            {'sort_indicator': 'Type Popular', 'brand': 'Dell', 'model': 'XPS',
             'image_url': 'http://ecx.images-amazon.com/images/I/218dheiyUrL._SL160_.jpg',
             'offers': [{'deal_id': 555,
                         'deal_url': 'http://www.amazon.com/gp/offer-listing/B00SQG3MQE%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-',
                         'vendor_name': 'Amazon',
                         'price': 1150}, {'deal_id': 666, 'deal_url': 'xxx', 'vendor_name': 'eBay', 'price': 1200}]
             },
            {'sort_indicator': 'Cost Effective', 'brand': 'Asus', 'model': 'Zenbook 133X',
             'image_url': 'http://ecx.images-amazon.com/images/I/41-6oCGJqwL._SL160_.jpg',
             'offers': [{'deal_id': 777,
                         'deal_url': 'http://www.amazon.com/gp/offer-listing/B01BLU6ERK%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-',
                         'vendor_name': 'Amazon',
                         'price': 1250}, {'deal_id': 888, 'deal_url': 'xxx', 'vendor_name': 'eBay', 'price': 1300}]
             },
            {'sort_indicator': 'Stylish', 'brand': 'Sony', 'model': 'Bomber 304',
             'image_url': 'http://ecx.images-amazon.com/images/I/41sgEA0JL-L._SL160_.jpg',
             'offers': [{'deal_id': 999,
                         'deal_url': 'http://www.amazon.com/gp/offer-listing/B018AX3YGU%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-',
                         'vendor_name': 'Amazon',
                         'price': 1350}, {'deal_id': 121, 'deal_url': 'xxx', 'vendor_name': 'eBay', 'price': 1400}]
             },
        ]
        total_results = 1435
        # Get page Title and Description
        page_title = 'Choose your type'
        page_desc = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. ' \
                    'Donec in maximus augue. Quisque euismod euismod posuere. ' \
                    'Phasellus tempor.'
        information_content = {
            "statistic": [
                "S1-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam."],
            "insight": [
                "I1-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.",
                "I2-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.",
                "I3-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam."],
            "objective": [
                "O11-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.",
                "O2-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam."]
        }
        context.update({
            "Product_id": Product_id,
            "affiliationsLength": len(affiliations),
            "affiliations": affiliations,
            "ConsultationProcess_id": ConsultationProcess_id[0],
            "offers": offers[0:3],
            "total_results": total_results,
            "page_title": page_title,
            "page_desc": page_desc,
            "information_content": information_content,
        })
    return render(request, "affiliation.html", context)

    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    # https://docs.djangoproject.com/en/1.8/intro/tutorial04/


def application(request, product=None):
    print('application|')
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
                            "form_input": uses[i]['form_input'],
                            "level_text": "Low",
                        },
                        {
                            "id": uses[i + 1]['id'],
                            "value": uses[i + 1]['value'],
                            "description": uses[i + 1]['description'],
                            "form_input": uses[i + 1]['form_input'],
                            "level_text": "Med",
                        },
                        {
                            "id": uses[i + 2]['id'],
                            "value": uses[i + 2]['value'],
                            "description": uses[i + 2]['description'],
                            "form_input": uses[i + 2]['form_input'],
                            "level_text": "High",
                        },
                    ],
                })
                j += 1
            i += 1
        offers = [
            {'sort_indicator': 'Best Match', 'brand': 'Apple', 'model': 'Macbook Pro',
             'image_url': 'http://ecx.images-amazon.com/images/I/41lmJ1hPMnL._SL160_.jpg',
             'offers': [{'deal_id': 111,
                         'deal_url': 'http://www.amazon.com/gp/offer-listing/B00GZB8D0M%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-',
                         'vendor_name': 'Amazon',
                         'price': 950}, {'deal_id': 222, 'deal_url': 'xxx', 'vendor_name': 'eBay', 'price': 1000}]
             },
            {'sort_indicator': 'Most Purchased', 'brand': 'Lenovo', 'model': 'Yoga 3',
             'image_url': 'http://ecx.images-amazon.com/images/I/41238W8tcjL._SL160_.jpg',
             'offers': [{'deal_id': 333,
                         'deal_url': 'http://www.amazon.com/gp/offer-listing/B00VQP3DNY%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-',
                         'vendor_name': 'Amazon',
                         'price': 1050}, {'deal_id': 444, 'deal_url': 'xxx', 'vendor_name': 'eBay', 'price': 1100}]
             },
            {'sort_indicator': 'Type Popular', 'brand': 'Dell', 'model': 'XPS',
             'image_url': 'http://ecx.images-amazon.com/images/I/218dheiyUrL._SL160_.jpg',
             'offers': [{'deal_id': 555,
                         'deal_url': 'http://www.amazon.com/gp/offer-listing/B00SQG3MQE%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-',
                         'vendor_name': 'Amazon',
                         'price': 1150}, {'deal_id': 666, 'deal_url': 'xxx', 'vendor_name': 'eBay', 'price': 1200}]
             },
            {'sort_indicator': 'Cost Effective', 'brand': 'Asus', 'model': 'Zenbook 133X',
             'image_url': 'http://ecx.images-amazon.com/images/I/41-6oCGJqwL._SL160_.jpg',
             'offers': [{'deal_id': 777,
                         'deal_url': 'http://www.amazon.com/gp/offer-listing/B01BLU6ERK%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-',
                         'vendor_name': 'Amazon',
                         'price': 1250}, {'deal_id': 888, 'deal_url': 'xxx', 'vendor_name': 'eBay', 'price': 1300}]
             },
            {'sort_indicator': 'Stylish', 'brand': 'Sony', 'model': 'Bomber 304',
             'image_url': 'http://ecx.images-amazon.com/images/I/41sgEA0JL-L._SL160_.jpg',
             'offers': [{'deal_id': 999,
                         'deal_url': 'http://www.amazon.com/gp/offer-listing/B018AX3YGU%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-',
                         'vendor_name': 'Amazon',
                         'price': 1350}, {'deal_id': 121, 'deal_url': 'xxx', 'vendor_name': 'eBay', 'price': 1400}]
             },
        ]
        total_results = 1435
        # Get page Title and Description
        page_title = 'Choose your uses'
        page_desc = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. ' \
                    'Donec in maximus augue. Quisque euismod euismod posuere. ' \
                    'Phasellus tempor.'
        information_content = {
            "statistic": [
                "S1-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam."],
            "insight": [
                "I1-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.",
                "I2-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.",
                "I3-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam."],
            "objective": [
                "O11-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.",
                "O2-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam."]
        }
        context.update({
            "template_uses": template_uses,
            "offers": offers[0:3],
            "total_results": total_results,
            "page_title": page_title,
            "page_desc": page_desc,
            "information_content": information_content,
        })

    return render(request, "application.html", context)


def focalization(request, product=None):
    print('focalization|')
    pages = OrderedDict()
    pages['Home'] = [False, "home"]
    pages['Affil'] = [False, "affiliation"]
    pages['Appli'] = [False, "application"]
    pages['Focal'] = [True, "focalization"]
    pages['Compar'] = [False, "comparison"]
    pages['Results'] = [False, "results"]
    offers = [
        {'sort_indicator': 'Best Match', 'brand': 'Apple', 'model': 'Macbook Pro',
         'image_url': 'http://ecx.images-amazon.com/images/I/41lmJ1hPMnL._SL160_.jpg',
         'offers': [{'deal_id': 111,
                     'deal_url': 'http://www.amazon.com/gp/offer-listing/B00GZB8D0M%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-',
                     'vendor_name': 'Amazon',
                     'price': 950}, {'deal_id': 222, 'deal_url': 'xxx', 'vendor_name': 'eBay', 'price': 1000}]
         },
        {'sort_indicator': 'Most Purchased', 'brand': 'Lenovo', 'model': 'Yoga 3',
         'image_url': 'http://ecx.images-amazon.com/images/I/41238W8tcjL._SL160_.jpg',
         'offers': [{'deal_id': 333,
                     'deal_url': 'http://www.amazon.com/gp/offer-listing/B00VQP3DNY%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-',
                     'vendor_name': 'Amazon',
                     'price': 1050}, {'deal_id': 444, 'deal_url': 'xxx', 'vendor_name': 'eBay', 'price': 1100}]
         },
        {'sort_indicator': 'Type Popular', 'brand': 'Dell', 'model': 'XPS',
         'image_url': 'http://ecx.images-amazon.com/images/I/218dheiyUrL._SL160_.jpg',
         'offers': [{'deal_id': 555,
                     'deal_url': 'http://www.amazon.com/gp/offer-listing/B00SQG3MQE%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-',
                     'vendor_name': 'Amazon',
                     'price': 1150}, {'deal_id': 666, 'deal_url': 'xxx', 'vendor_name': 'eBay', 'price': 1200}]
         },
        {'sort_indicator': 'Cost Effective', 'brand': 'Asus', 'model': 'Zenbook 133X',
         'image_url': 'http://ecx.images-amazon.com/images/I/41-6oCGJqwL._SL160_.jpg',
         'offers': [{'deal_id': 777,
                     'deal_url': 'http://www.amazon.com/gp/offer-listing/B01BLU6ERK%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-',
                     'vendor_name': 'Amazon',
                     'price': 1250}, {'deal_id': 888, 'deal_url': 'xxx', 'vendor_name': 'eBay', 'price': 1300}]
         },
        {'sort_indicator': 'Stylish', 'brand': 'Sony', 'model': 'Bomber 304',
         'image_url': 'http://ecx.images-amazon.com/images/I/41sgEA0JL-L._SL160_.jpg',
         'offers': [{'deal_id': 999,
                     'deal_url': 'http://www.amazon.com/gp/offer-listing/B018AX3YGU%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-',
                     'vendor_name': 'Amazon',
                     'price': 1350}, {'deal_id': 121, 'deal_url': 'xxx', 'vendor_name': 'eBay', 'price': 1400}]
         },
    ]
    total_results = 1435
    # Get page Title and Description
    page_title = 'Choose your focal'
    page_desc = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. ' \
                'Donec in maximus augue. Quisque euismod euismod posuere. ' \
                'Phasellus tempor.'
    information_content = {
        "statistic": [
            "S1-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam."],
        "insight": [
            "I1-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.",
            "I2-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.",
            "I3-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam."],
        "objective": [
            "O11-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.",
            "O2-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam."]
    }
    context = {
        "pages": pages,
        "offers": offers[0:3],
        "total_results": total_results,
        "product": product,
        "page_title": page_title,
        "page_desc": page_desc,
        "information_content": information_content,
    }

    questions = [
        {
            "general_name": "Screen",
            "id": 1,
            "my_questions": [
                {
                    "q_id": 1,
                    "title": "Screen type",
                    "question": "what would be the best screen type for ya?",
                    "answers": ["mat", "flat", "something else"]},
                {
                    "q_id": 2,
                    "title": "Screen resolution",
                    "question": "do you fucking care about res?",
                    "answers": ["Yes Sir!", "No Sir!", "Fuck You Sir!"]},
                {
                    "q_id": 3,
                    "title": "Screen therapy",
                    "question": "Does your eyes hurts?",
                    "answers": ["most of the day", "NEVER!"]},
            ]
        },
        {
            "general_name": "Warranty",
            "id": 2,
            "my_questions": [
                {
                    "q_id": 1,
                    "title": "Warranty type",
                    "question": "what would be the best Warranty type for ya?",
                    "answers": ["Good one", "Bad one", "will not tell!"]},
                {
                    "q_id": 2,
                    "title": "Warranty period",
                    "question": "do you fucking care about warranty?",
                    "answers": ["long one", "short"]},
                {
                    "q_id": 3,
                    "title": "free Warranty",
                    "question": "Would you like that?",
                    "answers": ["no", "free", "stuff"]}
            ]
        },
        {
            "general_name": "Connections",
            "id": 4,
            "my_questions": [
                {
                    "q_id": 1,
                    "title": "Accessories 1",
                    "question": "How much would you use external accessories with your product?",
                    "answers": ["Only the laptop itself", "Averagely", "Most of the time"]},
                {
                    "q_id": 2,
                    "title": "Connections 2",
                    "question": "do you fucking care about connections?",
                    "answers": ["lots", "not a lot"]},
                {
                    "q_id": 3,
                    "title": "Connections 3",
                    "question": "Would you like that connected?",
                    "answers": ["no", "yes", "not sure!"]}
            ]
        },
        {
            "general_name": "Special Needs",
            "id": 5,
            "my_questions": [
                {
                    "q_id": 1,
                    "title": "Special 1",
                    "question": "1 How much would you use external Special with your product?",
                    "answers": ["Only the laptop itself", "Averagely", "Most of the time"]},
                {
                    "q_id": 2,
                    "title": "Special 2",
                    "question": "2 do you fucking care about Special?",
                    "answers": ["lots", "not a lot"]},
                {
                    "q_id": 3,
                    "title": "Special 3",
                    "question": "3 Would you like that Special?",
                    "answers": ["no", "yes", "not sure!"]}
            ]
        },
        {
            "general_name": "Dimensions",
            "id": 7,
            "my_questions": [
                {
                    "q_id": 1,
                    "title": "Dimensions 1",
                    "question": "1 How much would you use Dimensions with your product?",
                    "answers": ["Only the laptop itself", "Averagely", "Most of the time"]},
                {
                    "q_id": 2,
                    "title": "Dimensions 2",
                    "question": "2 do you fucking care about Dimensions?",
                    "answers": ["lots", "not a lot"]},
            ]
        },
        {
            "general_name": "Operation System",
            "id": 8,
            "my_questions": [
                {
                    "q_id": 1,
                    "title": "Operation System",
                    "question": "1 How much would you use Operation System with your product?",
                    "answers": ["Only the laptop itself", "Averagely", "Most of the time"]},
                {
                    "q_id": 2,
                    "title": "Operation System 2",
                    "question": "2 do you fucking care about Operation System?",
                    "answers": ["lots", "not a lot"]},
                {
                    "q_id": 3,
                    "title": "Operation System 3",
                    "question": "3 Would you like that Operation System?",
                    "answers": ["no", "yes", "not sure!"]}
            ]
        },
        {
            "general_name": "Dummy Question",
            "id": 10,
            "my_questions": [
                {
                    "q_id": 1,
                    "title": "Elad's Title",
                    "question": "What would you like do develop today sir?",
                    "answers": ["Java, Sir", "Basic Sir", "Dunno Sir!", "Python Plz! Sir!"]
                }
            ]
        },

    ]
    context.update({"questions": questions})
    return render(request, "focalization.html", context)


def comparison(request, product=None):
    pages = OrderedDict()
    pages['Home'] = [False, "home"]
    pages['Affil'] = [False, "affiliation"]
    pages['Appli'] = [False, "application"]
    pages['Focal'] = [False, "focalization"]
    pages['Compar'] = [True, "comparison"]
    pages['Results'] = [False, "results"]
    # Get page Title and Description
    page_title = 'Choose your comp'
    page_desc = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. ' \
                'Donec in maximus augue. Quisque euismod euismod posuere. ' \
                'Phasellus tempor.'
    information_content = {
        "statistic": [
            "S1-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam."],
        "insight": [
            "I1-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.",
            "I2-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.",
            "I3-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam."],
        "objective": [
            "O11-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.",
            "O2-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam."]
    }
    context = {
        "pages": pages,
        "page_title": page_title,
        "page_desc": page_desc,
        "information_content": information_content,
    }
    return render(request, "comparison.html", context)


def results(request, product=None):
    pages = OrderedDict()
    pages['Home'] = [False, "home"]
    pages['Affil'] = [False, "affiliation"]
    pages['Appli'] = [False, "application"]
    pages['Focal'] = [False, "focalization"]
    pages['Compar'] = [False, "comparison"]
    pages['Results'] = [True, "results"]
    context = {}
    # Title and description
    page_title = 'Research Zone'
    context.update({
        "page_title": page_title,
        "pages": pages,
        "product": product,
    })
    page_desc = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. ' \
                'Donec in maximus augue. Quisque euismod euismod posuere. ' \
                'Phasellus tempor.'
    context.update({
        "page_desc": page_desc,
    })
    # Affiliation Form
    ConsultationProcess_id = None
    Product_id = None
    affiliations = None
    uses = None
    que_ans = None

    if product == 'Laptop':
        Product_id = 1  # Laptop product ID
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
            # Application Data
            cursor = connection.cursor()
            if not cursor:
                print("cursor was not defined")
            else:
                # Input: product id
                # Output: levels of use (id,name,value)
                cursor.execute('CALL getLevelsOfUse(%s)', [Product_id])
                uses = dictfetchall(cursor)
                cursor.close()
            # Focalization Data
            cursor = connection.cursor()
            if not cursor:
                print("cursor was not defined")
            else:
                # Input: product id
                # Output: levels of use (id,name,value)
                cursor.execute('CALL getQuestionsAndAnswers(%s)', [Product_id])
                que_ans = dictfetchall(cursor)
                cursor.close()
        except Error as e:
            print(e)

        if Product_id:
            request.session['Product_id'] = Product_id
        # Affiliation Form
        if affiliations:
            affiliations_form = AffiliationsForm(affiliations_dict=affiliations)
            context.update({
                "affiliations_form": affiliations_form,
            })
        # Application Form
        if uses:
            applications_form = UsesForm(uses_dict=uses)
            context.update({
                "applications_form": applications_form,
            })
        # Focalization Dictionary
        questions_list = []
        if que_ans:
            questions_form = QuestionsForm(questions_dict=que_ans)
            i = 1
            # take form inputs and append them to relevant uses
            for index, que in enumerate(que_ans):
                if i == 1:
                    ans_list = []
                    ans_list.append({
                        'ans_input': questions_form[que['question_header'] + str(que['answer_id'])],
                        'ans_content': que['answer_name']
                    })
                    while index + i < len(que_ans) and que['question_id'] == que_ans[index + i]['question_id']:
                        ans_list.append({
                            'ans_input': questions_form[
                                que_ans[index + i]['question_header'] + str(que_ans[index + i]['answer_id'])],
                            'ans_content': que_ans[index + i]['answer_name']
                        })
                        i += 1
                    questions_list.append({
                        'question_header': que['question_header'],
                        'question_id': que['question_id'],
                        'question_content': que['question_content'],
                        'answers': ans_list,
                    })
                else:
                    i -= 1
            context.update({
                "questions_list": questions_list,
            })
        if ConsultationProcess_id:
            request.session['ConsultationProcess_id'] = ConsultationProcess_id[0]
    # Algorithm
    classifier_algo = Classifier()

    # Filtering Form
    # unit: " , GB x 2, lb.
    filters_list = OrderedDict(
        [('Screen Size', ['11.6"', '13.3"', '14"', '15.6"', '17.4"']),
         ('Processor', ['Intel Core i3', 'Intel Core i5', 'Intel Core i7',
                        'Intel Core M', 'AMD X', 'AMD Y', 'Rocket']),
         ('Memory', ['2GB', '4GB', '8GB', '12GB', '16GB', '32GB', '64GB']),
         ('Storage', ['16GB', '32GB', '64GB', '128GB', '192GB', '256GB',
                      '320GB', '500GB', '750GB', '1000GB', '1128GB']),
         ('GPU', ['Intel HD Graphics', 'NVIDIA GeForce', 'AMD Radeon']),
         ('Screen Resolution', ['1024 x 768', '1366 x 768', '1440 x 900',
                                '1920 x 1080', '1920 x 1200', '2166 x 1440',
                                '2560 x 1440', '2560 x 1600', '2880 x 1800',
                                '3200 x 1800', '3860 x 2160']),
         ('Touch Screen', ['Yes', 'No']),
         ('Weight', ['1-2 lb.', '2-3 lb.', '3-4 lb.', '4+ lb.']),
         ('Operating System', ['Chromebook', 'Windows', 'OSX']),
         ('Brand', ['Apple', 'Dell', 'Samsung'])])
    context.update({
        "filters_list": filters_list,
    })
    filters_optional = OrderedDict(
        [('Screen Size', ['13.3"', '14"', '15.6"']),
         ('Processor', ['Intel Core i5', 'Intel Core i7',
                        'AMD X']),
         ('Memory', ['8GB', '12GB', '16GB', '32GB', '64GB']),
         ('Storage', ['320GB', '500GB', '750GB', '1000GB']),
         ('GPU', ['Intel HD Graphics', 'NVIDIA GeForce', 'AMD Radeon']),
         ('Screen Resolution', [
             '1920 x 1080', '1920 x 1200', '2166 x 1440',
             '2560 x 1440', '2560 x 1600']),
         ('Touch Screen', ['Yes', 'No']),
         ('Weight', ['1-2 lb.', '2-3 lb.']),
         ('Operating System', ['Chromebook', 'Windows']),
         ('Brand', ['Apple', 'Dell'])])
    context.update({
        "filters_optional": filters_optional,
    })
    filters_selected = OrderedDict(
        [('Screen Size', ['13.3"', '14"', '15.6"']),
         ('Processor', ['Intel Core i5', 'Intel Core i7']),
         ('Memory', ['8GB']),
         ('Storage', ['500GB', '750GB']),
         ('GPU', ['NVIDIA GeForce']),
         ('Screen Resolution', [
             '2560 x 1440', '2560 x 1600']),
         ('Touch Screen', []),
         ('Weight', ['2-3 lb.']),
         ('Operating System', ['Windows']),
         ('Brand', ['Apple', 'Dell'])])
    context.update({
        "filters_selected": filters_selected,
    })
    filters_form = FilterForm(filters_list=filters_list, filters_optional=filters_optional,
                              filters_selected=filters_selected)
    context.update({
        "filters_form": filters_form,
    })
    # if request.method == 'POST':
    #     filters_form = FilterForm(data=request.POST)
    #     if filters_form.is_valid():
    #         # need to implement filter change event: send params to db and get new results
    #         print("Missing: extract relevant data from db")
    # else:
    #     filters_form = FilterForm(filters_list=filters_list, filters_optional=filters_optional,
    #                               filters_selected=filters_selected)

    # Information Elements Content
    information_content = {
        "statistic": [
            "S1-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam."],
        "insight": [
            "I1-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.",
            "I2-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.",
            "I3-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam."],
        "objective": [
            "O11-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam.",
            "O2-Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam."]
    }
    context.update({
        "information_content": information_content,
    })
    # Final Results
    # Laptop Features (keys): Screen Size, Processor, Memory, Storage [ssd,hdd], GPU, Screen Resolution, Touch Screen,
    #   Weight, Dimensions (WxHxD), Battery [chemistry,cells,wh], Color, Operating System, Model (manufacturer model)

    final_offers = predict('init', classifier_algo, request)
    context.update({
        "final_offers": final_offers[0:3],
    })
    recommended_spec = OrderedDict(
        [('Screen Size', '13-15"'), ('Processor', 'Intel Core i5-5600U'), ('Memory', '8GB'),
         ('Storage', ['8GB SSD', '1000GB HDD']), ('GPU', 'Intel HD Graphics'),
         ('Screen Resolution', '1920 x 1080'), ('Touch Screen', 'Yes'),
         ('Weight', '2.5-3 lb'),
         ('Battery', 'Li-Polymer 6 cells 56Wh'),
         ('Operating System', ['Windows /', 'Chromebook'])])
    context.update({
        "recommended_spec": recommended_spec,
    })

    return render(request, "results.html", context)


def contact(request):
    print('contact|')
    form = ContactForm
    page_title = 'Contact Us'
    page_desc = "Thank you for your interest in Djaroo's consulting platform. " \
                "Please fill in the following form and we'll get back to you shortly."
    context = {
        "page_title": page_title,
        "page_desc": page_desc,
        "form": form,
    }
    if 'contact_name' in request.session:
        success_message = request.session['contact_name'] + ", Thank you for applying us."
        context.update({
            "success_message": success_message,
        })
        del request.session['contact_name']
        return render(request, 'contact.html', context)
    # handle form submission
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            contact_name = request.POST.get('name', '')
            contact_email = request.POST.get('email', '')
            form_content = request.POST.get('message', '')
            # Email the contact information
            template = get_template('contact_template.txt')
            information = Context({
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            })
            email_content = template.render(information)
            email = EmailMessage(
                "New contact form submission",
                email_content,
                "Djaroo Website", ['eladdan88@gmail.com', 'tzuramir@gmail.com', 'talzee10@gmail.com'],
                headers={'Reply-To': contact_email}
            )
            email.send()
            request.session['contact_name'] = contact_name
            return redirect('contact')
        else:
            context.update({
                "form": form,
            })
    return render(request, 'contact.html', context)


def about(request):
    print('about|')
    page_title = 'About Us'
    page_desc = ""
    context = {
        "page_title": page_title,
        "page_desc": page_desc,
    }
    return render(request, 'about.html', context)


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


# # Find the nth occurrence of substring in a string
# def find_nth(haystack, needle, n):
#     start = haystack.find(needle)
#     while start >= 0 and n > 1:
#         start = haystack.find(needle, start + len(needle))
#         n -= 1
#     return start
#
#
# # parse spec value
# def get_spec_val(data, term):
#     data = data[data.index(term) + len(term):]
#     return data[find_nth(data, '>', 1) + 1:data.index('</td>')]


def user_actions(request):
    print('user_actions|')
    if request.method == 'POST':
        request.session.modified = True
        entrance_id = request.session['Entrance_id']
        consultation_process_id = request.session['ConsultationProcess_id']
        action_name = request.POST.get('action_name')
        action_type = request.POST.get('action_type')
        object_id = request.POST.get('object_id')
        action_content = request.POST.get('action_content')
        validate_data = True
        if not object_id.isdigit():
            validate_data = False
        if not (action_type.isdigit() or (action_type[0] == '-' and action_type[1:].isdigit())):
            validate_data = False
        if validate_data:
            try:
                cursor = connection.cursor()
                if not cursor:
                    print("cursor was not defined")
                else:
                    # Input: Entrance_id, Consultation_Process_id, Name, Type, Object_id, Content
                    # Output: saves user action
                    cursor.execute('CALL setNewAction(%s,%s,%s,%s,%s,%s)',
                                   [entrance_id,
                                    consultation_process_id,
                                    action_name,
                                    action_type,
                                    object_id,
                                    action_content
                                    ])
                    cursor.close()
            except Error as e:
                print(e)
        else:
            print('data is not valid')
        # update algorithm
        classifier_ent = Classifier()
        offer_list = []
        # Session Update
        if action_name == 'affiliation_choosing':
            # if checked
            if int(action_type) == 1:
                request.session['affiliation'].append(int(object_id))
                print('affiliations checked. ', request.session['affiliation'])
                offer_list = predict('needs', classifier_ent, request)
            # if un-checked
            elif int(action_type) == -1:
                request.session['affiliation'].remove(int(object_id))
                print('affiliations unchecked. ', request.session['affiliation'])
                offer_list = predict('needs', classifier_ent, request)
        if action_name == 'use_ranking':
            # if checked
            if int(action_type) in [1, 2, 3]:
                request.session['application']['use_id'].append(int(object_id))
                request.session['application']['level_of_use'].append(int(action_type))
            elif int(action_type) in [-1, -2, -3]:
                request.session['application']['use_id'].remove(int(object_id))
                request.session['application']['level_of_use'].remove(int(action_type) * -1)
            offer_list = predict('needs', classifier_ent, request)

        # get results in response
        # send results
        response_data = {}  # hold the data that will send back to client (for future use)
        response_data['offers'] = offer_list
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json",
        )
    else:
        return HttpResponse(
            json.dumps({"failed": "request POST didn't go through"}),
            content_type="application/json"
        )


def predict(p_type, p_classifier, request):
    """

    :param p_type: status type: init/specs/needs
    :param p_classifier: Classifier instance
    :return:
    """
    final_offers = None
    if p_type == 'init':
        final_offers = parse_results(p_classifier.getTop3Results())
        request.session['affiliation'] = []
        request.session['application'] = {'use_id': [], 'level_of_use': []}
        request.session['focalization'] = ''
        request.session['specification'] = []
    elif p_type == 'specs':
        return
    elif p_type == 'price':
        return
    elif p_type == 'needs':
        if len(request.session['affiliation']) > 0:
            final_offers = parse_results(
                p_classifier.getResultsAccordingToAffiliationInput(pd.DataFrame(request.session['affiliation'])))
        if len(request.session['application']['use_id']) > 0:
            print(request.session['application'])
            for index, val in enumerate(request.session['application']['use_id']):
                if index == len(request.session['application']['use_id']) - 1:
                    final_offers = parse_results(p_classifier.getResultsAccordingToApplicationInput(
                        request.session['application']['use_id'][index],
                        request.session['application']['level_of_use'][index]
                    ))
                    print('last one')
                else:
                    parse_results(p_classifier.getResultsAccordingToApplicationInput(
                        request.session['application']['use_id'][index],
                        request.session['application']['level_of_use'][index]
                    ))
                    print('middle one')
        if len(request.session['affiliation']) < 1 and len(request.session['application']['use_id']) < 1:
            print('Unchecked all affiliations and applications')
            final_offers = parse_results(p_classifier.getTop3Results())
    return final_offers


def parse_results(results_list):
    """
    :param results_list: List with 3 result dic - unstructured
    :return: List with 3 result dict - structured
    """
    final_offers = []
    if isinstance(final_offers, str):
        print(final_offers)
    else:
        for offer_dict in results_list:
            ord_dict = OrderedDict([])
            offer_list = []
            result_dict = {'features': ord_dict, 'offers': offer_list}
            for key, val in offer_dict.items():
                if key == 'sort_indicator' or key == 'Brand' or key == 'Line' or key == 'image_url':
                    result_dict[key] = val
                elif key == 'offers':
                    vendor_name, price, deal_url = val.split(',')
                    result_dict['offers'].append(
                        {'vendor_name': vendor_name,
                         'price': price,
                         'deal_url': deal_url,
                         }
                    )
                else:
                    result_dict['features'].update({key: val})
            features_dict = OrderedDict([
                ('Screen Size', result_dict['features']['Screen Size']),
                ('Processor', result_dict['features']['Processor']),
                ('Memory', result_dict['features']['Memory']),
                ('Storage', result_dict['features']['Storage']),
                ('GPU', result_dict['features']['GPU']),
                ('Screen Resolution', result_dict['features']['Screen Resolution']),
                ('Touch Screen', result_dict['features']['Touch Screen']),
                ('Weight', result_dict['features']['Weight']),
                ('Dimensions (WxHxD)', result_dict['features']['Dimensions']),
                ('Battery', result_dict['features']['Battery']),
                ('Color', result_dict['features']['Color']),
                ('Operating System', result_dict['features']['Operating System']),
                ('Model', result_dict['features']['Model'])
            ])
            result_dict['features'] = features_dict
            final_offers.append(result_dict)
    return final_offers


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
        offers = [
            {'sort_indicator': 'Best Match', 'brand': 'Affle', 'model': 'Macbook Froombook',
             'image_url': 'http://ecx.images-amazon.com/images/I/51T4mO8USwL._SL160_.jpg',
             'offers': [{'deal_id': 111,
                         'deal_url': 'http://www.amazon.com/gp/offer-listing/B01C7UGP04%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-',
                         'vendor_name': 'Amazon',
                         'price': 2150}, {'deal_id': 222, 'deal_url': 'xxx', 'vendor_name': 'eBay', 'price': 1000}]
             },
            {'sort_indicator': 'Most Purchased', 'brand': 'Denovo', 'model': 'Yona 3',
             'image_url': 'http://ecx.images-amazon.com/images/I/41sgEA0JL-L._SL160_.jpg',
             'offers': [{'deal_id': 333,
                         'deal_url': 'http://www.amazon.com/gp/offer-listing/B00VX4K8AY%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-',
                         'vendor_name': 'Amazon',
                         'price': 2250}, {'deal_id': 444, 'deal_url': 'xxx', 'vendor_name': 'eBay', 'price': 1100}]
             },
            {'sort_indicator': 'Type Popular', 'brand': 'Nell', 'model': 'PPS',
             'image_url': 'http://ecx.images-amazon.com/images/I/11g7mTNdxLL._SL160_.jpg',
             'offers': [{'deal_id': 555,
                         'deal_url': 'http://www.amazon.com/gp/offer-listing/B0143Q3TLS%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-',
                         'vendor_name': 'Amazon',
                         'price': 2550}, {'deal_id': 666, 'deal_url': 'xxx', 'vendor_name': 'eBay', 'price': 1200}]
             },
            {'sort_indicator': 'Cost Effective', 'brand': 'Azuz', 'model': 'Benbook 133X',
             'image_url': 'http://ecx.images-amazon.com/images/I/51ePHH0Re8L._SL160_.jpg',
             'offers': [{'deal_id': 777,
                         'deal_url': 'http://www.amazon.com/gp/offer-listing/B00J39HLEM%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-',
                         'vendor_name': 'Amazon',
                         'price': 2750}, {'deal_id': 888, 'deal_url': 'xxx', 'vendor_name': 'eBay', 'price': 1300}]
             },
            {'sort_indicator': 'Stylish', 'brand': 'Rony', 'model': 'Romber 304',
             'image_url': 'http://ecx.images-amazon.com/images/I/41gL4chShUL._SL160_.jpg',
             'offers': [{'deal_id': 999,
                         'deal_url': 'http://www.amazon.com/gp/offer-listing/B01COPL3PO%3FSubscriptionId%3DAKIAJZXUIQUQZ34J3E5Q%26tag%3Ddjaroo10-',
                         'vendor_name': 'Amazon',
                         'price': 2800}, {'deal_id': 121, 'deal_url': 'xxx', 'vendor_name': 'eBay', 'price': 1400}]
             },
        ]
        total_results = 1450
        response_data['total_results'] = total_results
        response_data['offers'] = offers
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"failed": "request POST didn't go through"}),
            content_type="application/json"
        )
