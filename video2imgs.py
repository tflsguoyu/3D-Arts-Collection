import os
import cv2
import argparse
import numpy as np
 
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Convert video to images')
    parser.add_argument('filename', type=str, help='path to input video')
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.filename)
    if (cap.isOpened() == False): 
        print("Error opening video")
        exit()

    out_path = args.filename[:-4]
    if not os.path.exists(out_path):
        os.mkdir(out_path)

    idx = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            cv2.imwrite(os.path.join(out_path, '%03d.png' % idx), frame)
            idx += 1     
        else: 
            break                 
    
    cap.release()
 
