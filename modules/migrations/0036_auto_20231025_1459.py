# Generated by Django 3.2.12 on 2023-10-25 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0035_auto_20231023_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='birthcertificate',
            name='district',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='birthcertificate',
            name='taluka',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='birthcertificate',
            name='village',
            field=models.TextField(blank=True, null=True),
        ),
    ]
