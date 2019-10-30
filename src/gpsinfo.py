"""

(c) 2019 Rechenraum GmbH (office@rechenraum.com)

This file is part of gpsinfo (www.gpsinfo.org).

gpsinfo is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

gpsinfo is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with gpsinfo. If not, see <http://www.gnu.org/licenses/>.
           

"""

################################################################################
#
# imports
#
################################################################################

import xml.etree.ElementTree as xmlET
import sys
import urllib.request
# sudo apt install python3-gdal
import gdal

# We support python3 only
assert sys.version_info > (3, 0)

################################################################################
#
# class ServiceInfo
#
################################################################################

class Service:
	
	#---------------------------------------------------------------------------
	
	# Constructor
	def __init__(self):
		self.__isConnected = False
		self.__xmlNamespace = {
			'wmts' : 'http://www.opengis.net/wmts/1.0',
			'ows' : 'http://www.opengis.net/ows/1.1'
		}
	
	#---------------------------------------------------------------------------
		
	# \brief Checks is a connection could be established successfully
	#
	# This basically means the class was successfully initialized
	#
	# \return True, if connection was successful, false otherwise.
	def isConnected(self):
		return self.__isConnected

	#---------------------------------------------------------------------------

	# \brief Establish connection to a gpsinfo service
	#
	# A successful call to this method is mandatory.
	#
	# \param baseurl Full URL to XML file. For local files, prefix with file://
	#
	# \return String in case of error, nothing in case of success
	def connect(self, baseurl):
		
		self.__isConnected = False
		self.__baseurl = baseurl
		
		# Download XML file
		#	https://stackoverflow.com/a/7244263
		# For local files, use a "file://" prefix, see
		#	https://stackoverflow.com/a/20558624
		try:
			xml = urllib.request.urlopen(baseurl).read().decode('utf-8')		
		except: 
			return "ERROR: Failed to download service XML file from '" + baseurl + "'."
				
		# Parse XML file
		#
		# See https://docs.python.org/3/library/xml.etree.elementtree.html
		#	xmlET.parse(baseurl).getroot()
		# would open a file.
		self.__xmlRoot = xmlET.fromstring(xml)
		
		# Get layers
		self.__layers = []
		for layerNode in self.__xmlRoot.findall('wmts:Contents/wmts:Layer/ows:Title', self.__xmlNamespace):
			self.__layers.append(layerNode.text)
			
		self.__isConnected = True
		
	#---------------------------------------------------------------------------
	
	# \brief Getter for baseurl property
	#
	# \return baseurl of connected service, e.g. URL of XML file
	def baseurl(self):
		if not self.isConnected() : return 'ERROR: You need to successfully connect to a service first.'
		return self.__baseurl
		
	#---------------------------------------------------------------------------
		
	# \brief Get layers of connected service
	#
	# \return String list of layers of connected service
	def layers(self):
		if not self.isConnected() : return 'ERROR: You need to successfully connect to a service first.'
		return self.__layers
		
	#---------------------------------------------------------------------------
			
	# \brief Getter for root of XML element tree of the service's XML file
	#
	# \return Root of XML element tree of the service's XML file
	def xmlRoot(self):
		if not self.isConnected() : return 'ERROR: You need to successfully connect to a service first.'
		return self.__xmlRoot
		
	#---------------------------------------------------------------------------
			
	# \brief Getter for XML namespace
	#
	# \return XML namespace
	def xmlNamespace(self):
		if not self.isConnected() : return 'ERROR: You need to successfully connect to a service first.'
		return self.__xmlNamespace
		
	#---------------------------------------------------------------------------
		
################################################################################
#
# class LayerInfo
#
################################################################################

