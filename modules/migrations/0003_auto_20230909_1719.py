# Generated by Django 3.2.12 on 2023-09-09 11:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('modules', '0002_auto_20230909_1319'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('userid', models.AutoField(primary_key=True, serialize=False)),
                ('mobile_number', models.BigIntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('address', models.TextField()),
                ('village_id', models.IntegerField()),
                ('verification_code', models.IntegerField()),
                ('type', models.CharField(max_length=50)),
                ('signature', models.FileField(upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Collector',
        ),
        migrations.DeleteModel(
            name='Talati',
        ),
        migrations.DeleteModel(
            name='usertable',
        ),
    ]
