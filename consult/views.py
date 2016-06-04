import time
from django.shortcuts import render
from collections import OrderedDict
from django.db import connection, Error

from apis.utils import get_spec_val, find_nth
from consult.forms import AffiliationsForm, UsesForm
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
        #                                             offers[{deal_id, deal_url, vendor_name, price}, {}, ]}
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
        context.update({
            "Product_id": Product_id,
            "affiliationsLength": len(affiliations),
            "affiliations": affiliations,
            "ConsultationProcess_id": ConsultationProcess_id[0],
            "offers": offers[0:3],
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
        context.update({
            "template_uses": template_uses,
            "offers": offers[0:3],
            "total_results": total_results,
        })

    return render(request, "application.html", context)


def focalization(request, product=None):
    # http://stackoverflow.com/questions/26566799/selenium-python-how-to-wait-until-the-page-is-loaded
    from selenium import webdriver

    pages = OrderedDict()
    pages['Home'] = [False, "home"]
    pages['Affil'] = [False, "affiliation"]
    pages['Appli'] = [False, "application"]
    pages['Focal'] = [True, "focalization"]
    pages['Compar'] = [False, "comparison"]
    pages['Results'] = [False, "results"]

    # upc = 889349130445
    # url = 'http://www.rakuten.com/sr/searchresults#qu=' + str(upc)
    # browser = webdriver.Firefox()
    # browser.get(url)
    # web_data = browser.page_source
    # desired_content_is_loaded = False
    # # loop until sku is loaded
    # while not desired_content_is_loaded:
    #     if 'data-sku="' not in web_data:
    #         time.sleep(3)
    #         web_data = browser.page_source
    #         print('not found')
    #     else:
    #         desired_content_is_loaded = True
    #         print('found')
    #         start_index = int(web_data.index('data-sku="') + len('data-sku="'))
    #         end_index = int(start_index + 9)
    #         sku = web_data[start_index:end_index]
    #         print(sku)

    # sku = 259193368
    # sku = str(sku)
    # url = 'http://www.rakuten.com/prod/' + sku + '.html'
    # browser = webdriver.Firefox()
    # browser.get(url)
    # web_data = browser.page_source
    # browser.quit()
    # # take only specification section
    # start_index = int(web_data.index('<h2>Specifications</h2>'))
    # end_index = int(web_data.index('<h2>More Buying Options</h2>'))
    # web_data = web_data[start_index:end_index]
    # # create specifications dictionary
    # specs_dic = {'sku': sku}
    # # text of anchor tags
    # if '<th>Manufacturer</th>' in web_data:
    #     # take just the text after found string
    #     temp_data = web_data[web_data.index('<th>Manufacturer</th>') + len('<th>Manufacturer</th>'):]
    #     start_index = find_nth(temp_data, '>', 2) + 1
    #     end_index = temp_data.index('</a>')
    #     specs_dic['Manufacturer'] = temp_data[start_index:end_index]
    # if '<th>Product Guide</th>' in web_data:
    #     temp_data = web_data[web_data.index('<th>Manufacturer</th>') + len('<th>Manufacturer</th>'):]
    #     start_index = find_nth(temp_data, '>', 2) + 1
    #     end_index = temp_data.index('</a>')
    #     specs_dic['productGuide'] = temp_data[start_index:end_index]
    # # text of table column
    # term = '<th>Mfg Part#</th>'
    # if term in web_data:
    #     specs_dic['mfgPart'] = get_spec_val(web_data, term)
    # term = '<th>SKU</th>'
    # if term in web_data:
    #     specs_dic['Sku'] = get_spec_val(web_data, term)
    # term = '<th>UPC</th>'
    # if term in web_data:
    #     specs_dic['Upc'] = get_spec_val(web_data, term)
    # term = '<th>UPC 14</th>'
    # if term in web_data:
    #     specs_dic['Upc14'] = get_spec_val(web_data, term)
    # term = '<th>battery Chemistry </th>'
    # if term in web_data:
    #     specs_dic['BatteryChemistry'] = get_spec_val(web_data, term)
    # term = '<th>Number of Cells </th>'
    # if term in web_data:
    #     specs_dic['numberOfCells'] = get_spec_val(web_data, term)
    # term = '<th>Maximum Battery Run Time </th>'
    # if term in web_data:
    #     specs_dic['maximumBatteryRunTime'] = get_spec_val(web_data, term)
    # term = '<th>Finger Print Reader </th>'
    # if term in web_data:
    #     specs_dic['fingerPrintReader'] = get_spec_val(web_data, term)
    # term = '<th>Front Camera/Webcam </th>'
    # if term in web_data:
    #     specs_dic['frontCamera'] = get_spec_val(web_data, term)
    # term = '<th>HDMI </th>'
    # if term in web_data:
    #     specs_dic['Hdmi'] = get_spec_val(web_data, term)
    # term = '<th>Network (RJ-45) </th>'
    # if term in web_data:
    #     specs_dic['networkRJ45'] = get_spec_val(web_data, term)
    # term = '<th>Total Number of USB Ports </th>'
    # if term in web_data:
    #     specs_dic['totalNumberOfUsbPorts'] = get_spec_val(web_data, term)
    # term = '<th>Number of USB 3.0 Ports </th>'
    # if term in web_data:
    #     specs_dic['numberOfUsb3.0Ports'] = get_spec_val(web_data, term)
    # term = '<th>Aspect Ratio </th>'
    # if term in web_data:
    #     specs_dic['aspectRatio'] = get_spec_val(web_data, term)
    # term = '<th>Screen Resolution </th>'
    # if term in web_data:
    #     specs_dic['screenResolution'] = get_spec_val(web_data, term)
    # term = '<th>Screen Size </th>'
    # if term in web_data:
    #     specs_dic['screenSize'] = get_spec_val(web_data, term)
    # term = '<th>Graphics Controller Manufacturer </th>'
    # if term in web_data:
    #     specs_dic['graphicsControllerManufacturer'] = get_spec_val(web_data, term)
    # term = '<th>Graphics Controller Model </th>'
    # if term in web_data:
    #     specs_dic['graphicsControllerModel'] = get_spec_val(web_data, term)
    # term = '<th>Graphics Memory Technology </th>'
    # if term in web_data:
    #     specs_dic['graphicsMemoryTechnology'] = get_spec_val(web_data, term)
    # term = '<th>Graphics Memory Accessibility </th>'
    # if term in web_data:
    #     specs_dic['graphicsMemoryAccessibility'] = get_spec_val(web_data, term)
    # term = '<th>Display Screen Technology </th>'
    # if term in web_data:
    #     specs_dic['displayScreenTechnology'] = get_spec_val(web_data, term)
    # term = '<th>Product Type </th>'
    # if term in web_data:
    #     specs_dic['productType'] = get_spec_val(web_data, term)
    # term = '<th>Manufacturer Part Number </th>'
    # if term in web_data:
    #     specs_dic['manufacturerPartNumber'] = get_spec_val(web_data, term)
    # term = '<th>Manufacturer </th>'
    # if term in web_data:
    #     specs_dic['manufacturer'] = get_spec_val(web_data, term)
    # term = '<th>Product Model </th>'
    # if term in web_data:
    #     specs_dic['productModel'] = get_spec_val(web_data, term)
    # term = '<th>Product Name </th>'
    # if term in web_data:
    #     specs_dic['productName'] = get_spec_val(web_data, term)
    # term = '<th>Product Series </th>'
    # if term in web_data:
    #     specs_dic['productSeries'] = get_spec_val(web_data, term)
    # term = '<th>Brand Name </th>'
    # if term in web_data:
    #     specs_dic['brandName'] = get_spec_val(web_data, term)
    # term = '<th>Standard Memory </th>'
    # if term in web_data:
    #     specs_dic['standardMemory'] = get_spec_val(web_data, term)
    # term = '<th>Memory Technology </th>'
    # if term in web_data:
    #     specs_dic['memoryTechnology'] = get_spec_val(web_data, term)
    # term = '<th>Package Contents </th>'
    # if term in web_data:
    #     specs_dic['packageContents'] = get_spec_val(web_data, term)
    # term = '<th>Green Compliant </th>'
    # if term in web_data:
    #     specs_dic['greenCompliant'] = get_spec_val(web_data, term)
    # term = '<th>Green Compliance Certificate/Authority </th>'
    # if term in web_data:
    #     specs_dic['greenComplianceCertificate'] = get_spec_val(web_data, term)
    # term = '<th>Bluetooth </th>'
    # if term in web_data:
    #     specs_dic['bluetooth'] = get_spec_val(web_data, term)
    # term = '<th>Wireless LAN </th>'
    # if term in web_data:
    #     specs_dic['wirelessLAN'] = get_spec_val(web_data, term)
    # term = '<th>Wireless LAN Standard </th>'
    # if term in web_data:
    #     specs_dic['wirelessLANStandard'] = get_spec_val(web_data, term)
    # term = '<th>Weight (Approximate) </th>'
    # if term in web_data:
    #     specs_dic['weightApproximate'] = get_spec_val(web_data, term)
    # term = '<th>Color </th>'
    # if term in web_data:
    #     specs_dic['color'] = get_spec_val(web_data, term)
    # term = '<th>Height </th>'
    # if term in web_data:
    #     specs_dic['height'] = get_spec_val(web_data, term)
    # term = '<th>Width </th>'
    # if term in web_data:
    #     specs_dic['width'] = get_spec_val(web_data, term)
    # term = '<th>Depth </th>'
    # if term in web_data:
    #     specs_dic['depth'] = get_spec_val(web_data, term)
    # term = '<th>Optical Drive Type </th>'
    # if term in web_data:
    #     specs_dic['opticalDriveType'] = get_spec_val(web_data, term)
    # term = '<th>Solid State Drive Capacity </th>'
    # if term in web_data:
    #     specs_dic['solidStateDriveCapacity'] = get_spec_val(web_data, term)
    # term = '<th>Processor Speed </th>'
    # if term in web_data:
    #     specs_dic['processorSpeed'] = get_spec_val(web_data, term)
    # term = '<th>Processor Type </th>'
    # if term in web_data:
    #     specs_dic['processorType'] = get_spec_val(web_data, term)
    # term = '<th>Processor Model </th>'
    # if term in web_data:
    #     specs_dic['processorModel'] = get_spec_val(web_data, term)
    # term = '<th>Processor Core </th>'
    # if term in web_data:
    #     specs_dic['processorCore'] = get_spec_val(web_data, term)
    # term = '<th>Processor Manufacturer </th>'
    # if term in web_data:
    #     specs_dic['processorManufacturer'] = get_spec_val(web_data, term)
    # term = '<th>Operating System </th>'
    # if term in web_data:
    #     specs_dic['operatingSystem'] = get_spec_val(web_data, term)
    # term = '<th>Operating System Architecture </th>'
    # if term in web_data:
    #     specs_dic['operatingSystemArchitecture'] = get_spec_val(web_data, term)
    # term = '<th>Operating System Platform </th>'
    # if term in web_data:
    #     specs_dic['operatingSystemPlatform'] = get_spec_val(web_data, term)
    # term = '<th>Limited Warranty </th>'
    # if term in web_data:
    #     specs_dic['limitedWarranty'] = get_spec_val(web_data, term)
    #
    # # remove space at beginning of values
    # for key, value in specs_dic.items():
    #     if ' ' in value and value.index(' ') == 0:
    #         specs_dic[key] = value[1:]
    # print(specs_dic)
    context = {
        "pages": pages,
        "product": product,
        # "web_data": web_data,
    }
    return render(request, "focalization.html", context)


def comparison(request, product=None):
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
