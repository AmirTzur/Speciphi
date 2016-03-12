from django import template

register = template.Library()


def key(d, key_name):
    """Key filter return dictionary value for a given key"""
    return d[key_name]


key = register.filter('key', key)


def keylist1(d, key_name):
    return d[key_name][0]


keylist1 = register.filter('keylist1', keylist1)


def keylist2(d, key_name):
    return d[key_name][1]


keylist2 = register.filter('keylist2', keylist2)
