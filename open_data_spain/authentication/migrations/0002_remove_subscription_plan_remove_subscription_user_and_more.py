# Generated by Django 4.2.8 on 2023-12-11 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='plan',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='user',
        ),
        migrations.DeleteModel(
            name='Plan',
        ),
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]
