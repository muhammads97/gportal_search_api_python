# gportal_search_api_python
this is used to query the gportal for sgli data using latitude and longitude
## token 
get the token from the fuel_csrf_token header (inspect, network tab) 

## search params 
### cloud
not working at the moment

### date format
"%Y/%m/%d"

### coordinates
lat, long (array[2], pair, etc)
 
### identifier
product id (string)

### count
results max size

### path_number 
satellite path number (identifies the image location)

### scene_number
identifies a specific scene on the path

### resolution
250 or 1000
