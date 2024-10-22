# Generated by Django 5.1.2 on 2024-10-22 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash_board', '0003_alter_shipment_actual_delivery_alter_shipment_ata_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='actual_delivery',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='ata',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='cargo_available',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='date_cleared',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='forty_ft',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='twenty_ft',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='weight',
            field=models.CharField(max_length=25),
        ),
    ]