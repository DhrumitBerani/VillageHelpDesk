# Generated by Django 3.2.12 on 2023-09-19 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modules', '0019_auto_20230919_1145'),
    ]

    operations = [
        migrations.CreateModel(
            name='CastCertificate',
            fields=[
                ('form_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('inward_id', models.CharField(blank=True, max_length=50, null=True)),
                ('fullname', models.TextField()),
                ('gender', models.CharField(max_length=50)),
                ('parent_name', models.TextField()),
                ('religion', models.TextField()),
                ('cast', models.TextField()),
                ('subcast', models.TextField()),
                ('district', models.TextField()),
                ('taluka', models.TextField()),
                ('village', models.TextField()),
                ('leaving_certificate', models.FileField(blank=True, null=True, upload_to='uploads/castcertificate/')),
                ('family_lc_certificate', models.FileField(blank=True, null=True, upload_to='uploads/castcertificate/')),
                ('electricity_bill', models.FileField(blank=True, null=True, upload_to='uploads/castcertificate/')),
                ('approval_date', models.DateField(blank=True, null=True)),
                ('form_status', models.CharField(max_length=50)),
                ('application_date', models.DateTimeField(blank=True, null=True)),
                ('talati_id', models.IntegerField(blank=True, null=True)),
                ('user_villageId', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.RemoveField(
            model_name='birthcertificate',
            name='talati_username',
        ),
        migrations.AddField(
            model_name='birthcertificate',
            name='talati_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
