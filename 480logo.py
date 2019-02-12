#This program merges Dexter Industries' Raspberry Pi Speech code with their
#Google Vision API logo recognition code.  11/12/18
#ISAT Capstone - Machine Learning with Autonomous Vehicles
#Ben Bland - Kashaun Finch - Dr. Teate


import argparse
import base64
import picamera
import subprocess ##allows for 'call' to be used
import os
import sys

from gtts import gTTS
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials




def takephoto():
    camera = picamera.PiCamera()
    camera.capture('image.jpg')
    camera.close()

def main():
    takephoto() # First take a picture
    """Run a label request on a single image"""

    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials)



    with open('image.jpg', 'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LOGO_DETECTION',
                    'maxResults': 1
                }]
            }]
        })
        response = service_request.execute()
        
        try:
             label = response['responses'][0]['logoAnnotations'][0]['description']
        except:
             label = "No response."
        
        print (label)
        text = label   
        speech=gTTS(text,'en','slow')
        speech.save("testfile.mp3")

        #Calling a CL command to play the newly created file
        #subprocess.call('omxplayer "testfile.mp3"')
        os.system ("omxplayer /home/pi/GoogleVisionTutorials/testfile.mp3")
        

if __name__ == '__main__':
    main()
    