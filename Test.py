import cv2
from ultralytics import YOLO
from flask import Flask, render_template, Response, request, jsonify
from flask_socketio import SocketIO
import cvzone
import math
import threading
import time
import main
import ocr

app = Flask(__name__)
socketio = SocketIO(app)

model = YOLO("yolov8n.pt")
minarea = 500
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]
line_pos = 650
detect = []


def centre(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy


def generate_frames():
    count = 0
    offset = 5
    cap = cv2.VideoCapture("images/lv_0_20240520171000.mp4")
    while True:
        sucess, img = cap.read()
        result = model(img, stream=True)
        # cv2.line(img, (0, line_pos), (3000, line_pos), (255, 127, 0), 3)
        for r in result:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                cls = int(box.cls[0])

                w, h = x2 - x1, y2 - y1
                if cls == 2:
                    cvzone.cornerRect(img, (x1, y1, w, h))
                    img_roii = img[y1: y1+h,x1:x1+w]


                if (classNames[cls] == 'car') or (classNames[cls] == 'truck'):
                    centro = centre(x1, y1, w, h)
                    detect.append(centro)
                    cv2.circle(img, centro, 4, (0, 0,255), -1)

                for (x, y) in detect:
                     if y<(line_pos+offset) and y>(line_pos-offset):

                        #  cv2.line(img, (50, line_pos), (3000, line_pos), (0,127,255), 3)
                         detect.remove((x,y))
                         cv2.imwrite("plates/scanned_img_" + str(count) + ".jpg", img_roii)
                         print("car is detected : "+str(count))
                         count+=1
                        

        # cv2.putText(img, "VEHICLE COUNT : "+str(count), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),5)
        

        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


def send_data():
    while True:
        time.sleep(1)
        data = main.res2 
        resultString = '<table style="border: 1px solid black"><tr style="border: 1px solid black"><th style="border: 1px solid black">License_number</th><th style="border: 1px solid black">Registration_date</th><th style="border: 1px solid black">Registration_exp_date</th><th style="border: 1px solid black">Name</th><th style="border: 1px solid black">Number</th><th style="border: 1px solid black">Details</th></tr>'
        for item in data:
            resultString += '<tr style="border: 1px solid black"><td style="border: 1px solid black">' + str(item[2]) + '</td><td style="border: 1px solid black">' + str(item[1]) + '</td></td><td style="border: 1px solid black">' + str(item[3]) + '</td></td><td style="border: 1px solid black">' + str(item[5]) + '</td><td style="border: 1px solid black">' + str(item[6]) + '</td><td style="border: 1px solid black">' + str(item[8]) + '</td></tr>'
        resultString += '</table>'
        socketio.emit('data', resultString)


def sockito_run():
    socketio.run()

# Flask route
@app.route('/')
def hello():
    return render_template('index.html')



if __name__ == '__main__':
    # Create a thread for running Flask
    flask_thread = threading.Thread(target=app.run)
    flask_thread.start()

    # Create and start the processing thread
    processing_thread = threading.Thread(target=ocr.ocr_fun)
    processing_thread.start()

    socketio.start_background_task(send_data()) 
    socketio.run(app)

    # Continue with the main program
    print("Flask and processing threads started.")
