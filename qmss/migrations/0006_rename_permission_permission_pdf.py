# Generated by Django 4.2 on 2023-05-01 04:38

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qmss', '0005_remove_pdffile_recipients_permission'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Permission',
            new_name='Permission_pdf',
        ),
    ]
