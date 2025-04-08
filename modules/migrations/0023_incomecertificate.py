# Generated by Django 3.2.12 on 2023-09-23 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0022_charactercertificate_deathcertificate'),
    ]

    operations = [
        migrations.CreateModel(
            name='IncomeCertificate',
            fields=[
                ('form_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('inward_id', models.CharField(blank=True, max_length=50, null=True)),
                ('fullname', models.TextField()),
                ('gender', models.CharField(max_length=50)),
                ('parent_name', models.TextField()),
                ('applicant_income', models.BigIntegerField()),
                ('parent_income', models.BigIntegerField()),
                ('other_income', models.BigIntegerField()),
                ('district', models.TextField()),
                ('taluka', models.TextField()),
                ('village', models.TextField()),
                ('photo', models.FileField(blank=True, null=True, upload_to='uploads/incomecertificate/')),
                ('ration_card', models.FileField(blank=True, null=True, upload_to='uploads/incomecertificate/')),
                ('electricity_bill', models.FileField(blank=True, null=True, upload_to='uploads/incomecertificate/')),
                ('adhar_card', models.FileField(blank=True, null=True, upload_to='uploads/incomecertificate/')),
                ('approval_date', models.DateField(blank=True, null=True)),
                ('id_proof', models.FileField(blank=True, null=True, upload_to='uploads/deathcertificate/')),
                ('form_status', models.CharField(max_length=50)),
                ('application_date', models.DateTimeField(blank=True, null=True)),
                ('talati_id', models.IntegerField(blank=True, null=True)),
                ('user_villageId', models.IntegerField()),
            ],
        ),
    ]
