# Generated by Django 5.1.2 on 2024-11-20 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dash_board', '0017_alter_contact_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'permissions': (('can_view_page', 'View Page'),)},
        ),
    ]