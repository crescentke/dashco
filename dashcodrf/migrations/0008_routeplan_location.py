# Generated by Django 2.0.7 on 2018-07-24 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashcodrf', '0007_routeplan'),
    ]

    operations = [
        migrations.AddField(
            model_name='routeplan',
            name='location',
            field=models.CharField(default='Nairobi', max_length=128),
        ),
    ]
