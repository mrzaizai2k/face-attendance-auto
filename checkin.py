# Step 1: Import necessary libraries
import cv2
import numpy as np
from utils import *

def main():

    cap = initialize_camera()

    while True:
        _, frame = cap.read()

        faces = detect_faces(frame)
        if len(faces) > 0:
            break

        # Step 9: Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Step 10: Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()


    face = FaceScraper(show_UI = True)

    attemp = 0
    max_attemps = 3
    while attemp <= max_attemps:
        isface = face.signin()
        if isface:
            # face.close_broser() 
            time.sleep(10)
            break
        attemp += 1

if __name__ == "__main__":
    main()
