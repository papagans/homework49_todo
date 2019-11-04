# Generated by Django 2.2 on 2019-11-04 09:18

from django.db import migrations


def create_profiles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('accounts', 'Profile')
    for user in User.objects.all():
        Profile.objects.get_or_create(user=user)


def delete_profiles(apps, schema_editor):
    Profile = apps.get_model('accounts', 'Profile')
    Profile.objects.all.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20191104_0855'),
    ]

    operations = [
        migrations.RunPython(create_profiles, delete_profiles)
    ]
