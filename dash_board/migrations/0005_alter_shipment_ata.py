# Generated by Django 5.1.2 on 2024-10-23 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash_board', '0004_alter_shipment_actual_delivery_alter_shipment_ata_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='ata',
            field=models.DateField(),
        ),
    ]
