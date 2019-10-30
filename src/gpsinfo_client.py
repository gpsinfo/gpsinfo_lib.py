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

# INPUT_filenameXML = 'file:///home/rechenraum/Base/data/gpsinfo/20191024/gpsinfoWMTSCapabilities.xml'
# INPUT_layerTitle = 'AUSTRIA DGM 10x10m'

# INPUT_filenameXML = 'file:///home/simon/Base/data/gpsinfo/20191025/gpsinfoWMTSCapabilities.xml'
# INPUT_layerTitle = 'gpsinfo Test Layer'

INPUT_filenameXML = 'http://gpsinfo.org/service_wmts/gpsinfoWMTSCapabilities.xml'
INPUT_layerTitle = 'AT_OGD_DHM_LAMB_10M_ELEVATION_COMPRESSED'

################################################################################
#
# imports
#
################################################################################

import sys
import time
import xml.etree.ElementTree as xmlET
# sudo apt install python3-gdal
import gdal
import gpsinfo

################################################################################
#
# \brief Download/open tile via GDAL and returns its data as numpy array
#
# \param layerURLTemplate URL template as defined in the XML file
# \param tileRowIndex Row index of tile
# \param tileColIndex Column index of tile
#
# \return Numpy array storing the tile data
# 
################################################################################

def loadTileData(layerURLTempalte, tileRowIndex, tileColIndex) :
	# Build URL
	url = layerURLTemplate.replace('{TileCol}', str(tileColIndex)).replace('{TileRow}', str(tileRowIndex))
	# DEBUGGING ONLY (start)
	#url = url.replace('c/', '/home/rechenraum/Base/data/gpsinfo/20191024/')
	# DEBUGGING ONLY (end)
	print('Loading ' + url + ' ...')

	# GDAL's virtual file system: https://gdal.org/user/virtual_file_systems.html
	# GDAL and python: 
	#	- https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html
	#	- https://automating-gis-processes.github.io/2016/Lesson7-read-raster.html
	gdal_dataset = gdal.Open(url)
	if gdal_dataset is None:
		print('ERROR Failed to open ' + url + '.')
		sys.exit()
	
	# read data as numpy array
	array = gdal_dataset.ReadAsArray();
	
	# Close the dataset
	gdal_dataset = None
	
	return array

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

si = gpsinfo.ServiceInfo()
si.connect(INPUT_filenameXML)
for layer in si.layers():
    print('\t' + layer)
    
sys.exit()

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
for layerNode in xmlRoot.findall('wmts:Contents/wmts:Layer/ows:Title', xmlNamespace):
    print('\t' + layerNode.text)

sys.exit()

################################################################################
#
# collect information about requested layer
#
################################################################################

layerNode = xmlRoot.findall("./wmts:Contents/wmts:Layer[ows:Title='" + INPUT_layerTitle + "']", xmlNamespace)
if (len(layerNode) == 0) :
	print('ERROR Failed to find layer with title ' + INPUT_layerTitle + '.')
	sys.exit()
elif (len(layerNode) != 1) :
	print('ERROR Failed to find unique layer with title ' + INPUT_layerTitle + '.')
	sys.exit()

layerURLFormat = layerNode[0].find('wmts:ResourceURL', xmlNamespace).attrib['format']
layerURLTemplate = layerNode[0].find('wmts:ResourceURL', xmlNamespace).attrib['template']

tileMatrixSet = layerNode[0].find("wmts:TileMatrixSetLink/wmts:TileMatrixSet", xmlNamespace).text
tileMatrixSetNode = xmlRoot.find("./wmts:Contents/wmts:TileMatrixSet[ows:Identifier='" + tileMatrixSet + "']", xmlNamespace)

topLeftCorner = tileMatrixSetNode.find('wmts:TileMatrix/wmts:TopLeftCorner', xmlNamespace).text.split()
topLeftCornerX = float(topLeftCorner[0])
topLeftCornerY = float(topLeftCorner[1])
tileWidth = int(tileMatrixSetNode.find('wmts:TileMatrix/wmts:TileWidth', xmlNamespace).text)
tileHeight = int(tileMatrixSetNode.find('wmts:TileMatrix/wmts:TileHeight', xmlNamespace).text)
nrTilesX = int(tileMatrixSetNode.find('wmts:TileMatrix/wmts:MatrixWidth', xmlNamespace).text)
nrTilesY = int(tileMatrixSetNode.find('wmts:TileMatrix/wmts:MatrixHeight', xmlNamespace).text)
cellsize = float(tileMatrixSetNode.find('wmts:TileMatrix/wmts:ScaleDenominator', xmlNamespace).text) * 0.00028

################################################################################
#
# compute tile index for a specific query point
#
################################################################################

INPUT_qX = topLeftCornerX+100
INPUT_qY = topLeftCornerY-200

globalColIndex = int(round((INPUT_qX - topLeftCornerX) / cellsize));
globalRowIndex = int(round((topLeftCornerY - INPUT_qY) / cellsize));

if (globalColIndex < 0) | (globalRowIndex < 0) :
	print('ERROR Query point out of bounds.')
	sys.exit()

# The wanted value is in tile (tileRowIndex, tileColIndex) at 
# (localRowIndex, localColIndex)
tileColIndex, localColIndex = divmod(globalColIndex, tileWidth)
tileRowIndex, localRowIndex = divmod(globalRowIndex, tileHeight)

if (tileColIndex >= nrTilesX) | (tileRowIndex >= nrTilesY) :
	print('ERROR Query point out of bounds.')
	sys.exit()

# print(str(tileRowIndex) + ', ' + str(tileColIndex))
# print(str(localColIndex) + ', ' + str(localRowIndex))

data = loadTileData(layerURLTemplate, tileRowIndex, tileColIndex)
print(str(data[localRowIndex,localColIndex]))

sys.exit()



	
