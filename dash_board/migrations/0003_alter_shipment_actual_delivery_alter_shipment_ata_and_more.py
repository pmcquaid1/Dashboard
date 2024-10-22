# Generated by Django 5.1.2 on 2024-10-22 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash_board', '0002_rename_actualdelivery_shipment_actual_delivery_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='actual_delivery',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='ata',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='cargo_available',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='consignee',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='date_cleared',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='forty_ft',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='shipment_id',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='twenty_ft',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='weight',
            field=models.IntegerField(),
        ),
    ]