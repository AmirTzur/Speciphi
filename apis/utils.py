import os
import json
import csv

from django.conf import settings

# eBay-Python sdk
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection as Finding
from ebaysdk.trading import Connection as Trading

# model to store local data from eBay
from .models import EbayLaptopAspect, EbayLaptopDeal


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
        self.min_price = kwargs.get('min_price', 200)
        self.max_price = kwargs.get('max_price', 250)
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
        return "<ebayClient>"

    # def __getattr__(self, method):
    #     return ebayClient(self.domain, self.appid, '%s/%s' % (self.method, self.method))

    def fetch_deals(self, min_price, max_price):
        self.pull_laptop_deals(min_price, max_price)
        p_range = str(min_price) + '-' + str(max_price)
        print(len(self.item_deals[p_range]))
        self.add_deals_json(p_range)

    def json_to_csv(self):
        header = []
        with open(os.path.join(settings.BASE_DIR, 'deals.ebay.json'), 'r', encoding='utf-8') as ebay_deals:
            io_str = ebay_deals.read()
            json_parsed = json.loads(io_str)
            deals_data = json_parsed['ebay_deals']
            for item in deals_data:
                for key in item.keys():
                    if key not in header:
                        header.append(key)
            # open a file for writing
            with open(os.path.join(settings.BASE_DIR, 'ebay.data.csv'), 'w', encoding='utf-8') as ebay_data:
                # create the csv writer object
                csv_writer = csv.writer(ebay_data)
                csv_writer.writerow(header)
                for item in deals_data:
                    item_values = []
                    for title in header:
                        if title in item.keys():
                            item_values.append(item[title])
                        else:
                            item_values.append('')
                    csv_writer.writerow(item_values)
            ebay_data.close()
        ebay_deals.close()


    def add_deals_json(self, price_range=""):
        """
        Get dictionary with item deals details (range:list structure) and add item instances to the table.
        If specification name field does not exist in model - a new field will be create.
        :return:
        """
        if price_range in self.item_deals.keys():
            with open(os.path.join(settings.BASE_DIR, 'deals.ebay.json'), 'a', encoding='utf-8', newline='') as deals_json:
                for items_in_range in self.item_deals[price_range]:
                    for items_group in items_in_range:
                        json.dump(items_group, deals_json, sort_keys=True, indent=4)
                        deals_json.write(',\n')
            deals_json.close()

        # for items_in_range in self.item_deals.values():
        #             for item_group in items_in_range:
        #                 for item in item_group:
        #                     for spec_name, spec_val in item.items():
        #                         # insert to spec_name field if exist, else create new filed
        #                         if spec_name:
        #                             return
        #                         else:
        #                             return

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
                                {'name': 'MinPrice', 'value': min_price, 'paramName': 'Currency', 'paramValue': 'USD'},
                                {'name': 'MaxPrice', 'value': max_price, 'paramName': 'Currency', 'paramValue': 'USD'},
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
                self.pull_laptop_deals(min_price, int(max_price/2))
                self.pull_laptop_deals(int(max_price/2)+1, max_price)
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
                        for spec in trading_item['ItemSpecifics']['NameValueList']:
                            if not isinstance(spec, str):
                                item_data[spec['Name']] = spec['Value']
                    # Extract listing details (if exist) such as 'Price'
                    if 'ListingDetails' in trading_item.keys():
                        item_data['dealEndTime'] = trading_item['ListingDetails']['EndTime']
                        item_data['price'] = trading_item['ListingDetails']['ConvertedStartPrice']['value']
                        item_data['URL'] = trading_item['ListingDetails']['ViewItemURL']
                    # Extract picture url (if exist)
                    if 'PictureDetails' in trading_item.keys():
                        if 'PictureURL' in trading_item['PictureDetails'].keys():
                            item_data['image'] = trading_item['PictureDetails']['PictureURL']
                    # Extract title (if exist)
                    if 'Title' in trading_item.keys():
                        item_data['title'] = trading_item['Title']
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


