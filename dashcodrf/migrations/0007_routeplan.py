# Generated by Django 2.0.7 on 2018-07-24 08:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashcodrf', '0006_remove_client_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoutePlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=55)),
                ('visit_date', models.DateField()),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default=True)),
                ('slug', models.SlugField(max_length=128)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]