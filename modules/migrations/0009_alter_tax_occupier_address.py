# Generated by Django 3.2.12 on 2023-09-10 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0008_tax'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tax',
            name='occupier_address',
            field=models.CharField(max_length=100),
        ),
    ]
