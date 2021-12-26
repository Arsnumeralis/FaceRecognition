import dlib
import numpy
import os
import sys

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("./data_files/shape_predictor_5_face_landmarks.dat")
recognition_model = dlib.face_recognition_model_v1("./data_files/dlib_face_recognition_resnet_model_v1.dat")

def vector_collection_local(name):
    for filename in os.listdir(os.path.join("ml", name)):
        reference_img_path = os.path.join("ml", name, filename)
        reference_img = dlib.load_rgb_image(reference_img_path)
        detected_reference = detector(reference_img, 1)
        print(filename, len(detected_reference))
        reference_shape = predictor(reference_img, detected_reference[0])
        aligned_reference = dlib.get_face_chip(reference_img, reference_shape)
        reference_rep = recognition_model.compute_face_descriptor(aligned_reference)
        reference_rep = numpy.array(reference_rep)
        numpy.save(os.path.join(f"ml/{name}", filename), reference_rep)

def vector_collection(name, file, data):
    # reference_img = dlib.load_rgb_image(file)
    reference_img = data
    detected_reference = detector(reference_img, 1)
    print(file, len(detected_reference))
    if len(detected_reference) == 1:
        reference_shape = predictor(reference_img, detected_reference[0])
        aligned_reference = dlib.get_face_chip(reference_img, reference_shape)
        reference_rep = recognition_model.compute_face_descriptor(aligned_reference)
        reference_rep = numpy.array(reference_rep)
        numpy.save(os.path.join(f"ml/{name}", file), reference_rep)

if __name__ == "__main__":
    vector_collection(sys.argv[1])



