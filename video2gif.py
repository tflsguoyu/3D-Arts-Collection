import os
import cv2
import glob
import argparse
import numpy as np
from PIL import Image
from PIL import GifImagePlugin
GifImagePlugin.LOADING_STRATEGY = GifImagePlugin.LoadingStrategy.RGB_ALWAYS

video2imgs = False
imgs2gif = True

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Convert video to images')
    parser.add_argument('filename', type=str, help='path to input video')
    args = parser.parse_args()

    # Video to images
    if video2imgs:
        cap = cv2.VideoCapture(args.filename)
        if (cap.isOpened() == False): 
            print("Error opening video")
            exit()

        out_dir = args.filename[:-4]
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        idx = 0
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                cv2.imwrite(os.path.join(out_path, '%03d.png' % idx), frame)
                idx += 1     
            else: 
                break                 
        
        cap.release()
        print('Video to images DONE')
 
    # Images to GIF
    if imgs2gif:
        in_dir = args.filename[:-4]
        out_fn = args.filename[:-4] + '.gif'
        
        imgs = [Image.open(f) for f in sorted(glob.glob(os.path.join(in_dir,'*.*')))]
        
        width, height = imgs[0].size
        left = int((width - height)/2)
        right = left + height
        top = 0
        bottom = height
        
        for i in range(len(imgs)):
            imgs[i] = imgs[i].crop((left, top, right, bottom)).resize((256,256))
            k = 1.8 # enlarge brightness
            imgs[i] = Image.fromarray(np.uint8(((np.array(imgs[i]).astype(np.float32)/255)**(2.2)*k)**(1/2.2)*255))
        
        img = imgs[0]
        img.save(out_fn, format = 'GIF', append_images = imgs[1:], 
            save_all = True, duration = 1000/30, loop = 0)
        print('Images to GIF DONE')
