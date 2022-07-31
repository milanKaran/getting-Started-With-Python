import urllib.request
import urllib.parse
import sqlite3
import json
import time
import ssl

api_key = False

if api_key is False:
    service_url = 'http://py4e-data.dr-chuck.net/geojson?'
else:
    service_url = 'http://maps.googleapis.com/maps/api/place/textsearch/json?'

conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

fh = open('where.data')
count = 0

for line in fh:
    if count > 200:
        print('Retrieved 200 locations, restart to retrieve more')
        break
    address = line.strip()
    print('')
    cur.execute('SELECT geodata FROM Locations WHERE address = ?', (memoryview(address.encode()),))

    try:
        data = cur.fetchone()[0]
        print('Found in database ', address)
        continue
    except:
        pass

    params = dict()
    params['query'] = address
    if api_key is not False:
        params['key'] = api_key
    url = service_url + urllib.parse.urlencode(params)

    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))
    count = count + 1

    try:
        js = json.loads(data)
    except:
        print(data)
        continue

    if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS'):
        print('Failure to retrieve')
        print(data)
        break

    cur.execute(
        'INSERT INTO Locations (address, geodata) values (?, ?)',
        (memoryview(address.encode()), memoryview(data.encode())))
    conn.commit()
    if count % 10 == 0:
        print('Pausing...')
        time.sleep(5)

print('Run geo_dump.py to tread the data from the database so you can visualize it on a map.')
