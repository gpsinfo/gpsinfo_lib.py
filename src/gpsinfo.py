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
# imports
#
################################################################################

import xml.etree.ElementTree as xmlET
import sys

# We support python3 only
assert sys.version_info < (3, 0)

################################################################################
#
# class ServiceInfo
#
################################################################################

class ServiceInfo:
	
	# Constructor
	def __init__(self):
		self.__xmlNamespace = {
			'wmts' : 'http://www.opengis.net/wmts/1.0',
			'ows' : 'http://www.opengis.net/ows/1.1'
		}

	# baseurl is URL to XML file
	def connect(self, baseurl):
		
		self.__baseurl = baseurl
		
		# Parse XML file
		#
		# See https://docs.python.org/3/library/xml.etree.elementtree.html
		self.__xmlRoot = xmlET.parse(baseurl).getroot()
		
		# Get layers
		self.__layers = []
		for layerNode in self.__xmlRoot.findall('wmts:Contents/wmts:Layer/ows:Title', self.__xmlNamespace):
			self.__layers.append(layerNode.text)
		
	def baseurl(self):
		return self.__baseurl
		
	def layers(self):
		return self.__layers
		
	def xmlRoot(self):
		return self.__xmlRoot
		
	def xmlNamespace(self):
		return self.__xmlNamespace
		
################################################################################
#
# class LayerInfo
#
################################################################################

class LayerInfo:
	
	# Constructor
	def __init__(self):
		pass
		
	def connect(self, serviceInfo, layerName):
		layerNode = serviceInfo.xmlRoot().findall("./wmts:Contents/wmts:Layer[ows:Title='" + layerName + "']", serviceInfo.xmlNamespace())
		
	def value(self, method, x, y, value):
		value = 4
		return ''
		
	def values(self, xLowerLeft, yLowerLeft, xUpperRight, yUpperRight, values):
		return ''
        
