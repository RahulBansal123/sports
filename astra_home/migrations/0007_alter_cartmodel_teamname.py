# Generated by Django 4.1.7 on 2023-03-05 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('astra_home', '0006_cartmodel_teamname_sportsmodel_regfee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartmodel',
            name='teamName',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]
