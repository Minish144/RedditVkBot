import urllib.request



url = "https://i.redd.it/ksd4gfhk9i431.jpg"
img = urllib.request.urlopen(url).read()
out = open("img.jpg", "wb")
out.write(img)
out.close
