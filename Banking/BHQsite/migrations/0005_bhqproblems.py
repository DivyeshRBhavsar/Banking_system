# Generated by Django 3.1.4 on 2021-03-16 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BHQsite', '0004_delete_bhq_problems'),
    ]

    operations = [
        migrations.CreateModel(
            name='bhqproblems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.CharField(max_length=20)),
                ('subject', models.CharField(max_length=20)),
                ('problem', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('empid', models.CharField(max_length=20)),
            ],
        ),
    ]
