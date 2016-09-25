from django.shortcuts import render, redirect
from django.db import connection, Error
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context
from consult.forms import AffiliationsForm, UsesForm, QuestionsForm, ContactForm, FilterForm
from django.http import HttpResponse
from collections import OrderedDict
import urllib.request
import json
import pickle
from consult.utils import Classifier
import pandas as pd


def home(request):
    print('home|')
    pages = OrderedDict()
    pages['Home'] = [True, "home"]
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
    # gather user data
    if 'Entrance_id' in request.session:
        entrance_id = str(request.session['Entrance_id'])
    else:
        entrance_id = 1
    if 'ConsultationProcess_id' in request.session:
        consultation_process_id = request.session['ConsultationProcess_id']
    else:
        consultation_process_id = 1
    action_name = 'webpage_viewing'
    action_type = 0
    action_content_referer = request.META.get('HTTP_REFERER') or None
    # device type is determined on mobileesp.middleware
    action_content_device = request.device_type
    try:
        if action_content_referer is not None:
            set_new_action(entrance_id, consultation_process_id, action_name, action_type, None, action_content_referer)
        set_new_action(entrance_id, consultation_process_id, action_name, action_type, None, action_content_device)
    except Error as e:
        print(e)
    return render(request, "index.html", context)


def results(request, product=None):
    context = {}
    # Session ajax
    request.session['ajax_in_process'] = []
    # Title and description
    page_title = 'Research Zone'
    context.update({
        "page_title": page_title,
        "product": product,
    })
    page_desc = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. ' \
                'Donec in maximus augue. Quisque euismod euismod posuere. ' \
                'Phasellus tempor.'
    context.update({
        "page_desc": page_desc,
    })

    # initial variables
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
    # gather user data
    if 'Entrance_id' in request.session:
        entrance_id = str(request.session['Entrance_id'])
    else:
        entrance_id = 1
    if 'ConsultationProcess_id' in request.session:
        consultation_process_id = request.session['ConsultationProcess_id']
    else:
        consultation_process_id = 1
    action_name = 'webpage_viewing'
    action_type = 1
    action_content = request.META.get('HTTP_REFERER') or None
    try:
        set_new_action(entrance_id, consultation_process_id, action_name, action_type, None, action_content)
    except Error as e:
        print(e)
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
    # user data
    if 'Entrance_id' in request.session:
        entrance_id = str(request.session['Entrance_id'])
    else:
        entrance_id = 1
    if 'ConsultationProcess_id' in request.session:
        consultation_process_id = request.session['ConsultationProcess_id']
    else:
        consultation_process_id = 1
    action_name = 'webpage_viewing'
    action_type = 3

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
            # save form at DB
            try:
                set_new_action(entrance_id, consultation_process_id, action_name, action_type, None,
                               'Name: ' + str(contact_name) +
                               ' , Email: ' + str(contact_email) +
                               ' , Content: ' + str(form_content))
            except Error as e:
                print(e)
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
            print('form is not valid')
            context.update({
                "form": form,
            })
    # gather user data
    action_content = request.META.get('HTTP_REFERER') or None
    try:
        set_new_action(entrance_id, consultation_process_id, action_name, action_type, None, action_content)
    except Error as e:
        print(e)
    return render(request, 'contact.html', context)


def about(request):
    print('about|')
    page_title = 'About Us'
    page_desc = ""
    context = {
        "page_title": page_title,
        "page_desc": page_desc,
    }
    # gather user data
    if 'Entrance_id' in request.session:
        entrance_id = str(request.session['Entrance_id'])
    else:
        entrance_id = 1
    if 'ConsultationProcess_id' in request.session:
        consultation_process_id = request.session['ConsultationProcess_id']
    else:
        consultation_process_id = 1
    action_name = 'webpage_viewing'
    action_type = 2
    action_content = request.META.get('HTTP_REFERER') or None
    try:
        set_new_action(entrance_id, consultation_process_id, action_name, action_type, None, action_content)
    except Error as e:
        print(e)
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


