import requests
from PIL import Image, ImageDraw, ImageFont
import os
import sys

BASE = "http://127.0.0.1:5000/"


# PATH = "C:/Users/guddu/Desktop/Flask-Rest-API-Tutorial/WebProjects-PCToons/git_code/pcadmin/media/"

# os.chdir(PATH)
##response = requests.put(BASE + "video/4", {"name": "gaurav", "views": "10", "id": "4", "likes": "10"})

def tags_choice():
    choice = []
    response = requests.get(BASE + "users")
    # print(response.json())
    for i in response.json():
        # print(i)
        choice.append(tuple(i))

    return choice



