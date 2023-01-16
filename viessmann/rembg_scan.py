
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from pathlib import Path
from rembg import remove, new_session

import os
from os import path
from PIL import Image

import cv2

import time

session = new_session()

#output_folder = "C:\\ftp\\rembg"
output_folder = "C:\\ftp\\bin\\data\\IN"

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        print(event.src_path.strip() + " is being processed")

        timestep = time.time()

        #PIL
        # i = Image.open(event.src_path.strip())
        # w, h = i.size
        # i_resize = i.resize((2600, int(h*(2600/w))))

        #NumPy
        is_readable = False
        
        while is_readable != True:
            try:
                i = cv2.imread(event.src_path.strip())
                w, h, c = i.shape
                is_readable = True
            except:
                pass

        i_resize = cv2.resize(i, dsize =(int(h*(2600/w)), 2600), interpolation=cv2.INTER_CUBIC)
        print("Resize is finished in " + str(time.time() - timestep))

        output = remove(i_resize, session=session, alpha_matting=True)

        print("Remove is finished in " + str(time.time() - timestep))
        
        output_path = output_folder + "\\" + path.basename(event.src_path.strip()).split(".")[0] + ".png"
        #PIL
        #output.save(output_path)
        cv2.imwrite(output_path, output)
        print (event.src_path.strip() + " is finished in " + str(time.time() - timestep))


event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path='C:\\ftp', recursive=False)
observer.start()


while True:
    try:
        pass
    except KeyboardInterrupt:
        observer.stop()