def user_actions(request):
    print('user_actions|')
    if request.method == 'POST':
        request.session.modified = True
        if 'Entrance_id' in request.session:
            entrance_id = request.session['Entrance_id']
        else:
            entrance_id = 1
        if 'ConsultationProcess_id' in request.session:
            consultation_process_id = request.session['ConsultationProcess_id']
        else:
            consultation_process_id = 1
        action_name = request.POST.get('action_name')
        action_type = request.POST.get('action_type')
        object_id = request.POST.get('object_id')
        action_content = request.POST.get('action_content')
        validate_data = True
        if not (object_id is None or object_id.isdigit()):
            print('object_id is not valid: ', object_id)
            validate_data = False
        if not (action_type is None or action_type.isdigit() or (action_type[0] == '-' and action_type[1:].isdigit())):
            print('action_type is not valid: ', action_type)
            validate_data = False
        if validate_data:
            # Input: Entrance_id, Consultation_Process_id, Name, Type, Object_id, Content
            # Output: saves user action
            try:
                set_new_action(entrance_id,
                               consultation_process_id,
                               action_name,
                               action_type,
                               object_id,
                               action_content)
            except Error as e:
                print(e)
        else:
            print('data is not valid')
        # update algorithm
        classifier_ent = Classifier()
        offer_list = []
        # Session Update
        print('-----Updating SESSION-----')
        if action_name == 'affiliation_choosing':
            # if checked
            print('affiliation_choosing - action type value:', int(action_type))
            if int(action_type) == 1:
                request.session['affiliation'].append(int(object_id))
                print('affiliations checked. SESSEION: ', request.session['affiliation'])
                offer_list = predict('needs', classifier_ent, request)
            # if un-checked
            elif int(action_type) == -1:
                if int(object_id) in request.session['affiliation']:
                    request.session['affiliation'].remove(int(object_id))
                print('affiliations unchecked. SESSEION: ', request.session['affiliation'])
                offer_list = predict('needs', classifier_ent, request)
        if action_name == 'use_ranking':
            # if checked
            print('action type', int(action_type))
            if int(action_type) in [1, 2, 3]:
                # if re-checked
                if int(object_id) in request.session['application']['use_id']:
                    remove_index = request.session['application']['use_id'].index(int(object_id))
                    del request.session['application']['use_id'][remove_index]
                    del request.session['application']['level_of_use'][remove_index]
                request.session['application']['use_id'].append(int(object_id))
                request.session['application']['level_of_use'].append(int(action_type))
            # if un-checked
            elif int(action_type) in [-1, -2, -3]:
                request.session['application']['use_id'].remove(int(object_id))
                request.session['application']['level_of_use'].remove(int(action_type) * -1)
            offer_list = predict('needs', classifier_ent, request)
        if action_name == 'price_range_changing':
            prices = [int(x) for x in action_content.split(",")]
            if len(prices) == 4:
                request.session['specification']['price'] = []
                request.session['specification']['price'].append([prices[0], prices[1]])
                request.session['specification']['price'].append([prices[2], prices[3]])
                print('price range choosing ')
                print(request.session['specification']['price'])
                # if menu type needs or specs -> execute different predict
                offer_list = predict('needs', classifier_ent, request)
        # get results in response
        # send results
        response_data = {}  # hold the data that will send back to client (for future use)
        response_data['offers'] = offer_list
        print('-----RETURN-----')
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json",
        )
    else:
        return HttpResponse(
            json.dumps({"failed": "request POST didn't go through"}),
            content_type="application/json"
        )


def user_exit(request):
    print('user_exit|')
    if 'Entrance_id' in request.session:
        entrance_id = request.session['Entrance_id']
    else:
        entrance_id = 1
    if 'ConsultationProcess_id' in request.session:
        consultation_process_id = request.session['ConsultationProcess_id']
    else:
        consultation_process_id = 1
    try:
        set_new_action(entrance_id, consultation_process_id, 'webpage_viewing', -1, None, None)
    except Error as e:
        print(e)
    return HttpResponse('')


def navbar_update(request):
    print('navbar_update|')
    context = {
    }
    return render(request, "navbar.html", context)


def predict(p_type, p_classifier, request):
    """

    :param p_type: status type: init/specs/needs
    :param p_classifier: Classifier instance
    :return:
    """
    final_offers = None
    print('-----Predict-----')
    if p_type == 'init':
        print('predict Init')
        request.session['affiliation'] = []
        request.session['application'] = {'use_id': [], 'level_of_use': []}
        request.session['focalization'] = ''
        request.session['static_price_range'] = p_classifier.getPriceRange()
        # specs - manual insert: [brand, screen_size, touch_screen, screen_resolution,
        #                        ram, gpu, cpu, capacity, os, weight]
        # price - auto insert: [min_start, max_start, min_end, max_end]
        request.session['specification'] = {'specs': [[], [], [], [], [], [], [], [], [], [0, 10000]],
                                            'price': [[0, 0], request.session['static_price_range']]
                                            }
        final_offers = parse_results(p_classifier.getTop3Results())
    elif p_type == 'specs':
        return
    elif p_type == 'needs':
        if len(request.session['affiliation']) > 0:
            print('predict AFFILIATION. executing the following input:')
            print(request.session['affiliation'])
            final_offers = parse_results(
                p_classifier.getResultsAccordingToAffiliationInput(pd.DataFrame(request.session['affiliation'])))
        if len(request.session['application']['use_id']) > 0:
            print('predict APPLICATION. executing the following input:')
            print(request.session['application'])
            for index, val in enumerate(request.session['application']['use_id']):
                if index == len(request.session['application']['use_id']) - 1:
                    final_offers = parse_results(p_classifier.getResultsAccordingToApplicationInput(
                        request.session['application']['use_id'][index],
                        request.session['application']['level_of_use'][index]
                    ))
                else:
                    parse_results(p_classifier.getResultsAccordingToApplicationInput(
                        request.session['application']['use_id'][index],
                        request.session['application']['level_of_use'][index]
                    ))
        if len(request.session['affiliation']) < 1 and len(request.session['application']['use_id']) < 1:
            print('Unchecked all affiliations and applications')
            final_offers = parse_results(p_classifier.getTop3Results())
    if p_type != 'specs':
        print('predict PRICE. executing the following input:')
        # price input: empty specs + price values  (just if needs and init)
        specs_input = [[] for x in range(0, len(request.session['specification']['specs']))]
        # add weight value manually
        specs_input[len(specs_input) - 1] = [0, 10000]
        price_input = specs_input + [request.session['specification']['price'][1]]
        print(*price_input)
        final_offers = parse_results(p_classifier.filterByRules(*price_input))
    return final_offers


def parse_results(results_list):
    """
    :param results_list: List with 3 result dic - unstructured
    :return: List with 3 result dict - structured
    """
    final_offers = []
    # print(final_offers)
    # print(type(final_offers))
    # print(isinstance(final_offers, str))
    if isinstance(results_list, str):
        print(results_list)
        return results_list
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
                ('Model', result_dict['features']['Model']),
                ('Key', result_dict['features']['Key']),  # model key
            ])
            result_dict['features'] = features_dict
            final_offers.append(result_dict)
    return final_offers


def set_new_action(entrance_id, consultation_process_id, action_name, action_type, object_id, action_content):
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
