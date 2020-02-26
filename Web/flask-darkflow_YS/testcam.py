import sys, cv2, time


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

def runcam():

    camera = cv2.VideoCapture(0)

    for i in range(10):
        time.sleep(1)  # implemented for cams with long image aquisition time. Its 1 sec.
                       # delay before the next step is repeated until range has finished.
                       # From first image to last each image becomes brighter.
        return_value, image = camera.read()
        cv2.imwrite('opencv'+str(i)+'.png', image)
        print (' taking image %s' % (i+1))


    del(camera)

    # Back up the reference to the exceptionhook
    sys._excepthook = sys.excepthook

    # Set the exception hook to our wrapping function
    sys.excepthook = my_exception_hook

def check_cam_index():
    i = 0
    found = False
    for i in range(4):
            capture = cv2.VideoCapture(i)
            if not capture:
                print ("UNABLE TO CAPTURE CAMERA")
            else:
                found = True
                print ("taken camera from index: ", i)
                break

    if found == False:
        print ("!!! No camera was found.")
        sys.exit()


if __name__ == '__main__':
    check_cam_index()
    runcam()
