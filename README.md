# gpsinfo_lib.py

GPL3-licensed reference implementation of gpsinfo client library API in Python 3. 
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

## Quick Start

Clone the repository (or simply download gpsinfo.py and gpsinfo_test.py) and
run 

```bash
python3 gpsinfo_test.py
```
