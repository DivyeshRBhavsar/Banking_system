# Generated by Django 3.1.4 on 2021-03-17 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BMsite', '0007_bm_problems'),
    ]

    operations = [
        migrations.CreateModel(
            name='customers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Year', models.CharField(max_length=10)),
                ('bapunagar_customers', models.CharField(max_length=10)),
                ('bopal_customers', models.CharField(max_length=10)),
                ('chandkheda_customers', models.CharField(max_length=10)),
                ('gandhinagar_customers', models.CharField(max_length=10)),
                ('gota_customers', models.CharField(max_length=10)),
                ('isanpur_customers', models.CharField(max_length=10)),
                ('lal_darwaja_customers', models.CharField(max_length=10)),
                ('maninagar_customers', models.CharField(max_length=10)),
                ('vastral_customers', models.CharField(max_length=10)),
            ],
        ),
    ]