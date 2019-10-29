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

import sys
import time
import xml.etree.ElementTree as xmlET
import gdal

################################################################################
#
# class ServiceInfo
#
################################################################################

class ServiceInfo:
	
	# Constructor
	def __init__(self):
		pass
		
	# baseurl is URL to XML file
	def connect(self, baseurl):
		self.__m_baseurl = baseurl
		
		
	def baseurl(self):
		return self.__m_baseurl
		
	def layers(self):
		return m_layers
		
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
		pass
		
	def value(self, method, x, y, value):
		value = 4
		return ''
		
	def values(self, xLowerLeft, yLowerLeft, xUpperRight, yUpperRight, values):
		return ''
        
