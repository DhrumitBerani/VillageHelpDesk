# Generated by Django 3.2.12 on 2023-10-18 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0032_incomecertificate_rupee_in_words'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='charactercertificate',
            name='birthdate',
        ),
        migrations.AddField(
            model_name='charactercertificate',
            name='years',
            field=models.TextField(blank=True, null=True),
        ),
    ]
