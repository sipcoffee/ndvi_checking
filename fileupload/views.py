from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import FileSerializer
import rasterio
import json
import os
from django.core.files.uploadedfile import TemporaryUploadedFile
from io import BytesIO
import numpy as np


@api_view(['POST'])
def upload(request):
    if 'rasterImage' in request.FILES:
        rasterImg = request.FILES['rasterImage']
        rasterName = request.data['nameRaster']

        file_extension = os.path.splitext(rasterImg.name)[1]
        if file_extension.lower() != '.tif':
            return Response({'error': 'Invalid file format. Only TIFF files are accepted.'}, status=400)

        try:
            raster_io = BytesIO(rasterImg.read())

            # Open the raster using rasterio from the BytesIO object
            dataset = rasterio.open(raster_io)

            bands = dataset.read()

            # Calculate false NDVI
            red_band = bands[2]  # Red band
            green_band = bands[1]  # Green band
            blue_band = bands[0]

            #threshold = 0.001

            #vari_denom = green_band + red_band - blue_band
            #vari_denom = np.where(vari_denom < threshold, threshold, vari_denom)

            vari = (green_band - red_band) / (green_band + red_band - blue_band)
            
            # Clip the vari values to be within the range of -1 to 1
            vari = np.clip(vari, -1, 1)

            print('vari val: ', vari)

            new_tiff_path = f'media/edited_file/{rasterName}_vari.tif'

            os.makedirs(os.path.dirname(new_tiff_path), exist_ok=True)
            original_crs = dataset.crs

            transform = dataset.transform

            with rasterio.open(new_tiff_path, 'w', driver='GTiff', width=bands.shape[2], height=bands.shape[1],
                               count=1, dtype=vari.dtype, crs=original_crs, transform=transform) as dst:
                dst.write(vari, 1)

            print("done converting")
            serializer = FileSerializer(data={
                'nameRaster': rasterName,
                'rasterImage': request.FILES['rasterImage'],
                'fileEdited': new_tiff_path,
            })

            if serializer.is_valid():
                serializer.save()
                print("SAVE")
                response_data = {
                    'msg': 'success',
                    'data': serializer.data
                }
                print("RS DATA: ", response_data)
                return Response(response_data, status=201)
            return Response(serializer.errors, status=400)

        except Exception as e:
            print(e)
            return Response({'error': 'Failed to process the raster file.'}, status=400)
    
    return Response({'error': 'Failed to process the raster file.'}, status=400)