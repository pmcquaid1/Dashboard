# Generated by Django 5.1.2 on 2024-11-26 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dash_board', '0020_transport'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transport',
            name='first_pickup_instructions',
        ),
        migrations.RemoveField(
            model_name='transport',
            name='first_pu_pkg_cont_id',
        ),
        migrations.RemoveField(
            model_name='transport',
            name='first_pu_pkg_qty',
        ),
        migrations.RemoveField(
            model_name='transport',
            name='first_pu_pkg_type',
        ),
    ]
