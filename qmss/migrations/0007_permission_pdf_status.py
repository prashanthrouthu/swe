# Generated by Django 4.2 on 2023-05-01 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qmss', '0006_rename_permission_permission_pdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission_pdf',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
