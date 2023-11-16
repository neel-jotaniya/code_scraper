import requests
import urllib


r = requests.get('http://example.org', proxies=urllib.request.getproxies())
print(r.status_code)