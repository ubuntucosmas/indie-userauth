# Generated by Django 5.0.7 on 2024-09-13 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_fileupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='infor_graphic',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
