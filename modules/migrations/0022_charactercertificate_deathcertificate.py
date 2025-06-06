# Generated by Django 3.2.12 on 2023-09-19 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0021_alter_birthcertificate_weight'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharacterCertificate',
            fields=[
                ('form_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('inward_id', models.CharField(blank=True, max_length=50, null=True)),
                ('fullname', models.TextField()),
                ('gender', models.CharField(max_length=50)),
                ('parent_name', models.TextField()),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('religion', models.TextField()),
                ('district', models.TextField()),
                ('taluka', models.TextField()),
                ('village', models.TextField()),
                ('photo', models.FileField(blank=True, null=True, upload_to='uploads/charactercertificate/')),
                ('approval_date', models.DateField(blank=True, null=True)),
                ('form_status', models.CharField(max_length=50)),
                ('application_date', models.DateTimeField(blank=True, null=True)),
                ('talati_id', models.IntegerField(blank=True, null=True)),
                ('user_villageId', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DeathCertificate',
            fields=[
                ('form_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('inward_id', models.CharField(blank=True, max_length=50, null=True)),
                ('fullname', models.TextField()),
                ('gender', models.CharField(max_length=50)),
                ('father_name', models.TextField()),
                ('mother_name', models.TextField()),
                ('address_of_deceased', models.TextField()),
                ('place_of_death', models.TextField()),
                ('remarks', models.TextField()),
                ('deathdate', models.DateField(blank=True, null=True)),
                ('registrationdate', models.DateField(blank=True, null=True)),
                ('approval_date', models.DateField(blank=True, null=True)),
                ('id_proof', models.FileField(blank=True, null=True, upload_to='uploads/deathcertificate/')),
                ('form_status', models.CharField(max_length=50)),
                ('application_date', models.DateTimeField(blank=True, null=True)),
                ('talati_id', models.IntegerField(blank=True, null=True)),
                ('user_villageId', models.IntegerField()),
            ],
        ),
    ]
