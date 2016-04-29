# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Entrances(models.Model):
    ip = models.CharField(max_length=16)
    country = models.CharField(max_length=45, blank=True, null=True)
    entrancedatetime = models.DateTimeField(db_column='entranceDateTime')  # Field name made lowercase.
    exitdatetime = models.DateTimeField(db_column='exitDateTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'entrances'

class AccountEmailaddress(models.Model):
    email = models.CharField(unique=True, max_length=254, blank=True, null=True)
    verified = models.IntegerField()
    primary = models.IntegerField()
    user = models.ForeignKey('AuthUser')

    class Meta:
        managed = False
        db_table = 'account_emailaddress'


class AccountEmailconfirmation(models.Model):
    created = models.DateTimeField()
    sent = models.DateTimeField(blank=True, null=True)
    key = models.CharField(unique=True, max_length=64)
    email_address = models.ForeignKey(AccountEmailaddress)

    class Meta:
        managed = False
        db_table = 'account_emailconfirmation'


class Advices(models.Model):
    advisors = models.ForeignKey('Advisors', db_column='Advisors_id')  # Field name made lowercase.
    context = models.TextField()
    creationdatetime = models.DateTimeField(db_column='creationDateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'advices'


class Advisors(models.Model):
    name = models.CharField(unique=True, max_length=45)
    specialty = models.CharField(max_length=45, blank=True, null=True)
    creationdatetime = models.DateTimeField(db_column='creationDateTime')  # Field name made lowercase.
    description = models.TextField()
    image = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'advisors'


class Affiliationadvices(models.Model):
    products = models.ForeignKey('Affiliations', db_column='Products_id')  # Field name made lowercase.
    affiliations = models.ForeignKey('Affiliations', db_column='Affiliations_id')  # Field name made lowercase.
    advisors = models.ForeignKey(Advices, db_column='Advisors_id')  # Field name made lowercase.
    advices = models.ForeignKey(Advices, db_column='Advices_id')  # Field name made lowercase.
    relevancelevel = models.FloatField(db_column='relevanceLevel')  # Field name made lowercase.
    lastupdate = models.DateTimeField(db_column='lastUpdate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'affiliationadvices'
        unique_together = (('Products_id', 'Affiliations_id', 'Advisors_id', 'Advices_id'),)


class Affiliationlevelofuses(models.Model):
    products = models.ForeignKey('Levelofuse', db_column='Products_id')  # Field name made lowercase.
    affiliations = models.ForeignKey('Affiliations', db_column='Affiliations_id')  # Field name made lowercase.
    uses = models.ForeignKey('Levelofuse', db_column='Uses_id')  # Field name made lowercase.
    levelofuse = models.ForeignKey('Levelofuse', db_column='levelofUse_id')  # Field name made lowercase.
    levelofuse_value = models.ForeignKey('Levelofuse', db_column='levelofUse_value')  # Field name made lowercase.
    lastupdate = models.DateTimeField(db_column='lastUpdate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'affiliationlevelofuses'
        unique_together = (('Products_id', 'Affiliations_id', 'Uses_id', 'levelofUse_id'),)


class Affiliationquestions(models.Model):
    products = models.ForeignKey('Focalizationquestions', db_column='Products_id')  # Field name made lowercase.
    affiliations = models.ForeignKey('Affiliations', db_column='Affiliations_id')  # Field name made lowercase.
    focalizationcategories = models.ForeignKey('Focalizationquestions', db_column='focalizationCategories_id')  # Field name made lowercase.
    focalizationquestions = models.ForeignKey('Focalizationquestions', db_column='focalizationQuestions_id')  # Field name made lowercase.
    importancelevel = models.FloatField(db_column='importanceLevel')  # Field name made lowercase.
    lastupdate = models.DateTimeField(db_column='lastUpdate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'affiliationquestions'
        unique_together = (('Products_id', 'Affiliations_id', 'focalizationCategories_id', 'focalizationQuestions_id'),)


class Affiliations(models.Model):
    products = models.ForeignKey('Products', db_column='Products_id')  # Field name made lowercase.
    name = models.CharField(max_length=45)
    description = models.TextField()
    image = models.TextField(blank=True, null=True)
    creationdatetime = models.DateTimeField(db_column='creationDateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'affiliations'
        unique_together = (('Products_id', 'name'),)


class Affiliationuses(models.Model):
    products = models.ForeignKey('Uses', db_column='Products_id')  # Field name made lowercase.
    affiliations = models.ForeignKey(Affiliations, db_column='Affiliations_id')  # Field name made lowercase.
    uses = models.ForeignKey('Uses', db_column='Uses_id')  # Field name made lowercase.
    fittinglevel = models.FloatField(db_column='fittingLevel')  # Field name made lowercase.
    lastupdate = models.DateTimeField(db_column='lastUpdate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'affiliationuses'
        unique_together = (('Affiliations_id', 'Uses_id'),)


class Answerstouses(models.Model):
    products = models.ForeignKey('Levelofuse', db_column='Products_id')  # Field name made lowercase.
    focalizationcategories = models.ForeignKey('Focalizationanswers', db_column='focalizationCategories_id')  # Field name made lowercase.
    focalizationquestions = models.ForeignKey('Focalizationanswers', db_column='focalizationQuestions_id')  # Field name made lowercase.
    focalizationanswers_value = models.ForeignKey('Focalizationanswers', db_column='focalizationAnswers_value')  # Field name made lowercase.
    uses = models.ForeignKey('Levelofuse', db_column='Uses_id')  # Field name made lowercase.
    levelofuse_value = models.ForeignKey('Levelofuse', db_column='levelofUse_value')  # Field name made lowercase.
    lastupdate = models.DateTimeField(db_column='lastUpdate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'answerstouses'
        unique_together = (('Products_id', 'focalizationCategories_id', 'focalizationQuestions_id', 'focalizationAnswers_value', 'Uses_id', 'levelofUse_value'),)


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group_id', 'permission_id'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type_id', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user_id', 'permission_id'),)


class Brands(models.Model):
    name = models.CharField(unique=True, max_length=45)
    description = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'brands'


class Categories(models.Model):
    name = models.CharField(unique=True, max_length=45)
    creationdatetime = models.DateTimeField(db_column='creationDateTime')  # Field name made lowercase.
    image = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categories'


class Categoryproducts(models.Model):
    categories = models.ForeignKey(Categories, db_column='Categories_id')  # Field name made lowercase.
    products = models.ForeignKey('Products', db_column='Products_id')  # Field name made lowercase.
    creationdatetime = models.DateTimeField(db_column='creationDateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'categoryproducts'
        unique_together = (('Categories_id', 'Products_id'),)


class Categoryselections(models.Model):
    entrances = models.ForeignKey('Entrances', db_column='Entrances_id')  # Field name made lowercase.
    categories = models.ForeignKey(Categories, db_column='Categories_id')  # Field name made lowercase.
    selectiondatetime = models.DateTimeField(db_column='selectionDateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'categoryselections'
        unique_together = (('Entrances_id', 'Categories_id', 'selectionDateTime'),)


class Checkeddeals(models.Model):
    entrances_id = models.IntegerField(db_column='Entrances_id')  # Field name made lowercase.
    consultationprocesses = models.ForeignKey('Consultationprocesses', db_column='consultationProcesses_id')  # Field name made lowercase.
    products_id = models.IntegerField(db_column='Products_id')  # Field name made lowercase.
    vendors_id = models.IntegerField(db_column='Vendors_id')  # Field name made lowercase.
    brands_id = models.IntegerField(db_column='Brands_id')  # Field name made lowercase.
    models_id = models.IntegerField(db_column='Models_id')  # Field name made lowercase.
    deals = models.ForeignKey('Deals', db_column='Deals_id')  # Field name made lowercase.
    selectiondatetime = models.DateTimeField(db_column='selectionDateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'checkeddeals'
        unique_together = (('Entrances_id', 'consultationProcesses_id', 'Vendors_id', 'Brands_id', 'Models_id', 'Deals_id', 'selectionDateTime'),)


class Checkedreviews(models.Model):
    entrances_id = models.IntegerField(db_column='Entrances_id')  # Field name made lowercase.
    consultationprocesses = models.ForeignKey('Consultationprocesses', db_column='consultationProcesses_id')  # Field name made lowercase.
    products_id = models.IntegerField(db_column='Products_id')  # Field name made lowercase.
    brands_id = models.IntegerField(db_column='Brands_id')  # Field name made lowercase.
    models_id = models.IntegerField(db_column='Models_id')  # Field name made lowercase.
    reviewers_id = models.IntegerField(db_column='Reviewers_id')  # Field name made lowercase.
    reviews = models.ForeignKey('Reviews', db_column='Reviews_id')  # Field name made lowercase.
    selectiondatetime = models.DateTimeField(db_column='selectionDateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'checkedreviews'
        unique_together = (('consultationProcesses_id', 'Reviews_id', 'selectionDateTime'),)


class Comparisonmodels(models.Model):
    entrances_id = models.IntegerField(db_column='Entrances_id')  # Field name made lowercase.
    consultationprocesses = models.ForeignKey('Consultationprocesses', db_column='consultationProcesses_id')  # Field name made lowercase.
    products = models.ForeignKey('Models', db_column='Products_id')  # Field name made lowercase.
    brands = models.ForeignKey('Models', db_column='Brands_id')  # Field name made lowercase.
    models = models.ForeignKey('Models', db_column='Models_id')  # Field name made lowercase.
    selectiondatetime = models.CharField(db_column='selectionDateTime', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'comparisonmodels'
        unique_together = (('consultationProcesses_id', 'Products_id', 'Brands_id', 'Models_id', 'selectionDateTime'),)


class Consultationadvices(models.Model):
    entrances_id = models.IntegerField(db_column='Entrances_id')  # Field name made lowercase.
    products_id = models.IntegerField(db_column='Products_id')  # Field name made lowercase.
    consultationprocesses = models.ForeignKey('Consultationprocesses', db_column='consultationProcesses_id')  # Field name made lowercase.
    advisors = models.ForeignKey(Advices, db_column='Advisors_id')  # Field name made lowercase.
    advices = models.ForeignKey(Advices, db_column='Advices_id')  # Field name made lowercase.
    selectiondatetime = models.DateTimeField(db_column='selectionDateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'consultationadvices'
        unique_together = (('Products_id', 'consultationProcesses_id', 'Advisors_id', 'Advices_id', 'selectionDateTime'),)


class Consultationprocesses(models.Model):
    entrances = models.ForeignKey('Entrances', db_column='Entrances_id')  # Field name made lowercase.
    products = models.ForeignKey('Products', db_column='Products_id')  # Field name made lowercase.
    startdatetime = models.DateTimeField(db_column='startDateTime')  # Field name made lowercase.
    enddatetime = models.DateTimeField(db_column='endDateTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'consultationprocesses'


class Consulteeaffiliations(models.Model):
    entrances_id = models.IntegerField(db_column='Entrances_id')  # Field name made lowercase.
    products_id = models.IntegerField(db_column='Products_id')  # Field name made lowercase.
    consultationprocesses = models.ForeignKey(Consultationprocesses, db_column='consultationProcesses_id')  # Field name made lowercase.
    affiliations = models.ForeignKey(Affiliations, db_column='Affiliations_id')  # Field name made lowercase.
    selectiondatetime = models.DateTimeField(db_column='selectionDateTime')  # Field name made lowercase.
    checked = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'consulteeaffiliations'
        unique_together = (('consultationProcesses_id', 'selectionDateTime'),)


class Consulteehardpreferences(models.Model):
    entrances_id = models.IntegerField(db_column='Entrances_id')  # Field name made lowercase.
    consultationprocesses = models.ForeignKey(Consultationprocesses, db_column='consultationProcesses_id')  # Field name made lowercase.
    products = models.ForeignKey('Specfeatures', db_column='Products_id')  # Field name made lowercase.
    specfeatures = models.ForeignKey('Specfeatures', db_column='specFeatures_id')  # Field name made lowercase.
    selectiondatetime = models.DateTimeField(db_column='selectionDateTime')  # Field name made lowercase.
    minspeclevel = models.FloatField(db_column='minSpecLevel')  # Field name made lowercase.
    maxspeclevel = models.FloatField(db_column='maxSpecLevel')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'consulteehardpreferences'
        unique_together = (('consultationProcesses_id', 'Products_id', 'specFeatures_id', 'selectionDateTime'),)


class Consulteeuses(models.Model):
    entrances_id = models.IntegerField(db_column='Entrances_id')  # Field name made lowercase.
    products = models.ForeignKey('Levelofuse', db_column='Products_id')  # Field name made lowercase.
    consultationprocesses = models.ForeignKey(Consultationprocesses, db_column='consultationProcesses_id')  # Field name made lowercase.
    uses = models.ForeignKey('Levelofuse', db_column='Uses_id')  # Field name made lowercase.
    levelofuse_value = models.ForeignKey('Levelofuse', db_column='levelofUse_value')  # Field name made lowercase.
    selectiondatetime = models.DateTimeField(db_column='selectionDateTime')  # Field name made lowercase.
    checked = models.IntegerField()
    checkedbyuser = models.IntegerField(db_column='checkedByUser')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'consulteeuses'
        unique_together = (('consultationProcesses_id', 'Uses_id'),)


class Deals(models.Model):
    products = models.ForeignKey('Models', db_column='Products_id')  # Field name made lowercase.
    vendors = models.ForeignKey('Vendors', db_column='Vendors_id')  # Field name made lowercase.
    brands = models.ForeignKey('Models', db_column='Brands_id')  # Field name made lowercase.
    models = models.ForeignKey('Models', db_column='Models_id')  # Field name made lowercase.
    code = models.CharField(max_length=45)
    websiteurl = models.CharField(db_column='webSiteURL', max_length=2083)  # Field name made lowercase.
    price = models.FloatField()
    rank = models.FloatField()

    class Meta:
        managed = False
        db_table = 'deals'
        unique_together = (('code', 'id'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSite(models.Model):
    domain = models.CharField(max_length=100)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'django_site'


class Focalizationanswers(models.Model):
    products = models.ForeignKey('Focalizationquestions', db_column='Products_id')  # Field name made lowercase.
    focalizationcategories = models.ForeignKey('Focalizationquestions', db_column='focalizationCategories_id')  # Field name made lowercase.
    focalizationquestions = models.ForeignKey('Focalizationquestions', db_column='focalizationQuestions_id')  # Field name made lowercase.
    value = models.IntegerField()
    context = models.TextField()

    class Meta:
        managed = False
        db_table = 'focalizationanswers'
        unique_together = (('Products_id', 'focalizationCategories_id', 'focalizationQuestions_id', 'value'),)


class Focalizationcategories(models.Model):
    products = models.ForeignKey('Products', db_column='Products_id')  # Field name made lowercase.
    creationdatetime = models.DateTimeField(db_column='creationDateTime')  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'focalizationcategories'


class Focalizationquestions(models.Model):
    products = models.ForeignKey(Focalizationcategories, db_column='Products_id')  # Field name made lowercase.
    focalizationcategories = models.ForeignKey(Focalizationcategories, db_column='focalizationCategories_id')  # Field name made lowercase.
    headline = models.TextField(db_column='headLine')  # Field name made lowercase.
    context = models.TextField()
    creationdatetime = models.DateTimeField(db_column='creationDateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'focalizationquestions'


class Levelofuse(models.Model):
    creationdatetime = models.DateTimeField(db_column='creationDateTime')  # Field name made lowercase.
    products = models.ForeignKey('Uses', db_column='Products_id')  # Field name made lowercase.
    uses = models.ForeignKey('Uses', db_column='Uses_id')  # Field name made lowercase.
    value = models.IntegerField()
    name = models.CharField(max_length=45, blank=True, null=True)
    description = models.TextField()
    lastupdate = models.DateTimeField(db_column='lastUpdate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'levelofuse'
        unique_together = (('Products_id', 'Uses_id', 'value'),)


class Levelofuseadvices(models.Model):
    products = models.ForeignKey(Levelofuse, db_column='Products_id')  # Field name made lowercase.
    uses = models.ForeignKey(Levelofuse, db_column='Uses_id')  # Field name made lowercase.
    levelofuse_value = models.ForeignKey(Levelofuse, db_column='levelofUse_value')  # Field name made lowercase.
    advisors = models.ForeignKey(Advices, db_column='Advisors_id')  # Field name made lowercase.
    advices = models.ForeignKey(Advices, db_column='Advices_id')  # Field name made lowercase.
    relevancelevel = models.FloatField(db_column='relevanceLevel')  # Field name made lowercase.
    lastupdate = models.DateTimeField(db_column='lastUpdate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'levelofuseadvices'
        unique_together = (('Products_id', 'Uses_id', 'levelofUse_value', 'Advisors_id', 'Advices_id'),)


class Levelofusequestions(models.Model):
    products = models.ForeignKey(Levelofuse, db_column='Products_id')  # Field name made lowercase.
    uses = models.ForeignKey(Levelofuse, db_column='Uses_id')  # Field name made lowercase.
    levelofuse_value = models.ForeignKey(Levelofuse, db_column='levelofUse_value')  # Field name made lowercase.
    focalizationcategories = models.ForeignKey(Focalizationquestions, db_column='focalizationCategories_id')  # Field name made lowercase.
    focalizationquestions = models.ForeignKey(Focalizationquestions, db_column='focalizationQuestions_id')  # Field name made lowercase.
    importancelevel = models.FloatField(db_column='importanceLevel')  # Field name made lowercase.
    lastupdate = models.DateTimeField(db_column='lastUpdate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'levelofusequestions'
        unique_together = (('Products_id', 'Uses_id', 'levelofUse_value', 'focalizationCategories_id', 'focalizationQuestions_id'),)


class Models(models.Model):
    products = models.ForeignKey('Productbrands', db_column='Products_id')  # Field name made lowercase.
    brands = models.ForeignKey('Productbrands', db_column='Brands_id')  # Field name made lowercase.
    version = models.CharField(max_length=45)
    code = models.CharField(unique=True, max_length=45)
    creationdatetime = models.DateTimeField(db_column='creationDateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'models'


class Modelspecfeatures(models.Model):
    products = models.ForeignKey('Specfeatures', db_column='Products_id')  # Field name made lowercase.
    brands = models.ForeignKey(Models, db_column='Brands_id')  # Field name made lowercase.
    models = models.ForeignKey(Models, db_column='Models_id')  # Field name made lowercase.
    specfeatures = models.ForeignKey('Specfeatures', db_column='specFeatures_id')  # Field name made lowercase.
    specfeaturebrands = models.ForeignKey('Types', db_column='specFeatureBrands_id')  # Field name made lowercase.
    types = models.ForeignKey('Types', db_column='Types_id')  # Field name made lowercase.
    types_level = models.FloatField(db_column='Types_level')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'modelspecfeatures'
        unique_together = (('Products_id', 'Brands_id', 'Models_id', 'specFeatures_id', 'specFeatureBrands_id', 'Types_id'),)


class Productbrands(models.Model):
    products = models.ForeignKey('Products', db_column='Products_id')  # Field name made lowercase.
    brands = models.ForeignKey(Brands, db_column='Brands_id')  # Field name made lowercase.
    creationdatetime = models.DateTimeField(db_column='creationDateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productbrands'
        unique_together = (('Products_id', 'Brands_id'),)


class Productreviewers(models.Model):
    products = models.ForeignKey('Products', db_column='Products_id')  # Field name made lowercase.
    reviewers = models.ForeignKey('Reviewers', db_column='Reviewers_id')  # Field name made lowercase.
    creationdatetime = models.DateTimeField(db_column='creationDateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productreviewers'
        unique_together = (('Products_id', 'Reviewers_id'),)


class Products(models.Model):
    name = models.CharField(unique=True, max_length=45)
    creationdatetime = models.DateTimeField(db_column='creationDateTime')  # Field name made lowercase.
    image = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'


class Productvendors(models.Model):
    products = models.ForeignKey(Products, db_column='Products_id')  # Field name made lowercase.
    vendors = models.ForeignKey('Vendors', db_column='Vendors_id')  # Field name made lowercase.
    creationdatetime = models.DateTimeField(db_column='creationDateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'productvendors'
        unique_together = (('Products_id', 'Vendors_id'),)


class Registeredusers(models.Model):
    username = models.CharField(db_column='userName', unique=True, max_length=64)  # Field name made lowercase.
    email = models.CharField(unique=True, max_length=320)
    password = models.CharField(db_column='Password', unique=True, max_length=264)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'registeredusers'


class Reviewers(models.Model):
    name = models.CharField(unique=True, max_length=45)
    websiteurl = models.CharField(db_column='webSiteURL', max_length=2083)  # Field name made lowercase.
    creationdatetime = models.DateTimeField(db_column='creationDateTime')  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reviewers'


class Reviews(models.Model):
    products = models.ForeignKey(Models, db_column='Products_id')  # Field name made lowercase.
    brands = models.ForeignKey(Models, db_column='Brands_id')  # Field name made lowercase.
    models = models.ForeignKey(Models, db_column='Models_id')  # Field name made lowercase.
    reviewers = models.ForeignKey(Reviewers, db_column='Reviewers_id')  # Field name made lowercase.
    type = models.IntegerField()
    websiteurl = models.CharField(db_column='webSiteURL', max_length=2083)  # Field name made lowercase.
    creationdatetime = models.DateTimeField(db_column='creationDateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'reviews'


class Signins(models.Model):
    registeredusers = models.ForeignKey(Registeredusers, db_column='registeredUsers_id')  # Field name made lowercase.
    entrances = models.ForeignKey(Entrances, db_column='Entrances_id')  # Field name made lowercase.
    signindatetime = models.DateTimeField(db_column='SignInDateTime')  # Field name made lowercase.
    signoutdatetime = models.DateTimeField(db_column='SignOutDateTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'signins'
        unique_together = (('registeredUsers_id', 'Entrances_id', 'SignInDateTime'),)


class SocialaccountSocialaccount(models.Model):
    provider = models.CharField(max_length=30)
    uid = models.CharField(max_length=255)
    last_login = models.DateTimeField()
    date_joined = models.DateTimeField()
    extra_data = models.TextField()
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialaccount'
        unique_together = (('provider', 'uid'),)


class SocialaccountSocialapp(models.Model):
    provider = models.CharField(max_length=30)
    name = models.CharField(max_length=40)
    client_id = models.CharField(max_length=100)
    secret = models.CharField(max_length=100)
    key = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp'


class SocialaccountSocialappSites(models.Model):
    socialapp = models.ForeignKey(SocialaccountSocialapp)
    site = models.ForeignKey(DjangoSite)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialapp_sites'
        unique_together = (('socialapp_id', 'site_id'),)


class SocialaccountSocialtoken(models.Model):
    token = models.TextField()
    token_secret = models.TextField()
    expires_at = models.DateTimeField(blank=True, null=True)
    account = models.ForeignKey(SocialaccountSocialaccount)
    app = models.ForeignKey(SocialaccountSocialapp)

    class Meta:
        managed = False
        db_table = 'socialaccount_socialtoken'
        unique_together = (('app_id', 'account_id'),)


class Specfeaturebrands(models.Model):
    products = models.ForeignKey('Specfeatures', db_column='Products_id')  # Field name made lowercase.
    specfeatures = models.ForeignKey('Specfeatures', db_column='specFeatures_id')  # Field name made lowercase.
    name = models.CharField(unique=True, max_length=45)
    creationdatetime = models.DateTimeField(db_column='creationDateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'specfeaturebrands'


class Specfeatures(models.Model):
    products = models.ForeignKey(Products, db_column='Products_id')  # Field name made lowercase.
    name = models.CharField(unique=True, max_length=45)
    numoftypelevels = models.IntegerField(db_column='numOfTypeLevels')  # Field name made lowercase.
    compareable = models.IntegerField()
    description = models.TextField()
    lastupdate = models.DateTimeField(db_column='lastUpdate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'specfeatures'


class Types(models.Model):
    products = models.ForeignKey(Specfeaturebrands, db_column='Products_id')  # Field name made lowercase.
    specfeatures = models.ForeignKey(Specfeaturebrands, db_column='specFeatures_id')  # Field name made lowercase.
    specfeaturebrands = models.ForeignKey(Specfeaturebrands, db_column='specFeatureBrands_id')  # Field name made lowercase.
    version = models.CharField(max_length=45)
    code = models.CharField(unique=True, max_length=45)
    level = models.FloatField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'types'


class Uses(models.Model):
    products = models.ForeignKey(Products, db_column='Products_id')  # Field name made lowercase.
    name = models.CharField(max_length=45)
    image = models.TextField(blank=True, null=True)
    creationdatetime = models.DateTimeField(db_column='creationDateTime')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'uses'
        unique_together = (('Products_id', 'name'),)


class Usestofeatures(models.Model):
    products = models.ForeignKey(Specfeatures, db_column='Products_id')  # Field name made lowercase.
    uses = models.ForeignKey(Levelofuse, db_column='Uses_id')  # Field name made lowercase.
    levelofuse_value = models.ForeignKey(Levelofuse, db_column='levelofUse_value')  # Field name made lowercase.
    specfeatures = models.ForeignKey(Specfeatures, db_column='specFeatures_id')  # Field name made lowercase.
    minspeclevel = models.FloatField(db_column='minSpecLevel')  # Field name made lowercase.
    lastupdate = models.DateTimeField(db_column='lastUpdate')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'usestofeatures'
        unique_together = (('Products_id', 'Uses_id', 'levelofUse_value', 'specFeatures_id'),)


class Vendors(models.Model):
    name = models.CharField(unique=True, max_length=45)
    websiteurl = models.CharField(db_column='webSiteURL', max_length=2083, blank=True, null=True)  # Field name made lowercase.
    creationdatetime = models.DateTimeField(db_column='creationDateTime')  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vendors'
