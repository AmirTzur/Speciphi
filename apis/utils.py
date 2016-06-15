import os
import json
import csv
import time
# Amazon sdk: bottlenode
import bottlenose
import lxml
from lxml import objectify

from django.conf import settings

# eBay-Python sdk
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection as Finding
from ebaysdk.trading import Connection as Trading

# model to store local data from eBay
from .models import EbayLaptopDeal
from selenium import webdriver
from selenium.common.exceptions import TimeoutException


# Find the nth occurrence of substring in a string
def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start + len(needle))
        n -= 1
    return start


# parse spec value
def get_spec_val(data, term):
    data = data[data.index(term) + len(term):]
    return data[find_nth(data, '>', 1) + 1:data.index('</td>')]


def get_sku(upc=None):
    upc = str(upc)  # check 12 digits
    while len(upc) < 12:
        upc = '0' + upc
        print('added zero', upc)
    url = 'http://www.rakuten.com/sr/searchresults#qu=' + upc
    browser = webdriver.Firefox()
    browser.get(url)
    web_data = browser.page_source
    browser.quit()
    if 'data-sku="' in web_data:
        print('found')
        start_index = int(web_data.index('data-sku="') + len('data-sku="'))
        end_index = int(start_index + 9)
        sku = web_data[start_index:end_index]
        # browser.quit()
        return sku
    else:
        print('not found')
        # browser.quit()
        return '0'


