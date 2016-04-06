import time

#eBay-Python sdk
from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
#eBay model to store local data
from .models import Laptop


class ebayClient(object):
    """
    ebayClient class - integrating with eBay API.
    Installation of 'ebay-python' sdk (and probably 'lxml' package) is a must. read more: https://github.com/timotheus/ebaysdk-python
    Currently the methods supports eBay Finding API and insert data into Laptop model.
    """

    interval = 0

    def __init__(self, domain, appid):
        """
        To create new instance provide appid and domain address (sandbox or production).
        sandbox: svcs.sandbox.ebay.com , PieceOfA-2f38-49cb-9727-a0baaf532e25
        prod: PieceOfA-ae60-404f-b9e8-963d4cb77c54
        """
        self.domain = domain
        self.appid = appid

    def laptop_by_price(self):
        """
        Get 'Netbook and Laptop' category items by price range (e.g min_price and max_price)
        """
        #eBay API rule: you can’t ping it more frequently than once per second.
        # The code below ensures that we don’t exceed that limit.
        delta = time.time() - ebayClient.interval
        if delta > 2:
            time.sleep(2 - delta)
        ebayClient.interval = time.time()
        try:
            if self.domain == "svcs.sandbox.ebay.com":
                #sandbox call
                api = Finding(domain=self.domain, appid=self.appid)
            else:
                #production call (EBAY-US - default 'site_id')
                api = Finding(appid=self.appid)
            api_request = {
                'keywords': u'laptop',
                'itemFilter': [
                    {'name': 'Condition',
                     'value': 'Used'},
                    {'name': 'LocatedIn',
                     'value': 'GB'},
                ],
                'affiliate': {'trackingId': 1},
                'sortOrder': 'CountryDescending',
            }
            response = api.execute('findItemsAdvanced', api_request)
            print(response.dict())
            return response.dict()
        except ConnectionError as e:
            print(e)
            print(e.response.dict())

    def __repr__(self):
        return "<ebayClient>"

    def __getattr__(self, method):
        return ebayClient(self.domain, self.appid, '%s/%s' % (self.method, self.method))

    # def laptop_by_price1(self):
    #     try:
    #         if self.domain == "svcs.sandbox.ebay.com":
    #             #sandbox call
    #             api = Finding(domain=self.domain, appid=self.appid)
    #         else:
    #             #production call (EBAY-US - default 'site_id')
    #             api = Finding(appid=self.appid)
    #         api_request = {
    #             'keywords': u'laptop',
    #             'itemFilter': [
    #                 {'name': 'Condition',
    #                  'value': 'Used'},
    #                 {'name': 'LocatedIn',
    #                  'value': 'GB'},
    #             ],
    #             'affiliate': {'trackingId': 1},
    #             'sortOrder': 'CountryDescending',
    #         }
    #         response = api.execute('findItemsAdvanced', api_request)
    #         print(response.dict())
    #     except ConnectionError as e:
    #         print(e)
    #         print(e.response.dict())

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

def insert_laptop(data):
    """
    Insert new data to Laptop table (if it is not exist).
    :param data: data is a dictionary from ebay API response
    :return: none
    """
    for key, value in data.iteritems():

        obj, created = Laptop.objects.get_or_create(
            first_name='John',
            last_name='Lennon',
            # defaults={'birthday': date(1940, 10, 9)}
        )

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


