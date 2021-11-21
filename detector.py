import sys
import os
import numpy
from PIL import Image
import dlib

if len(sys.argv) < 3:
    print(
        "Call this program like this:\n"
        "   ./cnn_face_detector.py mmod_human_face_detector.dat ../examples/faces/*.jpg\n"
        "You can get the mmod_human_face_detector.dat file from:\n"
        "    http://dlib.net/files/mmod_human_face_detector.dat.bz2")
    exit()

cnn_face_detector = dlib.cnn_face_detection_model_v1(sys.argv[1])

for f in sys.argv[2:]:
    print("Processing file: {}".format(f))
    img = dlib.load_rgb_image(f)

    dets = cnn_face_detector(img, 1)

    print("Number of faces detected: {}".format(len(dets)))
    for i, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {} Confidence: {}".format(
            i, d.rect.left(), d.rect.top(), d.rect.right(), d.rect.bottom(), d.confidence))

    rects = dlib.rectangles()
    rects.extend([d.rect for d in dets])

    for i, d in enumerate(dets):
        print("Detection {}, score: {}, face_type:{}".format(
            i, d.rect.left(), d.rect.top(), d.rect.right(), d.rect.bottom(), d.confidence))
        crop = img[d.rect.top():d.rect.bottom(), d.rect.left():d.rect.right()]
        image = Image.fromarray(crop, "RGB")
        image.save(os.path.join("/home/paulius/face/uploads/machine-learning", str(i) + ".jpg"))
    dlib.hit_enter_to_continue()