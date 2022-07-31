import urllib.request
import urllib.parse
import json

service_url = 'http://maps.googleapis.com/maps/api/geocode/json?'

while True:
    address = input('Enter location: ')
    url = service_url + urllib.parse.urlencode({'address': address})

    print('Retrieving', url)

    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters')

    try:
        js = json.loads(data)
    except:
        js = None

    if not js or 'status' not in js or js['status'] != 'OK':
        print('Failure')
        print(data)
        continue
    lat = js["results"][0]["geometry"]["location"]["lat"]
    lon = js["results"][0]["geometry"]["location"]["lng"]
    print('lat', lat, 'lon', lon)
    location = js['results'][0]['formatted_address']
    print(location)
