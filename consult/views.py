from django.shortcuts import render, redirect
from collections import OrderedDict
from django.db import connection, Error
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context
from consult.forms import AffiliationsForm, UsesForm, ContactForm
from django.http import HttpResponse
from consult.models import Levelofuse
import urllib.request
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
    context = {
        "pages": pages,
    }
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
    context = {
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
