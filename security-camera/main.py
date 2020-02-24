import cv2
from flask import Flask, render_template, Response
from camera import VideoCamera
import threading
lock = threading.Lock()

video_camera = VideoCamera(flip=False)  # creates a camera object, flip vertically
object_classifier = cv2.CascadeClassifier("models/facial_recognition_model.xml") # an opencv classifier


# App Globals (do not edit)
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        frame, found_object = camera.get_frame()
        # if found_object:
        #     print("have object detect")
        # else:
        #     print("no object detect")
        # print(found_object)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)


