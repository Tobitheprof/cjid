# Generated by Django 5.0 on 2023-12-18 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_document_extracted_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
