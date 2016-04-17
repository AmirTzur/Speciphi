# import time
# import os
# import sys

# eBay-Python sdk
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError

# model to store local data from eBay
from .models import Laptop


class ebayClient(object):
    """
    ebayClient class - integrating with eBay API.
    Installation of 'ebay-python' sdk (and probably 'lxml' package) is a must. read more: https://github.com/timotheus/ebaysdk-python
    Currently the methods supports eBay Finding API and insert data into Laptop model.
    """

    # interval = 0


    def __init__(self, state='production'):
        """
        To create new instance provide appid and domain address (sandbox or production).
        sandbox: svcs.sandbox.ebay.com , PieceOfA-2f38-49cb-9727-a0baaf532e25
        prod: PieceOfA-ae60-404f-b9e8-963d4cb77c54
        """

        self.state = state
        if state == 'production':
            # Production call (EBAY-US - default 'site_id')
            self.domain = 'svcs.ebay.com'
            self.appid = 'PieceOfA-ae60-404f-b9e8-963d4cb77c54'
        elif state == 'dev':
            # Sandbox call
            self.domain = 'svcs.sandbox.ebay.com'
            self.appid = 'PieceOfA-2f38-49cb-9727-a0baaf532e25'

    def stack_call(self):

        try:
            api = Finding(config_file=None, domain='svcs.sandbox.ebay.com',
                          appid='PieceOfA-2f38-49cb-9727-a0baaf532e25', siteid='EBAY-GB')
            response = api.execute('findItemsAdvanced', {
                'keywords': 'laptop',
                'categoryId': ['177', '111422'],
                'itemFilter': [
                    {'name': 'Condition', 'value': 'Used'},
                    {'name': 'MinPrice', 'value': '200', 'paramName': 'Currency', 'paramValue': 'GBP'},
                    {'name': 'MaxPrice', 'value': '400', 'paramName': 'Currency', 'paramValue': 'GBP'}
                ],
                'paginationInput': {
                    'entriesPerPage': '25',
                    'pageNumber': '1'
                },
                'sortOrder': 'CurrentPriceHighest'
            })
            print(response.dict())
            return response.dict()

        except ConnectionError as e:
            print(e)
            print(e.response.dict())


    def get_laptop_hist(self):
        """
        Search for optional filter aspects in 'Netbook and Laptop' (category id 175672).
        :return: List with category aspects
        """

        api_request = {
            'categoryId': '177',
            'outputSelector': 'AspectHistogram',
            # 'affiliate': {'trackingId': 1},
        }
            # 'itemFilter': [
            #     {'name': 'Condition',
            #      'value': 'New'},
            #     {'name': 'ListingType',
            #      'value': 'FixedPrice'},
            #     ],
                # {'name': 'MinPrice',
                #  'value': '200',
                #  'paramName': 'Currency',
                #  'paramValue': 'USD'
                #  },
                # {'name': 'MaxPrice',
                #  'value': '400',
                #  'paramName': 'Currency',
                #  'paramValue': 'USD'
                #  },
            # 'affiliate': {'trackingId': 1},
            # 'outputSelector': 'AspectHistogram',
            # 'sortOrder': 'CountryDescending',
            # 'paginationInput': '100',
        # api_request = {
        #         'keywords': 'laptop',
        #         'itemFilter': [
        #             {'name': 'Condition',
        #              'value': 'Used'},
        #             {'name': 'LocatedIn',
        #              'value': 'GB'},
        #         ],
        #         'paginationInput': {'entriesPerPage': 2},
        #         'affiliate': {'trackingId': 1},
        #         'sortOrder': 'CountryDescending',
        #     }

        try:
            # Finding call: (1) siteid = 'EBAY-US' (default) -- eBay country site id ,
            # (2) timeout = 20 (default) -- HTTP request timeout, (3) response_encoding = 'XML' (default) -- API encoding.
            api = Finding(config_file=None, domain=self.domain, appid=self.appid)
            response = api.execute('findItemsByCategory', api_request)
        except ConnectionError as e:
            print(e)
            print(e.response.dict())
            return e

        rs_dict = response.json()
        # for aspect in rs_dict['aspectHistogramContainer']['aspect']:
        #     print('## aspect %d ###' % aspect)
        #     print(rs_dict['aspectHistogramContainer']['aspect'](aspect))
        print(response.dom())
        return response
        # response_dict = response.dict()
        # for aspect in response.dict()['aspectHistogramContainer']['aspect']:
        #     print('## aspect ###')
        #     print(aspect.keys())
        # for aspect in response.dict()['aspectHistogramContainer']:
        #     print('## aspect ###')
        #     print(aspect)


    def example_call(self):
        """
        Get 'Netbook and Laptop' category items by price range (e.g min_price and max_price)
        """
        #eBay API rule: you can’t ping it more frequently than once per second.
        # The code below ensures that we don’t exceed that limit.
        # delta = time.time() - ebayClient.interval
        # if delta > 2:
        #     time.sleep(2 - delta)
        # ebayClient.interval = time.time()
        try:
            api = Finding(config_file=None, domain=self.domain, appid=self.appid)
            api_request = {

            }
            response = api.execute('findItemsByCategory', api_request)
            print(response.dict())
            return response.dict()
        except ConnectionError as e:
            print(e)
            print(e.response.dict())

    def __repr__(self):
        return "<ebayClient>"

    def __getattr__(self, method):
        return ebayClient(self.domain, self.appid, '%s/%s' % (self.method, self.method))


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


