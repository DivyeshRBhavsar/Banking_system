from django.db import models

class bm_problems(models.Model):
    empid = models.CharField(max_length=20)
    branch = models.CharField(max_length=30)
    subject = models.CharField(max_length=20)
    request = models.CharField(max_length=200)

class customers(models.Model):
    Year = models.CharField(max_length=10)
    bapunagar_customers = models.CharField(max_length=10)
    bopal_customers = models.CharField(max_length=10)
    chandkheda_customers = models.CharField(max_length=10)
    gandhinagar_customers = models.CharField(max_length=10)
    gota_customers = models.CharField(max_length=10)
    isanpur_customers = models.CharField(max_length=10)
    lal_darwaja_customers = models.CharField(max_length=10)
    maninagar_customers = models.CharField(max_length=10)
    vastral_customers = models.CharField(max_length=10)


class loans(models.Model):
    Year = models.CharField(max_length=10)
    bapunagar_loans = models.CharField(max_length=10)
    bopal_loans = models.CharField(max_length=10)
    chandkheda_loans = models.CharField(max_length=10)
    gandhinagar_loans = models.CharField(max_length=10)
    gota_loans = models.CharField(max_length=10)
    isanpur_loans = models.CharField(max_length=10)
    lal_darwaja_loans = models.CharField(max_length=10)
    maninagar_loans = models.CharField(max_length=10)
    vastral_loans = models.CharField(max_length=10)



