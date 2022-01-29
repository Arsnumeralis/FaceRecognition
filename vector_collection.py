import dlib
import numpy
import os
import sys

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("./data_files/shape_predictor_5_face_landmarks.dat")
recognition_model = dlib.face_recognition_model_v1("./data_files/dlib_face_recognition_resnet_model_v1.dat")

def vector_collection_local(name):
    for filename in os.listdir(os.path.join("ref", name)):
        reference_img_path = os.path.join("ref", name, filename)
        reference_img = dlib.load_rgb_image(reference_img_path)
        detected_reference = detector(reference_img, 1)
        print(filename, len(detected_reference))
        reference_shape = predictor(reference_img, detected_reference[0])
        aligned_reference = dlib.get_face_chip(reference_img, reference_shape)
        reference_rep = recognition_model.compute_face_descriptor(aligned_reference)
        reference_rep = numpy.array(reference_rep)
        numpy.save(os.path.join(f"ref/{name}", filename), reference_rep)

def vector_collection(name, file, data):
    # reference_img = dlib.load_rgb_image(file) #for testing
    reference_img = data
    detected_reference = detector(reference_img, 1)
    print(file, len(detected_reference))
    if len(detected_reference) == 1:
        reference_shape = predictor(reference_img, detected_reference[0])
        aligned_reference = dlib.get_face_chip(reference_img, reference_shape)
        reference_rep = recognition_model.compute_face_descriptor(aligned_reference)
        reference_rep = numpy.array(reference_rep)
        # I save all reference vectors so that if I add more reference pictures, the average representation wouldn't lose accuracy
        numpy.save(os.path.join(f"ref/{name}", file), reference_rep)

def average_representation(person, compound_ref = None):
    if compound_ref is None:
        compound_ref = []
    for file in os.listdir(os.path.join("ref", person)):
        if os.path.basename(os.path.join(f"ref/{person}", file)) == "representation.npy":
            continue
        rep = numpy.load(os.path.join(f"ref/{person}", file))
        compound_ref.append(rep)
    avg_rep = numpy.mean(numpy.array(compound_ref), axis=0)
    numpy.save(os.path.join(f"ref/{person}", "representation"), avg_rep)
        

if __name__ == "__main__":
    vector_collection(sys.argv[1])



