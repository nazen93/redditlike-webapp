import requests
from PIL import Image
from io import BytesIO
import urllib
import os
from random import randrange
from django.conf import settings

class ImgurThumbnail:
    """
    Takes imgur link as an argument and returns a thumbnail of the given image.
    """
    
    def imgur_imageid(self, url):
        imgur_list = url.split('/') 
        imgur_id = imgur_list[-1] 
        return imgur_id           
        
    def imgur_thumbnail(self, url):
        imgurl = requests.get('https://api.imgur.com/3/gallery/'+self.imgur_imageid(url))
        imgurl_json = imgurl.json() 
        try:
            imgurl_image = imgurl_json['data']['images'][0]['link']
        except KeyError:
            imgurl_image = imgurl_json['data']['link']

        return imgurl_image
    
    def imgur_image_large(self, url):
        splitted_url = url.split('.')
        splitted_url[-2] = splitted_url[-2]+'l' #adds 'l' to the url to receive the large thumbnail
        thumbnail_url = '.'.join(splitted_url)
        return thumbnail_url
    
    def download_thumbnail(self, url):
        image = requests.get(self.imgur_thumbnail(url))
        file = Image.open(BytesIO(image.content)).convert('RGB') 
        file.thumbnail((70,70), Image.ANTIALIAS)
        picture_file = BytesIO()
        imgurl_id = self.imgur_imageid(url) 
        image_name = imgurl_id +'.jpg'
        if image_name in os.listdir(settings.MEDIA_ROOT): #checks if the image with the same name already exists in the MEDIA_ROOT directory
            random_number = randrange(100)
            image_name = imgurl_id +str(random_number)+'.jpg'
        file_name = settings.MEDIA_ROOT+'/'+image_name       
        file.save(file_name, 'JPEG')
        return file_name

    def thumbnail_file(self, size):
        picture_path = self.image
        picture_path.seek(0)
        picture_file = BytesIO(picture_path.read())
        picture = Image.open(picture_file)
        if size == (255, 255):
            picture = picture.resize(size, Image.ANTIALIAS)
            picture_fullpath = picture_path.path
            base = os.path.basename(picture_fullpath)
            filename = os.path.splitext(base)[0]+'body.jpg'
            file_path = settings.MEDIA_ROOT+'/'+filename
            picture.save(file_path, 'JPEG')
            return file_path
        else:
            picture.thumbnail(size, Image.ANTIALIAS)
            picture_file = BytesIO()
            picture.save(picture_file, 'JPEG')
            return picture_file