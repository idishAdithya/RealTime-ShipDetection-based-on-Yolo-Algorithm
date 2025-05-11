import numpy as np
from tkinter import *
import os
from tkinter import filedialog
import cv2
import time,sys
from matplotlib import pyplot as plt
from tkinter import messagebox


def endprogram():
	print ("\nProgram terminated!")
	sys.exit()




def testing():
    global testing_screen
    testing_screen = Toplevel(main_screen)
    testing_screen.title("Testing")
    # login_screen.geometry("400x300")
    testing_screen.geometry("600x450+650+150")
    testing_screen.minsize(120, 1)
    testing_screen.maxsize(1604, 881)
    testing_screen.resizable(1, 1)
    testing_screen.configure(bg='cyan')
    # login_screen.title("New Toplevel")

    Label(testing_screen, text='''Upload Image''', disabledforeground="#a3a3a3",
          foreground="#000000", width="300", height="2",bg='cyan', font=("Calibri", 16)).pack()
    Label(testing_screen, text="").pack()
    Label(testing_screen, text="").pack()
    Label(testing_screen, text="").pack()
    Button(testing_screen, text='''Upload Image''', font=(
        'Verdana', 15), height="2", width="30",bg='cyan', command=imgtest).pack()


global affect
def imgtest():
    # import impre
    import_file_path = filedialog.askopenfilename()

    # image = cv2.imread(import_file_path)
    image = cv2.imread(import_file_path)
    from ultralytics import YOLO
    model = YOLO('runs/detect/ship/weights/best.pt')

    # Run YOLOv8 inference on the image
    results = model(image, conf=0.1)

    # Annotate the image
    annotated_image = image.copy()

    for result in results:
        if result.boxes:
            for box in result.boxes:
                # Extract class ID and name
                class_id = int(box.cls)
                object_name = model.names[class_id]

                # Extract bounding box coordinates (x1, y1, x2, y2)
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Calculate bounding box area
                width = x2 - x1
                height = y2 - y1
                area = width * height

                # Draw the bounding box and label
                cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{object_name}"
                cv2.putText(
                    annotated_image, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
                )

                print(f"Detected: {object_name}")

    # Display the annotated image
    cv2.imshow("YOLOv8 Prediction", annotated_image)
    cv2.waitKey(0)  # Wait for a key press to close the window
    cv2.destroyAllWindows()


def Camera1():
    import cv2
    from ultralytics import YOLO

    # Load the YOLOv8 model
    model = YOLO('runs/detect/ship/weights/best.pt')

    # Open webcam
    cap = cv2.VideoCapture(0)
    dd1 = 0

    # Distance estimation parameters
    KNOWN_WIDTH = 50  # in cm
    FOCAL_LENGTH = 700  # estimated focal length in pixels

    # Loop through video frames
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # YOLOv8 inference
        results = model(frame, conf=0.8)
        result = results[0]

        annotated_frame = frame.copy()

        if len(result.boxes) > 0:
            for box in result.boxes:
                class_id = int(box.cls)
                object_name = model.model.names[class_id]

                # Bounding box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                box_width = x2 - x1

                # Estimate distance
                distance = 0
                if box_width > 0:
                    distance = (KNOWN_WIDTH * FOCAL_LENGTH) / box_width

                # Draw bounding box and label
                label = f"{object_name} ({distance:.1f} m)"
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(annotated_frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                print(f"Detected: {object_name} - Distance: {distance:.2f} m")

                # Detection trigger
                if object_name != '':
                    dd1 += 1

                if dd1 == 20:
                    dd1 = 0
                    cv2.imwrite("alert.jpg", annotated_frame)
                    sendmail()
                    sendmsg("9786395112", f"Prediction Name: {object_name}, Distance: {distance:.2f} m")

        # Display frame
        cv2.imshow("YOLOv8 Inference with Distance", annotated_frame)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def sendmsg(targetno,message):
    import requests
    requests.post(
        "http://sms.creativepoint.in/api/push.json?apikey=6555c521622c1&route=transsms&sender=FSSMSS&mobileno=" + targetno + "&text=Dear customer your msg is " + message + "  Sent By FSMSG FSSMSS")


def sendmail():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "projectmailm@gmail.com"
    toaddr =  "dharshann012@gmail.com"

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Alert"

    # string to store the body of the mail
    body = "Ship Detection"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "alert.jpg"
    attachment = open("alert.jpg", "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "qmgn xecl bkqv musr")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()


def main_account_screen():
    global main_screen
    main_screen = Tk()
    width = 600
    height = 600
    screen_width = main_screen.winfo_screenwidth()
    screen_height = main_screen.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    main_screen.geometry("%dx%d+%d+%d" % (width, height, x, y))
    main_screen.resizable(0, 0)
    # main_screen.geometry("300x250")
    main_screen.configure()
    main_screen.title("Ship  Detection ")

    Label(text=" Ship  Detection", width="300", height="5", font=("Calibri", 16)).pack()

    Label(text="").pack()
    Button(text="Image", font=(
        'Verdana', 15), height="2", width="30", command=imgtest).pack(side=TOP)
    Label(text="").pack()
    Button(text="Camera", font=(
        'Verdana', 15), height="2", width="30", command=Camera1).pack(side=TOP)

    main_screen.mainloop()


main_account_screen()
