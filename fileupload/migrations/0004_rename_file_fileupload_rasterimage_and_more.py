# Generated by Django 4.2.1 on 2023-08-13 08:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fileupload", "0003_fileupload_fileedited"),
    ]

    operations = [
        migrations.RenameField(
            model_name="fileupload",
            old_name="file",
            new_name="rasterImage",
        ),
        migrations.AddField(
            model_name="fileupload",
            name="nameRaster",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
