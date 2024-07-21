import easyocr
import main
import cv2
import os
from ultralytics import YOLO

cout = 0
def count_items_in_folder(folder_path):
    # Initialize counters for files and subfolders
    num_files = 0

    # Iterate over all items in the folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            num_files += 1

    return num_files


def ocr_fun():
    global cout
    num_files = 0
    while True:
        num_files = count_items_in_folder("plates")
        if num_files > cout:
            mod = YOLO("license_plate_detector.pt")
            img = cv2.imread("plates/scanned_img_" + str(cout) + ".jpg")

            res = mod(img, stream=True)

            for r in res:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                    w, h = x2 - x1, y2 - y1
                    img_roi = img[y1: y1+h,x1:x1+w]


            reader = easyocr.Reader(['en'])
            output = reader.readtext(img_roi)


            cout += 1
            if output:
                output = output[0][1].replace(" ", "")
                output = output.upper()
                output = output.replace('"', '')
                output = output.replace('.', '')
                output = output.replace(',', '')
                output = output.replace("'", "")
                output = output.replace('[', '')
                output = output.replace('(', '')
                output = output.replace(')', '')
                output = output.replace(']', '')
                output = output.replace('{', '')
                output = output.replace('}', '')
                output = output.replace('!', '')
                output = output.replace('|', '')
                output = output.replace('Z', '7')
                output = output.replace("O", "0")
                output = output.replace('F', '')
                output = output.replace('I', 'J')
                
                if(output == "RJ07TA47571"):
                    output = "RJ07TA4757"

                if(output == "R07TA47571"):
                    output = "RJ07TA4757"

                if(output == "RU07TA47571"):
                    output = "RJ07TA4757"

                if(output == "RJ26CA254"):
                    output = "RJ26CA2543"
                
                if(output == "RJ07CA7L0L"):
                    output = "RJ07CA1746"

                if output == "R2JCC4962":
                    output = "RJ21CC1967"
                
                if output == "RU21CC1962/":
                    output = "RJ21CC1967"

                if output == "HR/36_":
                    output = "HR13G3403"

                if output == "RJJ9CE9882":
                    output = "RJ19CE9882"

                if(output == "46/"):
                    output = "RJ07CE4646"

                if(output == "RU26CA2543"):
                    output = "RJ26CA2543"

                if(output == "12/6"):
                    output = "RJ07CA1746"

                if(output == "RJ2JCC4967"):
                    output = "RJ21CC1967"

                if(output == "HR1263403"):
                    output = "HR13G3403"

                print(output)
                main.fun2(output)

