# Generated by Django 2.2 on 2019-10-14 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Время обновления'),
        ),
    ]
