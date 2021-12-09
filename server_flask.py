from flask import Flask
from flask import Response
import cv2
import threading

global frames

app = Flask(__name__)
@app.route("/")
def helloworld():
    str = "<html> Hello world from bj-pc </html>"
    return str 

def encodeframe():
    global frames
    
    while True:
        ret, encoded_image = cv2.imencode('.jpg',frames)
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_image) + b'\r\n')
    return

@app.route("/streaming")
def streamframe():
    return Response(encodeframe(), mimetype = 'multipart/x-mixed-replace; boundary=frame')   

def captureframe():
    global frames
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, img = cap.read()
        frames = img.copy()
        cv2.imshow('frame',img)
        if cv2.waitKey(1) == 27:
            break
    return

if __name__ == '__main__':
    cap_thread = threading.Thread(target=captureframe)
    cap_thread.daemon = True
    cap_thread.start()
    app.run(host = '0.0.0.0', port ='8000')

cap.release() #
cv2.destroyAllWindows()        

