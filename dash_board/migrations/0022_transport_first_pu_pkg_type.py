# Generated by Django 5.1.2 on 2024-11-26 15:30

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash_board', '0021_remove_transport_first_pickup_instructions_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transport',
            name='first_pu_pkg_type',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]
