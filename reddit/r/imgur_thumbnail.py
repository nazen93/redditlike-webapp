import requests
from PIL import Image
from io import BytesIO
import urllib
import os
from random import randrange
from django.conf import settings

class ImgurThumbnail:
    """
    Takes imgur link as an argument and returns the url of the thumbnail of the given image
    """
    
    def imgur_imageid(self, url):
        imgur_list = url.split('/')
        imgur_id = imgur_list[-1]
        return imgur_id           
        
    def imgur_thumbnail(self, url, imgur_id):
        imgurl = requests.get('https://api.imgur.com/3/gallery/'+imgur_id(url))
        imgurl_json = imgurl.json()
        try:
            imgurl_image = imgurl_json['data']['images'][0]['link']
        except KeyError:
            imgurl_image = imgurl_json['data']['link']

        return imgurl_image
    
    def imgur_image_large(self, url):
        splitted_url = url.split('.')
        splitted_url[-2] = splitted_url[-2]+'l'
        thumbnail_url = '.'.join(splitted_url)
        return thumbnail_url
    
    def download_thumbnail(self, new_thumbnail, url, imgur_id):
        image = requests.get(new_thumbnail(url, imgur_id))
        file = Image.open(BytesIO(image.content))
        file.thumbnail((70,70), Image.ANTIALIAS)
        picture_file = BytesIO()
        imgurl_id = self.imgur_imageid(url)
        image_name = imgurl_id +'.jpg'
        if image_name in os.listdir(settings.MEDIA_ROOT):
            random_number = randrange(100)
            image_name = imgurl_id +str(random_number)+'.jpg'
        file_name = settings.MEDIA_ROOT+'/'+image_name       
        file.save(file_name, 'JPEG')
        return file_name