def get_spec(sku=None):
    sku = str(sku)
    url = 'http://www.rakuten.com/prod/' + sku + '.html'
    browser = webdriver.Firefox()
    browser.get(url)
    web_data = browser.page_source
    browser.quit()
    # take only specification section
    # start position
    if '<h2>Specifications</h2>' in web_data:
        start_index = int(web_data.index('<h2>Specifications</h2>'))
    else:
        return {'sku': 0}
    # end position
    if '<h2>More Buying Options</h2>' in web_data:
        end_index = int(web_data.index('<h2>More Buying Options</h2>'))
    elif '<div class="title">Featured Products</div>' in web_data:
        end_index = int(web_data.index('<div class="title">Featured Products</div>'))
    else:
        return {'sku': 0}
    web_data = web_data[start_index:end_index]
    # create specifications dictionary
    specs_dic = {'sku': sku}
    # text of anchor tags
    if '<th>Manufacturer</th>' in web_data:
        # take just the text after found string
        temp_data = web_data[web_data.index('<th>Manufacturer</th>') + len('<th>Manufacturer</th>'):]
        start_index = find_nth(temp_data, '>', 2) + 1
        end_index = temp_data.index('</a>')
        specs_dic['Manufacturer'] = temp_data[start_index:end_index]
    if '<th>Product Guide</th>' in web_data:
        temp_data = web_data[web_data.index('<th>Manufacturer</th>') + len('<th>Manufacturer</th>'):]
        start_index = find_nth(temp_data, '>', 2) + 1
        end_index = temp_data.index('</a>')
        specs_dic['productGuide'] = temp_data[start_index:end_index]
        # text of table column
    term = '<th>Mfg Part#</th>'
    if term in web_data:
        specs_dic['mfgPart'] = get_spec_val(web_data, term)
    term = '<th>SKU</th>'
    if term in web_data:
        specs_dic['Sku'] = get_spec_val(web_data, term)
    term = '<th>UPC</th>'
    if term in web_data:
        specs_dic['Upc'] = get_spec_val(web_data, term)
    term = '<th>UPC 14</th>'
    if term in web_data:
        specs_dic['Upc14'] = get_spec_val(web_data, term)
    term = '<th>Battery Chemistry </th>'
    if term in web_data:
        specs_dic['BatteryChemistry'] = get_spec_val(web_data, term)
    term = '<th>Number of Cells </th>'
    if term in web_data:
        specs_dic['numberOfCells'] = get_spec_val(web_data, term)
    term = '<th>Maximum Battery Run Time </th>'
    if term in web_data:
        specs_dic['maximumBatteryRunTime'] = get_spec_val(web_data, term)
    term = '<th>Finger Print Reader </th>'
    if term in web_data:
        specs_dic['fingerPrintReader'] = get_spec_val(web_data, term)
    term = '<th>Front Camera/Webcam </th>'
    if term in web_data:
        specs_dic['frontCamera'] = get_spec_val(web_data, term)
    term = '<th>HDMI </th>'
    if term in web_data:
        specs_dic['Hdmi'] = get_spec_val(web_data, term)
    term = '<th>Network (RJ-45) </th>'
    if term in web_data:
        specs_dic['networkRJ45'] = get_spec_val(web_data, term)
    term = '<th>Total Number of USB Ports </th>'
    if term in web_data:
        specs_dic['totalNumberOfUsbPorts'] = get_spec_val(web_data, term)
    term = '<th>Number of USB 3.0 Ports </th>'
    if term in web_data:
        specs_dic['numberOfUsb3.0Ports'] = get_spec_val(web_data, term)
    term = '<th>Aspect Ratio </th>'
    if term in web_data:
        specs_dic['aspectRatio'] = get_spec_val(web_data, term)
    term = '<th>Screen Resolution </th>'
    if term in web_data:
        specs_dic['screenResolution'] = get_spec_val(web_data, term)
    term = '<th>Screen Size </th>'
    if term in web_data:
        specs_dic['screenSize'] = get_spec_val(web_data, term)
    term = '<th>Graphics Controller Manufacturer </th>'
    if term in web_data:
        specs_dic['graphicsControllerManufacturer'] = get_spec_val(web_data, term)
    term = '<th>Graphics Controller Model </th>'
    if term in web_data:
        specs_dic['graphicsControllerModel'] = get_spec_val(web_data, term)
    term = '<th>Graphics Memory Technology </th>'
    if term in web_data:
        specs_dic['graphicsMemoryTechnology'] = get_spec_val(web_data, term)
    term = '<th>Graphics Memory Accessibility </th>'
    if term in web_data:
        specs_dic['graphicsMemoryAccessibility'] = get_spec_val(web_data, term)
    term = '<th>Display Screen Technology </th>'
    if term in web_data:
        specs_dic['displayScreenTechnology'] = get_spec_val(web_data, term)
    term = '<th>Product Type </th>'
    if term in web_data:
        specs_dic['productType'] = get_spec_val(web_data, term)
    term = '<th>Manufacturer Part Number </th>'
    if term in web_data:
        specs_dic['manufacturerPartNumber'] = get_spec_val(web_data, term)
    term = '<th>Manufacturer </th>'
    if term in web_data:
        specs_dic['manufacturer'] = get_spec_val(web_data, term)
    term = '<th>Product Model </th>'
    if term in web_data:
        specs_dic['productModel'] = get_spec_val(web_data, term)
    term = '<th>Product Name </th>'
    if term in web_data:
        specs_dic['productName'] = get_spec_val(web_data, term)
    term = '<th>Product Series </th>'
    if term in web_data:
        specs_dic['productSeries'] = get_spec_val(web_data, term)
    term = '<th>Brand Name </th>'
    if term in web_data:
        specs_dic['brandName'] = get_spec_val(web_data, term)
    term = '<th>Standard Memory </th>'
    if term in web_data:
        specs_dic['standardMemory'] = get_spec_val(web_data, term)
    term = '<th>Memory Technology </th>'
    if term in web_data:
        specs_dic['memoryTechnology'] = get_spec_val(web_data, term)
    term = '<th>Package Contents </th>'
    if term in web_data:
        specs_dic['packageContents'] = get_spec_val(web_data, term)
    term = '<th>Green Compliant </th>'
    if term in web_data:
        specs_dic['greenCompliant'] = get_spec_val(web_data, term)
    term = '<th>Green Compliance Certificate/Authority </th>'
    if term in web_data:
        specs_dic['greenComplianceCertificate'] = get_spec_val(web_data, term)
    term = '<th>Bluetooth </th>'
    if term in web_data:
        specs_dic['bluetooth'] = get_spec_val(web_data, term)
    term = '<th>Wireless LAN </th>'
    if term in web_data:
        specs_dic['wirelessLAN'] = get_spec_val(web_data, term)
    term = '<th>Wireless LAN Standard </th>'
    if term in web_data:
        specs_dic['wirelessLANStandard'] = get_spec_val(web_data, term)
    term = '<th>Weight (Approximate) </th>'
    if term in web_data:
        specs_dic['weightApproximate'] = get_spec_val(web_data, term)
    term = '<th>Color </th>'
    if term in web_data:
        specs_dic['color'] = get_spec_val(web_data, term)
    term = '<th>Height </th>'
    if term in web_data:
        specs_dic['height'] = get_spec_val(web_data, term)
    term = '<th>Width </th>'
    if term in web_data:
        specs_dic['width'] = get_spec_val(web_data, term)
    term = '<th>Depth </th>'
    if term in web_data:
        specs_dic['depth'] = get_spec_val(web_data, term)
    term = '<th>Optical Drive Type </th>'
    if term in web_data:
        specs_dic['opticalDriveType'] = get_spec_val(web_data, term)
    term = '<th>Solid State Drive Capacity </th>'
    if term in web_data:
        specs_dic['solidStateDriveCapacity'] = get_spec_val(web_data, term)
    term = '<th>Processor Speed </th>'
    if term in web_data:
        specs_dic['processorSpeed'] = get_spec_val(web_data, term)
    term = '<th>Processor Type </th>'
    if term in web_data:
        specs_dic['processorType'] = get_spec_val(web_data, term)
    term = '<th>Processor Model </th>'
    if term in web_data:
        specs_dic['processorModel'] = get_spec_val(web_data, term)
    term = '<th>Processor Core </th>'
    if term in web_data:
        specs_dic['processorCore'] = get_spec_val(web_data, term)
    term = '<th>Processor Manufacturer </th>'
    if term in web_data:
        specs_dic['processorManufacturer'] = get_spec_val(web_data, term)
    term = '<th>Operating System </th>'
    if term in web_data:
        specs_dic['operatingSystem'] = get_spec_val(web_data, term)
    term = '<th>Operating System Architecture </th>'
    if term in web_data:
        specs_dic['operatingSystemArchitecture'] = get_spec_val(web_data, term)
    term = '<th>Operating System Platform </th>'
    if term in web_data:
        specs_dic['operatingSystemPlatform'] = get_spec_val(web_data, term)
    term = '<th>Limited Warranty </th>'
    if term in web_data:
        specs_dic['limitedWarranty'] = get_spec_val(web_data, term)
    term = '<th>Headphone/Microphone Combo Port </th>'
    if term in web_data:
        specs_dic['headphone.microphoneComboPort'] = get_spec_val(web_data, term)
    term = '<th>Micro HDMI </th>'
    if term in web_data:
        specs_dic['microHdmi'] = get_spec_val(web_data, term)
    term = '<th>Touchscreen </th>'
    if term in web_data:
        specs_dic['touchScreen'] = get_spec_val(web_data, term)
    term = '<th>Flash Memory Capacity </th>'
    if term in web_data:
        specs_dic['flashMemoryCapacity'] = get_spec_val(web_data, term)
    # remove space at beginning of values
    for key, value in specs_dic.items():
        if ' ' in value and value.index(' ') == 0:
            specs_dic[key] = value[1:]
    return specs_dic


