# Generated by Django 2.2 on 2019-10-30 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_usergithub'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergithub',
            name='github',
            field=models.URLField(blank=True, null=True, verbose_name='github'),
        ),
    ]
