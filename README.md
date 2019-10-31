# gpsinfo_lib.py

GPL3-license reference implementation of gpsinfo client library API in Python. 
Visit http://www.gpsinfo.org for more information.

## Example - Query Elevation Data

The following example illustrates how you may query elevation data at given 
coordinates with four lines of Python code.

```python
import gpsinfo
service = gpsinfo.Service('http://gpsinfo.org/service_wmts/gpsinfoWMTSCapabilities.xml')
layer = gpsinfo.Layer(service, 'AT_OGD_DHM_LAMB_10M_ELEVATION_COMPRESSED')
print('Elevation = ' + str(layer.value('nearest', 675392, 432848)))
```
