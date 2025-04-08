# Generated by Django 3.2.12 on 2023-09-09 07:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('modules', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='usertable',
            fields=[
                ('userid', models.AutoField(primary_key=True, serialize=False)),
                ('mobile_number', models.BigIntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('address', models.TextField()),
                ('village_id', models.IntegerField()),
                ('verification_code', models.IntegerField()),
                ('type', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
