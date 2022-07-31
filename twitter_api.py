import urllib.request
import urllib.parse
import twurl
import json

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

while True:
    print('')
    acct = input('Enter Twitter Account:')
    if len(acct) < 1:
        break
    url = twurl.augment(TWITTER_URL, {'screen name': acct, 'count': '5'})

    print('Retrieving', url)
    connection = urllib.request.urlopen(url)

    data = connection.read().decode()
    header = dict(connection.getheaders())
    print('remaining', headers['x-rate-limit-remaining'])
    js = json.load(data)
    print(json.dumps(js, indent=4))

    for u in js['users']:
        print(u['screen_name'])
        s = u['status']['text']
        print('  ', s[:50])
