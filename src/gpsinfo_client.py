"""

(c) 2019 Rechenraum GmbH (office@rechenraum.com)

This file is part of gpsinfo (www.gpsinfo.org).

gpsinfo is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

gpsinfo is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with gpsinfo. If not, see <http://www.gnu.org/licenses/>.
           

"""

################################################################################
#
# Constants
#
################################################################################

INPUT_filenameXML = '/home/rechenraum/Base/data/gpsinfo/20191024/gpsinfoWMTSCapabilities.xml'
INPUT_layerTitle = 'AUSTRIA DGM 10x10m'

################################################################################
#
# imports
#
################################################################################

import time
import xml.etree.ElementTree as xmlET
import gdal

################################################################################
#
# main
#
################################################################################

print('')
print('================================================================================')
print('gpsinfo_client (https://www.gpsinfo.org)')
print('')
print('(c) 2019 Rechenraum GmbH (office@rechenraum.com).')
print('================================================================================')
print('')

################################################################################
#
# parse XML file
#
################################################################################

# https://docs.python.org/3/library/xml.etree.elementtree.html
xmlNamespace = {
	'wmts' : 'http://www.opengis.net/wmts/1.0',
	'ows' : 'http://www.opengis.net/ows/1.1'
}
xmlRoot = xmlET.parse(INPUT_filenameXML).getroot()

print('Available layers:')
for layerNode in xmlRoot.findall('./wmts:Contents/wmts:Layer/ows:Title', xmlNamespace):
    print('\t' + layerNode.text)

################################################################################
#
# collect information about requested layer
#
################################################################################

layerNode = xmlRoot.findall("./wmts:Contents/wmts:Layer[ows:Title='" + INPUT_layerTitle + "']", xmlNamespace)
if (len(layerNode) == 0) :
	print('ERROR Failed to find layer with title ' + INPUT_layerTitle + '.')
	exit
elif (len(layerNode) != 1) :
	print('ERROR Failed to find unique layer with title ' + INPUT_layerTitle + '.')
	exit

layerURLFormat = layerNode[0].find('wmts:ResourceURL', xmlNamespace).attrib['format']
layerURLTemplate = layerNode[0].find('wmts:ResourceURL', xmlNamespace).attrib['template']

tileMatrixSet = layerNode[0].find("wmts:TileMatrixSetLink/wmts:TileMatrixSet", xmlNamespace).text
tileMatrixSetNode = xmlRoot.find("./wmts:Contents/wmts:TileMatrixSet[ows:Identifier='" + tileMatrixSet + "']", xmlNamespace)

################################################################################
#
# download tiles
#
################################################################################

# GDAL's virtual file system: https://gdal.org/user/virtual_file_systems.html
# GDAL and python: https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html
for row in range(0,2) :
	for col in range(0,3) :
		url = layerURLTemplate.replace('{TileCol}', str(col)).replace('{TileRow}', str(row))
		# DEBUGGING ONLY (start)
		url = url.replace('c/', '/home/rechenraum/Base/data/gpsinfo/20191024/')
		# DEBUGGING ONLY (end)
		print('Loading ' + url + ' ...')
		gdal_dataset = gdal.Open(url)
		if gdal_dataset is None:
			print('ERROR Failed to open ' + url + '.')
			exit
		
		print(gdal_dataset.GetGeoTransform())
		
		print (str(gdal_dataset.RasterXSize) + ' x ' + str(gdal_dataset.RasterYSize))
		
		gdal_rasterband = gdal_dataset.GetRasterBand(1)
		
		# Close the dataset
		gdal_dataset = None
