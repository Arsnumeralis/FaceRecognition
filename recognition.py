import dlib
import numpy
import sys
import os

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("./data_files/shape_predictor_5_face_landmarks.dat")
recognition_model = dlib.face_recognition_model_v1("./data_files/dlib_face_recognition_resnet_model_v1.dat")
margin = 0.60

# query_img = dlib.load_rgb_image(sys.argv[1]) #for testing

def query_vector(query):
    detected_query = detector(query, 1)
    query_shape = predictor(query, detected_query[0])
    aligned_query = dlib.get_face_chip(query, query_shape)
    query_rep = recognition_model.compute_face_descriptor(aligned_query)
    query_rep = numpy.array(query_rep)
    return query_rep
    

def find_euclidean_distance(query_rep, ref_rep):
    euclidean_distance = query_rep - ref_rep
    euclidean_distance = numpy.sum(numpy.multiply(euclidean_distance, euclidean_distance))
    euclidean_distance = numpy.sqrt(euclidean_distance)
    return euclidean_distance

def recognising(name, query, distance = None):
    ref_rep = numpy.load(os.path.join(name, "representation.npy"))
    if distance is None:
        distance = find_euclidean_distance(query_vector(query), ref_rep)
    print(distance)
    if distance < margin:
        print(f"Match found, the subject is {name}", distance)
        return True
    else:
        print("Not a match", distance)
        return False

if __name__ == "__main__":
    for name in os.listdir("ref"):
        is_person = recognising(os.path.join("ref", name), sys.argv[1])
        if is_person == True:
            break