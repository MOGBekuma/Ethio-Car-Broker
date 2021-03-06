# Generated by Django 4.0.5 on 2022-07-15 06:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default='', max_length=100)),
                ('city', models.CharField(default='', max_length=100)),
                ('phone', models.IntegerField(default=0)),
                ('type', models.CharField(default='client', max_length=20)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicleId', models.CharField(max_length=20)),
                ('make', models.CharField(max_length=40)),
                ('shortModel', models.CharField(max_length=35)),
                ('longModel', models.TextField()),
                ('trim', models.CharField(max_length=35)),
                ('derivative', models.CharField(max_length=35)),
                ('yearIntroduced', models.CharField(max_length=5)),
                ('yearDiscontinued', models.CharField(max_length=5, null=True)),
                ('currentlyAvailable', models.CharField(default='Y', max_length=10)),
                ('model_pic', models.ImageField(default='default.jpeg', upload_to='media')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
