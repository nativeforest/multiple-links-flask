#!/usr/bin/env python
#
# Project: Video Streaming with Flask
# Author: Log0 <im [dot] ckieric [at] gmail [dot] com>
# Date: 2014/12/21
# Website: http://www.chioka.in/
# Description:
# Modified to support streaming out with webcams, and not just raw JPEGs.
# Most of the code credits to Miguel Grinberg, except that I made a small tweak. Thanks!
# Credits: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
#
# Usage:
# 1. Install Python dependencies: cv2, flask. (wish that pip install works like a charm)
# 2. Run "python main.py".
# 3. Navigate the browser to the local webpage.
from flask import Flask, render_template, Response,url_for;
from camera import VideoCamera
import json
from time import time
from random import random
from flask import Flask, render_template, make_response

app = Flask(__name__)

@app.route('/home/') 
def home():
    createLink="   <a href='   "+url_for('camerapp')+"' '> camera pp</a>";
    createLink2="   <a href='   "+url_for('video_feed')+"' '> Video Feed</a>";
    createLink3="   <a href='   "+url_for('livechart')+"' '> Temperature</a>";
    return """ <html>
                           <title>OPTIONS</title>
                             <head>
                             <p>   """+createLink3+ """</p>
                              
                                         <title>hello--</title>
                             </head>
                                         <body>
                                             """+createLink+ """
                                         </body>
                       </html> """;                 
   # return render_template('index2.html')


@app.route('/livechart')
def livechart():
    return render_template('livechart.html', data='test')

@app.route('/live-data')
def live_data():
    
    # Create a PHP array and echo it as JSON
    data = [time() * 1000, random() * 100]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response











@app.route('/camera')
def  camerapp():
    return render_template('index2.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.errorhandler(404)
def page_not_found(error):
    return 'This fucking page does not exist', 404


if __name__ == '__main__':
    app.run(host='192.168.0.6', debug=True)
