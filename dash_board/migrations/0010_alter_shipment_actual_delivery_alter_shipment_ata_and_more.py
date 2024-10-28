# Generated by Django 5.1.2 on 2024-10-27 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash_board', '0009_alter_shipment_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='actual_delivery',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='ata',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='cargo_available',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='consignee',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='cont',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='date_cleared',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='forty_ft',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='shipment_id',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='twenty_ft',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='uw',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='weight',
            field=models.CharField(max_length=50),
        ),
    ]