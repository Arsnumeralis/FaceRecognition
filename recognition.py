import dlib
import numpy
import sys
import os

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(".\\shape_predictor_5_face_landmarks.dat")
recognition_model = dlib.face_recognition_model_v1(".\\dlib_face_recognition_resnet_model_v1.dat")
margin = 0.65


def recognising(name):
    for filename in os.listdir(os.path.join("ml", name)):
        distances = []
        query_img_path = sys.argv[1]
        reference_img_path = os.path.join("ml", name, filename)

        query_img = dlib.load_rgb_image(query_img_path)
        reference_img = dlib.load_rgb_image(reference_img_path)

        detected_query = detector(query_img, 1)
        detected_reference = detector(reference_img, 1)
        print(filename, len(detected_reference))

        query_shape = predictor(query_img, detected_query[0])
        reference_shape = predictor(reference_img, detected_reference[0])

        aligned_query = dlib.get_face_chip(query_img, query_shape)
        aligned_reference = dlib.get_face_chip(reference_img, reference_shape)

        query_rep = recognition_model.compute_face_descriptor(aligned_query)
        query_rep = numpy.array(query_rep)
        reference_rep = recognition_model.compute_face_descriptor(aligned_reference)
        reference_rep = numpy.array(reference_rep)

        def find_euclidean_distance(query_rep, ref_rep):
            euclidean_distance = query_rep - ref_rep
            euclidean_distance = numpy.sum(numpy.multiply(euclidean_distance, euclidean_distance))
            euclidean_distance = numpy.sqrt(euclidean_distance)
            return euclidean_distance

        distance = find_euclidean_distance(query_rep, reference_rep)
        distances.append(distance)
        avg_distance = (sum(distances)/len(distances))

    if avg_distance < margin:
        return f"Match found, the subject is {name}", distance
    else:
        print("Not a match", distance)

if __name__ == "__main__":
    for name in os.listdir("ml"):
        recognising(name)