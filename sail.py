from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from urllib import urlretrieve
import urlparse

import codecs

# url = "http://hanhuazu.cc/cartoon/post?id=9898"
# response = urlopen(url)
# html = response.read()
outpath = "test"
html = codecs.open("shuhui.html", 'r')

parsed_html = BeautifulSoup(html)
content = parsed_html.findAll('img')

f = open("test.txt", "a")
for image in content:
    img_url = 'http:' + image["src"].lower()
    pic = urlopen(img_url)
    #urlretrieve(img_url, outpath)
    content = pic.read()
    f.write(content)
    f.write("\n")

f.close()