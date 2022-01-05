from django.db import models


class Branch_Sheet(models.Model):
    Acct_branch = models.CharField(max_length=50)
    Branch_number =models.CharField(max_length=25)

    Transaction_code = models.CharField(max_length=5)
    Transaction_code_desc = models.CharField(max_length=30)
    Post_date = models.CharField(max_length=20)

    Amount = models.IntegerField()
    Debit_credit = models.CharField(max_length=3)


class bhq_problems(models.Model):
    empid = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    branch = models.CharField(max_length=20)
    subject = models.CharField(max_length=20)
    problem = models.CharField(max_length=300)


class deposits(models.Model):
    Year = models.CharField(max_length=10)
    Bapunagar_Deposits = models.CharField(max_length=10)
    Bopal_Deposits = models.CharField(max_length=10)
    Chandkheda_Deposits = models.CharField(max_length=10)
    Gandhinagar_Deposits = models.CharField(max_length=10)
    Gota_Deposits = models.CharField(max_length=10)
    Isanpur_Deposits = models.CharField(max_length=10)
    Lal_Darwaja_Deposits = models.CharField(max_length=10)
    Maninagar_Deposits = models.CharField(max_length=10)
    Vastral_Deposits = models.CharField(max_length=10)