class Layer:
	
	#---------------------------------------------------------------------------
	
	# Constructor
	def __init__(self):
		self.__isConnected = False
		
	#---------------------------------------------------------------------------
		
	# \brief Checks is a connection could be established successfully
	#
	# This basically means the class was successfully initialized
	#
	# \return True, if connection was successful, false otherwise.
	def isConnected(self):
		return self.__isConnected

	#---------------------------------------------------------------------------
		
	def connect(self, service, layerName):
		self.__isConnected = False
		if not service.isConnected() : 
			return 'ERROR: You need to pass a successfully connected service.'
			
		layerNode = service.xmlRoot().findall("./wmts:Contents/wmts:Layer[ows:Title='" + layerName + "']", service.xmlNamespace())
		if (len(layerNode) == 0) :
			return 'ERROR Failed to find layer with title ' + layerName + '.'
		elif (len(layerNode) != 1) :
			return 'ERROR Failed to find unique layer with title ' + layerName + '.'
		
		self.__layerInfo = { }
		self.__layerInfo['URLFormat'] = layerNode[0].find('wmts:ResourceURL', service.xmlNamespace()).attrib['format']
		self.__layerInfo['URLTemplate'] = layerNode[0].find('wmts:ResourceURL', service.xmlNamespace()).attrib['template']
		
		tileMatrixSet = layerNode[0].find("wmts:TileMatrixSetLink/wmts:TileMatrixSet", service.xmlNamespace()).text
		tileMatrixSetNode = service.xmlRoot().find("./wmts:Contents/wmts:TileMatrixSet[ows:Identifier='" + tileMatrixSet + "']", service.xmlNamespace())
		
		topLeftCorner = tileMatrixSetNode.find('wmts:TileMatrix/wmts:TopLeftCorner', service.xmlNamespace()).text.split()
		self.__layerInfo['topLeftCornerX'] = float(topLeftCorner[0])
		self.__layerInfo['topLeftCornerY'] = float(topLeftCorner[1])
		self.__layerInfo['tileWidth'] = int(tileMatrixSetNode.find('wmts:TileMatrix/wmts:TileWidth', service.xmlNamespace()).text)
		self.__layerInfo['tileHeight'] = int(tileMatrixSetNode.find('wmts:TileMatrix/wmts:TileHeight', service.xmlNamespace()).text)
		self.__layerInfo['nrTilesX'] = int(tileMatrixSetNode.find('wmts:TileMatrix/wmts:MatrixWidth', service.xmlNamespace()).text)
		self.__layerInfo['nrTilesY'] = int(tileMatrixSetNode.find('wmts:TileMatrix/wmts:MatrixHeight', service.xmlNamespace()).text)
		self.__layerInfo['cellsize'] = float(tileMatrixSetNode.find('wmts:TileMatrix/wmts:ScaleDenominator', service.xmlNamespace()).text) * 0.00028
				
		self.__isConnected = True
	
	#---------------------------------------------------------------------------
	
	def __loadTileData(self, tileRowIndex, tileColIndex) :
		# Build URL
		url = self.__layerInfo['URLTemplate'].replace('{TileCol}', str(tileColIndex)).replace('{TileRow}', str(tileRowIndex))
		
		# GDAL's virtual file system: 
		#	https://gdal.org/user/virtual_file_systems.html
		if not url.startswith('file://') : 
			url = '/vsicurl/' + url
		else :
			# We must strip the 'file://' prefix for gdal.Open
			url = url[7:]
		if self.__layerInfo['URLFormat'] == 'application/zip' :
			url = '/vsizip/' + url
		
		# print('Loading ' + url + ' ...')
		
		# GDAL and python: 
		#	- https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html
		#	- https://automating-gis-processes.github.io/2016/Lesson7-read-raster.html
		gdal_dataset = gdal.Open(url)
		if gdal_dataset is None:
			return 'ERROR Failed to open ' + url + '.'
					
		# read data as numpy array
		array = gdal_dataset.ReadAsArray()
		
		# Close the dataset
		gdal_dataset = None
		
		return array
	
	#---------------------------------------------------------------------------
	
	def __convertCoords2Idx(self, method, coordsX, coordsY) :
		globalColIndex = int(round((coordsX - self.__layerInfo['topLeftCornerX']) / self.__layerInfo['cellsize']))
		globalRowIndex = int(round((self.__layerInfo['topLeftCornerY'] - coordsY) / self.__layerInfo['cellsize']))

		if (globalColIndex < 0) | (globalRowIndex < 0) :
			return 'ERROR: Query point out of bounds.'
		
		# The wanted value is in tile (tileRowIndex, tileColIndex) at 
		# (localRowIndex, localColIndex)
		tileColIndex, localColIndex = divmod(globalColIndex, self.__layerInfo['tileWidth'])
		tileRowIndex, localRowIndex = divmod(globalRowIndex, self.__layerInfo['tileHeight'])

		if (tileColIndex >= self.__layerInfo['nrTilesX']) | (tileRowIndex >= self.__layerInfo['nrTilesY']) :
			return 'ERROR: Query point out of bounds.'
		
		return { 
			'tileRowIndex' : tileRowIndex, 
			'tileColIndex' : tileColIndex, 
			'localRowIndex' : localRowIndex,
			'localColIndex' : localColIndex
		}

	#---------------------------------------------------------------------------
		
	def value(self, method, x, y) :
		if not self.isConnected() : return 'ERROR: You need to successfully connect a layer first.'
		
		inds = self.__convertCoords2Idx(method, x,y)
		if isinstance(inds, str) : return inds
		if not isinstance(inds, dict) : return 'Error: Unexpected conversion result.'
				
		data = self.__loadTileData(inds['tileRowIndex'], inds['tileColIndex'])
		if isinstance(data, str) : return data
		
		return data[inds['localRowIndex'],inds['localColIndex']]
			
	#---------------------------------------------------------------------------
		
	def values(self, xLowerLeft, yLowerLeft, xUpperRight, yUpperRight):
		if not self.isConnected() : return 'ERROR: You need to successfully connect a layer first.'
		return 'ERROR: not implemented yet'
        
	#---------------------------------------------------------------------------
