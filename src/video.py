import os
import re
from io import BytesIO

import requests
from pytube import YouTube
from PIL import Image, ImageChops

class Video:
    def __init__(self, video_url, output_directory):
        self.youtube = YouTube(video_url)
        self.output_directory = output_directory

    def get_title(self):
        return self.youtube.streams[0].title

    def get_base_name(self):
        return re.sub(r'[^0-9a-zA-Z]+', '', self.get_title())

    def get_image_path(self):
        return self.__get_path('{}.png')

    def get_audio_path(self):
        return self.__get_path('{}.mp3')

    def save_image(self, image):
        image_file_path = self.get_image_path()
        image = image.save(image_file_path)
        return self.get_image_path()

    def download_image(self):
        if os.path.exists(self.get_image_path()) is False:
            response = requests.get(self.__get_image_url())
            image = Image.open(BytesIO(response.content))
            self.save_image(self.__crop_image_border(image))

    def download_audio(self):
        youtube_streams = self.youtube.streams.filter(only_audio=True).first()
        audio_file_name = f'{self.get_base_name()}.mp3'
        if os.path.exists(self.get_audio_path()) is False:
            youtube_streams.download(output_path=self.output_directory, filename=audio_file_name)

    def __get_path(self, extension_str):
        return os.path.join(self.output_directory, extension_str.format(self.get_base_name()))

    def __get_image_url(self):
        return self.youtube.thumbnail_url

    def __crop_image_border(self, image):
        bbox = ImageChops.add(image, image, 1, -100).getbbox()
        cropped_image = image.crop(bbox) if bbox else image
        return cropped_image
