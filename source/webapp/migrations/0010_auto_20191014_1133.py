# Generated by Django 2.2 on 2019-10-14 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0009_auto_20191014_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Время обновления'),
        ),
    ]
