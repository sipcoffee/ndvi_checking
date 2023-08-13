from django.db import models

class FileUpload(models.Model):
    nameRaster = models.CharField(max_length=100, null=True)
    rasterImage = models.FileField(upload_to='raster_files', null=True, blank=True)
    fileEdited =  models.FileField(upload_to='edited_file', null=True, blank=True)
