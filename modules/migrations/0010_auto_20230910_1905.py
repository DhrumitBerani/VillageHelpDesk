# Generated by Django 3.2.12 on 2023-09-10 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0009_alter_tax_occupier_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tax',
            name='payer_username',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='tax',
            name='payment_date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
