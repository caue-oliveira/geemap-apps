import subprocess
from osgeo import gdal

pygdal_version = gdal.__version__
gdal_version = subprocess.check_output(['gdal-config','--version']).decode('utf-8').strip()

print(f'pygdal version: {pygdal_version}')
print(f'gdal version: {gdal_version}')

if pygdal_version == gdal_version:
    print('GDAL versions match')
else:
    print('GDAL versions do not match')