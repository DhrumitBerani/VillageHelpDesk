# Generated by Django 3.2.12 on 2023-11-04 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0036_auto_20231025_1459'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='birthcertificate',
            name='district',
        ),
        migrations.RemoveField(
            model_name='birthcertificate',
            name='taluka',
        ),
        migrations.RemoveField(
            model_name='birthcertificate',
            name='village',
        ),
    ]
