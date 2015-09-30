import json, requests

url = 'https://api.karma.wiki/search'
payload = {'kind': 'Letter', 'limit' : 999}
headers = {"x-auth-token" : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwZXJtaXNzaW9ucyI6InJlc3RyaWN0ZWQiLCJpYXQiOjE0NDIyMTE2MDAsImV4cCI6MTQ0MzAwNjE2MywiYXVkIjoic0F6OHdzTnBDdzYxU0oxcW0xOXR1TGowQVlpVzZKSTYiLCJpc3MiOiJodHRwczovL2thcm1hd2lraS5hdXRoMC5jb20iLCJzdWIiOiJhdXRoMHw1NWYwZjQ0YzU1ZjJlNTYxNWQwN2Q2ZTkifQ.ocM9_VwMOYpyZZjMvbgGHDqgpbeK7kCOIX3tLlSxjwQ'}
response = requests.post(url, data=json.dumps(payload), headers=headers)

xx = json.loads(response.text)

ff = open('k_reviews.txt', 'w')

for i in xrange(len(xx)):
	try:
		x = xx[i][u'Data'][u'html'].encode('ascii','ignore').strip()
		if len(x) < 100000:
			ff.write(x)
			ff.write("\r\n")
	except KeyError:
		continue

ff.close()
