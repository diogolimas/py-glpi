import urllib2
baseUrl = "https://sd.uitis.ru/apirest.php"
initSessionUrl = baseUrl + '/initSession'
response = urllib2.urlopen(initSessionUrl)
print response.info()
html = response.read()
print html
response.close()

