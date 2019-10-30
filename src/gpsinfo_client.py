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
# INPUT_layerName = 'AUSTRIA DGM 10x10m'

# INPUT_filenameXML = 'file:///home/simon/Base/data/gpsinfo/20191025/gpsinfoWMTSCapabilities.xml'
# INPUT_layerName = 'gpsinfo Test Layer'

INPUT_filenameXML = 'http://gpsinfo.org/service_wmts/gpsinfoWMTSCapabilities.xml'
INPUT_layerName = 'AT_OGD_DHM_LAMB_10M_ELEVATION_COMPRESSED'

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

print('Connecting to ' + INPUT_filenameXML + ' ...')
gpsinfo_service = gpsinfo.Service()
gpsinfo_service.connect(INPUT_filenameXML)
print('Available layers: ')
for layer in gpsinfo_service.layers():
    print('\t' + layer)
print('')

gpsinfo_layer = gpsinfo.Layer()
error = gpsinfo_layer.connect(gpsinfo_service, INPUT_layerName)
if isinstance(error, str) : 
	print(error)
	sys.exit()

# height = gpsinfo_layer.value('undefined', 152803.0, 258808.0)
height = gpsinfo_layer.value('undefined', 675392, 432848)
# height = gpsinfo_layer.value('undefined', 125250, 371779)
if isinstance(height, str) :
	print(height)
	sys.exit()
	
print('Elevation = ' + str(height))
print('')

# as short as it gets without any error handling
service = gpsinfo.Service();
service.connect('http://gpsinfo.org/service_wmts/gpsinfoWMTSCapabilities.xml')
layer = gpsinfo.Layer()
layer.connect(service, 'AT_OGD_DHM_LAMB_10M_ELEVATION_COMPRESSED')
print('Elevation = ' + str(layer.value('undefined', 675392, 432848)))
print('')

    
