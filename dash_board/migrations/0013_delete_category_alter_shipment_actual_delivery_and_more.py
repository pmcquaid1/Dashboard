# Generated by Django 5.1.2 on 2024-11-05 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dash_board', '0012_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Category',
        ),
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
            name='date_cleared',
            field=models.DateField(),
        ),
    ]