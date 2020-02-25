import cv2
from flask import Flask, render_template, Response
from camera import VideoCamera
import threading
import time
import datetime
from upload import upload_images
lock = threading.Lock()

email_update_interval = 5  # sends an email only once in this time interval
video_camera = VideoCamera(flip=False)  # creates a camera object, flip vertically
object_classifier = cv2.CascadeClassifier("models/facial_recognition_model.xml") # an opencv classifier


# App Globals (do not edit)
app = Flask(__name__)


def timestamp():
    tstring = datetime.datetime.now()
    print("Filename generated ...")
    return tstring.strftime("%Y%m%d_%H%M%S")


local_file = timestamp()
print(local_file)
@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    last_epoch = 0
    while True:
        frame, found_object = camera.get_frame()
        if found_object and (time.time() - last_epoch) > email_update_interval:
            local_file = timestamp()
            print(local_file)
            last_epoch = time.time()
            image = camera.get_image(local_file)
            upload_images(local_file)
            print(image)

        # print(found_object)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)


