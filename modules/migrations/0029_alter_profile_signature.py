# Generated by Django 3.2.12 on 2023-10-11 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0028_complaints_talati_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='signature',
            field=models.FileField(blank=True, null=True, upload_to='uploads/birthcertificate/'),
        ),
    ]