class LaptopSpecs(object):
    def upcs_to_skus(self):
        # open sku's csv (output)
        output_csv_file = open('skus_output.csv', 'w', encoding='utf-8', newline='')
        csv_writer = csv.writer(output_csv_file)
        # read from upc's csv (input)
        with open('upcs_input.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            counter = 0
            for row in reader:
                print(counter)
                if counter == 0:
                    # header
                    row.append('sku')
                    print(row)
                    print()
                    csv_writer.writerow(row)
                    counter += 1
                    continue
                try:
                    # input: upc
                    # output: sku
                    sku = get_sku(row[1])
                    row.append(sku)
                    print(row)
                    # write row to csv
                    csv_writer.writerow(row)
                except TimeoutException as e:
                    print('TimeoutException', e)
                print()
                counter += 1

    def skus_to_specs(self):
        spec_keys = ['Manufacturer', 'productGuide', 'mfgPart', 'Sku', 'Upc', 'Upc14', 'BatteryChemistry',
                     'numberOfCells', 'maximumBatteryRunTime', 'fingerPrintReader', 'frontCamera', 'Hdmi',
                     'networkRJ45', 'totalNumberOfUsbPorts', 'numberOfUsb3.0Ports', 'aspectRatio',
                     'screenResolution', 'screenSize', 'graphicsControllerManufacturer', 'graphicsControllerModel',
                     'graphicsMemoryTechnology', 'graphicsMemoryAccessibility', 'displayScreenTechnology',
                     'productType', 'manufacturerPartNumber', 'manufacturer', 'productModel', 'productName',
                     'productSeries', 'brandName', 'standardMemory', 'memoryTechnology', 'packageContents',
                     'greenCompliant', 'greenComplianceCertificate', 'bluetooth', 'wirelessLAN', 'wirelessLANStandard',
                     'weightApproximate', 'color', 'height', 'width', 'depth', 'opticalDriveType',
                     'solidStateDriveCapacity', 'processorSpeed', 'processorType', 'processorModel', 'processorCore',
                     'processorManufacturer', 'operatingSystem', 'operatingSystemArchitecture',
                     'operatingSystemPlatform', 'limitedWarranty', 'headphone.microphoneComboPort', 'microHdmi',
                     'touchScreen', 'flashMemoryCapacity',
                     ]
        # open spec's (output) csv
        output_csv_file = open('specs_output.csv', 'w', encoding='utf-8', newline='')
        csv_writer = csv.writer(output_csv_file)
        # read from upc's (input) csv
        with open('skus_input.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            counter = 0
            for row in reader:
                print(counter)
                if counter == 0:
                    # header
                    for key in spec_keys:
                        row.append(key)
                    print(row)
                    print()
                    csv_writer.writerow(row)
                    counter += 1
                    continue
                try:
                    # input: sku
                    # output: spec
                    spec_dict = get_spec(row[2])
                    for key in spec_keys:
                        if key in spec_dict.keys():
                            row.append(spec_dict[key])
                        else:
                            row.append('')
                    # print(row)
                    # write row to csv
                    csv_writer.writerow(row)
                except TimeoutException as e:
                    print('TimeoutException', e)
                print()
                counter += 1


class EbayClient(object):
    """
    ebayClient class - integrating with eBay API.
    Installation of 'ebay-python' sdk (and probably 'lxml' package) is a must. read more: https://github.com/timotheus/ebaysdk-python
    Currently the methods supports eBay's Finding, Trading APIs and insert data into Laptop model.
    """

    def __init__(self, **kwargs):
        """
        To create new instance provide appid and domain address (sandbox or production).
        sandbox: svcs.sandbox.ebay.com , PieceOfA-2f38-49cb-9727-a0baaf532e25
        prod: PieceOfA-ae60-404f-b9e8-963d4cb77c54
        """
        self.state = kwargs.get('state', 'production')
        self.min_price = kwargs.get('min_price', 800)
        self.max_price = kwargs.get('max_price', 850)
        self.item_deals = {}
        self.devid = '63ffcffb-5194-4b29-99f6-46243937f140'
        self.token = 'AgAAAA**AQAAAA**aAAAAA**EHIVVw**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6AEloelDpeFqAWdj6x9nY+seQ**RcUCAA**AAMAAA**1AYoROp8ljS5LeygbB7JOsWbm1WZ87v/CkBJue4l0DMf0daQme2sNhQCT+K2Kr2Bhs/GGdFEwJUMQYfzbZ8Dwob5FRLEWlfno6qiSnqVDKls2+cVfqi6NRfre53capvWz8PrFNU0wnn2FfDXN/41YAHxJXLCJRfHdLJGDxKKcjnCDZOkJNOnbZTs+qLwXBI6/iQqUrAi87PhoBu8G81GSphGj50hn/th60j14rmyu4MDJTR3Az5YcOQfNQRbty3iRBzfkbJwCpG0ilNKHBlDoS2E708othrY3nqGiZ6GAKt2EPJT2Bhq5vKze1hCuHY5KQe8513MRJRJ0L5uaCARRgT1Wsega2IkXfwV6oWlgVxe1zD002iCGBYI7pezRdAIaEbguX7dwSmU0ZWeoP3HMBHwSTfM6gv0AMIYkf0vCwDohdTx2M+FkAzOCQy03oaVWsH/iu+1ahguhiHojfkHsovc3cT5WB5E3oLObhGq1R2Uilt15rUQp4m8J1UILo5vTvwPpB3ctub4xSTd+onFdCtl4qnQfEBQ9Fh2TINB/ONpEt0EksdP3ghV6Yoys84Yy6Ii56YDuDEKWU45ekHJMOZW55XbZdM7v4jBx5y78KkFb99UNn+a+jPSGvHHUX/SDXwz5XEQ8s/S+C7LMiAZJ/8kVDQJFZIR58vJwCYOy2mIZZxddCy/a1TZaGfh/B87AaRMSN+aMMvKcetLyA/+3+/qb9+3eHGh5Gf5RRDfIfkmXowjNy/jhsG5GIwfNqe7'
        if self.state == 'production':
            # Production call
            self.domain = 'svcs.ebay.com'
            self.appid = 'PieceOfA-ae60-404f-b9e8-963d4cb77c54'
            self.certid = '275a3f6b-1ba6-4b6f-a276-0e8b90f94628'
        elif self.state == 'dev':
            # Sandbox call
            self.domain = 'svcs.sandbox.ebay.com'
            self.appid = 'PieceOfA-2f38-49cb-9727-a0baaf532e25'
            self.certid = 'b3c9c740-b8d2-47b7-8123-830aa3df9087'

    def __repr__(self):
        return "<EbayClient>"

    # def __getattr__(self, method):
    #     return ebayClient(self.domain, self.appid, '%s/%s' % (self.method, self.method))

    def fetch_deals(self):
        self.pull_laptop_deals(self.min_price, self.max_price)
        p_range = str(self.min_price) + '-' + str(self.max_price)
        print(len(self.item_deals[p_range]))
        self.save_deals(p_range)
        # self.json_to_csv()

    def create_csv(self):
        header = []
        with open(os.path.join(settings.BASE_DIR, 'deals.ebay.json'), 'r', encoding='utf-8') as ebay_deals:
            io_str = ebay_deals.read()
            json_parsed = json.loads(io_str)
            deals_data = json_parsed['ebay_deals']
            for item in deals_data:
                for key in item.keys():
                    if key not in header:
                        header.append(str(key))
            header.sort()
            # open a file for writing
            with open(os.path.join(settings.BASE_DIR, 'ebay.data.csv'), 'w', encoding='utf-8') as ebay_data:
                # create the csv writer object
                csv_writer = csv.writer(ebay_data)
                csv_writer.writerow(header)
                for item in deals_data:
                    item_values = []
                    for title in header:
                        if title in item.keys():
                            item_values.append(str(item[title]))
                        else:
                            item_values.append('')
                    csv_writer.writerow(item_values)
            ebay_data.close()
        ebay_deals.close()

    def save_deals(self, price_range=""):
        """
        Get dictionary with item deals details (range:list structure) and add item instances to the table.
        If specification name field does not exist in model - a new field will be create.
        :return:
        """
        if price_range in self.item_deals.keys():
            with open(os.path.join(settings.BASE_DIR, 'deals.ebay.json'), 'a', encoding='utf-8',
                      newline='') as deals_json:
                for items_in_range in self.item_deals[price_range]:
                    for items_group in items_in_range:
                        json.dump(items_group, deals_json, sort_keys=True, indent=4)
                        deals_json.write(',\n')
            deals_json.close()

    def pull_laptop_deals(self, min_price, max_price):
        """
        Pull all laptop items from 'Netbook and Laptop' (categoryId = 175672) and extract
        specific data from each deal.
        :param min_price:
        :param max_price:
        :return: List of eBay API laptops (dictionary) that contains specific deal details.
        """
        try:
            api = Finding(config_file=None, domain=self.domain, appid=self.appid)
            api_request = {
                'categoryId': '175672',
                # Useful Filters: Condition, ListingType, MinPrice, MaxPrice, Currency,
                # EndTimeFrom?, EndTimeTo?, StartTimeFrom?, StartTimeTo?, FeaturedOnly?,
                # FeedbackScoreMin?, HideDuplicateItems, LocatedIn?, TopRatedSellerOnly?,
                # Uselful output selectors: GalleryInfo, PictureURLLarge?, SellerInfo
                'itemFilter': [
                    {'name': 'Condition',
                     'value': 'New'},
                    {'name': 'ListingType',
                     'value': 'FixedPrice'},
                    {'name': 'MinPrice', 'value': min_price, 'paramName': 'Currency', 'paramValue': 'USD'},
                    {'name': 'MaxPrice', 'value': max_price, 'paramName': 'Currency', 'paramValue': 'USD'},
                    {'name': 'HideDuplicateItems', 'value': True},
                ],
                'outputSelector': ['GalleryInfo', 'SellerInfo'],
                'paginationInput': {'entriesPerPage': 100, 'pageNumber': 1},
                'sortOrder': 'PricePlusShippingLowest',
            }
            finding_response = api.execute('findItemsByCategory', api_request)
        except ConnectionError as e:
            print(e)
            print(e.response.dict())
            return e
        finding_ack = finding_response.dict()['ack']
        if finding_ack == 'Success':
            total_items = int(finding_response.dict()['paginationOutput']['totalEntries'])
            if total_items <= 10000:
                items = []
                items.append(self.get_deals(finding_response))
                total_pages = int(finding_response.dict()['paginationOutput']['totalPages'])
                page_number = int(finding_response.dict()['paginationOutput']['pageNumber'])
                while page_number <= total_pages:
                    try:
                        api = Finding(config_file=None, domain=self.domain, appid=self.appid)
                        api_request = {
                            'categoryId': '175672',
                            'itemFilter': [
                                {'name': 'Condition',
                                 'value': 'New'},
                                {'name': 'ListingType',
                                 'value': 'FixedPrice'},
                                {'name': 'MinPrice', 'value': min_price, 'paramName': 'Currency',
                                 'paramValue': 'USD'},
                                {'name': 'MaxPrice', 'value': max_price, 'paramName': 'Currency',
                                 'paramValue': 'USD'},
                                {'name': 'HideDuplicateItems', 'value': True},
                            ],
                            'outputSelector': ['GalleryInfo', 'SellerInfo'],
                            'paginationInput': {'entriesPerPage': 100, 'pageNumber': page_number + 1},
                            'sortOrder': 'PricePlusShippingLowest',
                        }
                        finding_response = api.execute('findItemsByCategory', api_request)
                    except ConnectionError as e:
                        print(e)
                        print(e.response.dict())
                        return e
                    finding_ack = finding_response.dict()['ack']
                    if finding_ack == 'Success':
                        items.append(self.get_deals(finding_response))
                    page_number += 1
                self.item_deals[str(min_price) + '-' + str(max_price)] = items
                return
            else:
                self.pull_laptop_deals(min_price, int(max_price / 2))
                self.pull_laptop_deals(int(max_price / 2) + 1, max_price)
                return
        return self.item_deals

    def get_deals(self, finding_response):
        """
        Extract item data (e.g specification, price, end time, etc.) using Finding and Trading APIs call.
        :param finding_response - sdk Response class from findItemsByCategory call (Finding API).
        :return List of items (dictionaries) that contains specific deal details
        """
        deal_list = []
        if 'searchResult' in finding_response.dict().keys():
            results = finding_response.dict()['searchResult']
            for item in results['item']:
                item_data = {}
                item_data['itemId'] = item['itemId']
                item_data['sellerFeedback'] = item['sellerInfo']['positiveFeedbackPercent']
                # GetItem Call: extract item data
                try:
                    api = Trading(config_file=None, appid=self.appid, devid=self.devid, certid=self.certid)
                    api_request = {
                        'ItemID': item['itemId'],
                        'RequesterCredentials': {'eBayAuthToken': self.token},
                        'DetailLevel': 'ReturnAll',
                        'IncludeItemSpecifics': True,
                    }
                    trading_response = api.execute('GetItem', api_request)
                except ConnectionError as e:
                    print(e)
                    print(e.response.dict())
                    return e
                trading_ack = trading_response.dict()['Ack']
                if trading_ack and 'Item' in trading_response.dict().keys():
                    trading_item = trading_response.dict()['Item']
                    # Extract item specifics (if exist) such as 'Screen Size'
                    if 'ItemSpecifics' in trading_item.keys():
                        # Iterate ItemSpecifics tag data
                        for spec in trading_item['ItemSpecifics']['NameValueList']:
                            if not isinstance(spec, str):
                                spec_name = str(spec['Name'])
                                if spec_name == 'Brand' or spec_name == 'UPC' or spec_name == 'MPN':
                                    item_data[spec_name] = str(spec['Value'])
                    # Extract listing details (if exist) such as 'Price'
                    if 'ListingDetails' in trading_item.keys():
                        if 'EndTime' in trading_item['ListingDetails'].keys():
                            item_data['dealEndTime'] = trading_item['ListingDetails']['EndTime']
                        if 'ConvertedStartPrice' in trading_item['ListingDetails'].keys():
                            item_data['Price'] = trading_item['ListingDetails']['ConvertedStartPrice']['value']
                        if 'ViewItemURL' in trading_item['ListingDetails'].keys():
                            item_data['URL'] = trading_item['ListingDetails']['ViewItemURL']
                            # Extract picture url (if exist) - usually return list (csv -> R conflict !!!)
                            # if 'PictureDetails' in trading_item.keys():
                            #     if 'PictureURL' in trading_item['PictureDetails'].keys():
                            #         item_data['Image'] = trading_item['PictureDetails']['PictureURL']
                            # Extract title (if exist)
                            # if 'Title' in trading_item.keys():
                            #     item_data['Title'] = trading_item['Title']
                deal_list.append(item_data)
            return deal_list
        else:
            print('Finding response does not have searchResult')

    def get_laptop_aspects(self):
        """
        Extract browsing data (e.g aspects and filters) from 'Netbook and Laptop' (categoryId = 175672)
        :return: Dictionary of all aspects from 'Netbook and Laptop' children categories merging ('Apple Laptops':111422
                , 'PC Laptops & Netbooks':177).
                Keys are aspects name and Values are List of aspects optional values.
        """
        try:
            api = Finding(config_file=None, domain=self.domain, appid=self.appid)
            api_request = [
                # Apple Laptops Aspect Histogram
                {
                    'categoryId': '111422',
                    'outputSelector': 'AspectHistogram',
                    'itemFilter': [
                        {'name': 'Condition',
                         'value': 'New'},
                        {'name': 'ListingType',
                         'value': 'FixedPrice'},
                    ],
                },
                # PC Laptops & Netbooks Aspect Histogram
                {
                    'categoryId': '177',
                    'outputSelector': 'AspectHistogram',
                    'itemFilter': [
                        {'name': 'Condition',
                         'value': 'New'},
                        {'name': 'ListingType',
                         'value': 'FixedPrice'},
                    ],
                }
            ]
            response_dict = {}
            for category_request in api_request:
                api_response = api.execute('findItemsByCategory', category_request)
                response_dict[category_request['categoryId']] = api_response.dict()
            laptop_aspects = {}
            for categoryId, response in response_dict.items():
                hist = response['aspectHistogramContainer']
                hist_aspects = hist['aspect']
                for aspect in hist_aspects:
                    if aspect['_name'] in laptop_aspects.keys():
                        for value in aspect['valueHistogram']:
                            if value['_valueName'] in laptop_aspects[aspect['_name']]:
                                continue
                            else:
                                laptop_aspects[aspect['_name']].append(value['_valueName'])
                    else:
                        aspect_values = []
                        for value in aspect['valueHistogram']:
                            aspect_values.append(value['_valueName'])
                        laptop_aspects[aspect['_name']] = aspect_values
            return laptop_aspects
        except ConnectionError as e:
            print(e)
            print(e.response.dict())

            # class DeliciousClient(object):
            #
            #     interval = 0
            #
            #     def __init__(self, username, password):
            #         self.username, self.password = username, password
            #
            #     def fetch(self, **params):
            #         delta = time.time() - DeliciousClient.interval
            #         if delta < 2:
            #             time.sleep(2 - delta)
            #         DeliciousClient.interval = time.time()
            #         url = 'https://%s:%s@api.del.icio.us/v1/posts/recent' % (self.username, self.password)
            #         return self.fetch_xml(url)
            #
            #     def fetch_xml(self, url):
            #         u = urllib.FancyURLopener(None)
            #         usock = u.open(url)
            #         rawdata = usock.read()
            #         usock.close()
            #         return xml_parser.fromstring(rawdata)
            #
            #     def __getattr__(self, method):
            #         return DeliciousClient(self.username, self.password, '%s/%s' % (self.method, method))
            #
            #     def __repr__(self):
            #         return "<DeliciousClient>"

            # def insert_laptop(data):
            #     """
            #     Insert new data to Laptop table (if it is not exist).
            #     :param data: data is a dictionary from ebay API response
            #     :return: none
            #     """
            #     for key, value in data.iteritems():
            #
            #         obj, created = Laptop.objects.get_or_create(
            #             first_name='John',
            #             last_name='Lennon',
            #             # defaults={'birthday': date(1940, 10, 9)}
            #         )

            # def create_link(data):
            #     for post in data.findall('post'):
            #         info = dict((k, smart_unicode(post.get(k))) for k in post.keys())
            #         b, created = Link.objects.get_or_create(
            #             url = info['href'],
            #             description = info['extended'],
            #             tags = info.get('tag', ''),
            #             date = parsedate(info['time']),
            #             title = info['description']
            #         )


class AmazonClient(object):
    """

    limits: one query per second per associate tag
    """

    def __init__(self, **kwargs):
        """
        To create new instance provide Amazon credentials:
            AWS_ACCESS_KEY_ID = AKIAJZXUIQUQZ34J3E5Q
            AWS_SECRET_ACCESS_KEY = 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
            AWS_ASSOCIATE_TAG = djaroo10-20
        """
        self.amazon_id = kwargs.get('amazon_id', 'AKIAJZXUIQUQZ34J3E5Q')
        self.amazon_key = kwargs.get('amazon_key', '6ZHpC651IZ6WmW0dC9Y9DfVO6ORYGYpR633zdbj/')
        self.amazon_tag = kwargs.get('amazon_tag', 'djaroo10-20')

    def __repr__(self):
        return "<AmazonClient>"

    # def __getattr__(self, method):
    #     return ebayClient(self.domain, self.appid, '%s/%s' % (self.method, self.method))

    def pull_upc(self):
        # pull upc list from existing csv file
        upcs = []
        with open(os.path.join(settings.BASE_DIR, 'ebayUniqueUpcList.txt'), 'r', encoding='utf-8') as amazon_data:
            # create the csv writer object
            # csv_reader = csv.reader(amazon_data)
            for upc_raw in amazon_data:
                upcs.append(upc_raw.split('\n')[0])
        amazon_data.close()
        print(upcs)
        return upcs

    def save_deals(self, amazon_deals):
        # save list of deals (dict) to json file
        with open(os.path.join(settings.BASE_DIR, 'deals.amazon.json'), 'a', encoding='utf-8',
                  newline='') as deals_json:
            for items_group in amazon_deals:
                json.dump(items_group, deals_json, sort_keys=True, indent=4)
                deals_json.write(',\n')
        deals_json.close()

    def create_csv(self):
        # save json data to new csv file
        header = []
        with open(os.path.join(settings.BASE_DIR, 'deals.amazon.json'), 'r', encoding='utf-8') as amazon_deals:
            io_str = amazon_deals.read()
            json_parsed = json.loads(io_str)
            deals_data = json_parsed['amazon_deals']
            for item in deals_data:
                for key in item.keys():
                    if key not in header:
                        header.append(str(key))
            header.sort()
            # open a file for writing
            with open(os.path.join(settings.BASE_DIR, 'amazon.data.csv'), 'w', encoding='utf-8') as amazon_data:
                # create the csv writer object
                csv_writer = csv.writer(amazon_data)
                csv_writer.writerow(header)
                for item in deals_data:
                    item_values = []
                    for title in header:
                        if title in item.keys():
                            item_values.append(str(item[title]))
                        else:
                            item_values.append('')
                    csv_writer.writerow(item_values)
            amazon_data.close()
        amazon_deals.close()

    def fetch_deals(self):
        amazon_deals = []
        counter = 0
        upc_list = self.pull_upc()
        print('successful UPC extraction')
        # Extraction rate: 1 request per second, 5 second sleep for 10 items batch  ; Call limit: 3600 per hour
        for item_upc in upc_list:
            if counter % 10 == 0:
                # 5 second sleep to avoid timeout error
                time.sleep(5)
                print('5 sec break')
            item_dict = self.get_item(item_upc)
            if item_dict:
                amazon_deals.append(item_dict)
            counter += 1
        print('successful amazon deals data extraction')
        self.save_deals(amazon_deals)
        # reconstruct json and than execute create_csv
        # self.create_csv()

    def get_item(self, upc='887276124025'):
        """

        :param upc:
        :return:
        """
        amazon_data = {}
        amazon = bottlenose.Amazon(self.amazon_id, self.amazon_key, self.amazon_tag, MaxQPS=0.9)
        # Item lookup call: IdType=UPC , SearchIndex=Electronics (US market) , node=493964
        amazon_response = amazon.ItemLookup(ItemId=upc, ResponseGroup='Large', SearchIndex='Electronics',
                                            IdType='UPC')
        response_elem = objectify.fromstring(amazon_response.decode('utf-8'))
        item_path = objectify.ObjectPath("ItemLookupResponse.Items.Item")
        if item_path.hasattr(response_elem):
            # Extract data from Amazon xml response
            for amazon_attr in response_elem.Items.Item.iterchildren("*"):
                tag_str = amazon_attr.tag
                medium_tag = tag_str.split('}')[1]
                if not amazon_attr.text:
                    obj_data = self.breake_obj(amazon_attr, {})
                    amazon_data.update(obj_data)
                else:
                    amazon_data[medium_tag] = str(amazon_attr.text)
        else:
            print('The following UPC does not contain Item tag: ' + upc)
        return amazon_data

    def breake_obj(self, attr_obj, obj_data):
        """

        :param attr_obj:
        :param obj_data:
        :return:
        """
        if attr_obj.text:
            obj_tag = attr_obj.tag.split('}')[1]
            parent_tag = attr_obj.getparent().tag.split('}')[1]
            full_tag = str(parent_tag + '>' + obj_tag)
            obj_data[full_tag] = self.val_insert(full_tag, attr_obj.text, obj_data)
            # print('break_obj_simple_str: tag: '+full_tag+' val: '+obj_data[full_tag])
            return obj_data
        else:
            for sub_attr in attr_obj.iterchildren("*"):
                obj_tag = sub_attr.tag.split('}')[1]
                parent_tag = sub_attr.getparent().tag.split('}')[1]
                full_tag = str(parent_tag + '>' + obj_tag)
                if not sub_attr.text:
                    if full_tag == 'ItemAttributes>Feature':
                        print('object child (recursion): ' + full_tag)
                        print(type(attr_obj))
                        print(attr_obj.text)
                    obj_dict = self.breake_obj(sub_attr, {})
                    obj_data.update(obj_dict)
                    if full_tag == 'ItemAttributes>Feature':
                        print('obj_data after executing ' + full_tag)
                        # print(obj_data)
                else:
                    obj_data[full_tag] = self.val_insert(full_tag, sub_attr.text, obj_data)
                    # print('simple child (base type): '+full_tag+' with value:'+obj_data[full_tag])
        return obj_data

    def val_insert(self, tag_name, tag_value, item_dict):
        """

        :param tag_name:
        :param tag_value:
        :param item_dict:
        :return:
        """
        if tag_name in item_dict.keys():
            if isinstance(item_dict[tag_name], list):
                item_dict[tag_name].append(str(tag_value))
                return item_dict[tag_name]
            else:
                multi_values = [item_dict[tag_name], str(tag_value), ]
                return multi_values
        else:
            return str(tag_value)
            # get list of upc -> for each upc extract details ->  get large response -> parse xml -> save to self.item_deals -> export to json -> export to csv
