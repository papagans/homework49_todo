# Generated by Django 2.2 on 2019-11-06 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0012_auto_20191106_0726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='teams', to='webapp.Project', verbose_name='Проект'),
        ),
    ]
