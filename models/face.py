import os
import pickle
import face_recognition
import face_recognition_models

FACES_DIR = 'faces'


class Face:
    def __init__(self, constraints):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        faces_path = os.path.join(dir_path, FACES_DIR)
        self.encodings = []
        for constrain_name in constraints:
            if constrain_name != 'value':
                print('Unsupported constrain {cname} for Face model'.format(cname=constrain_name))
                return
            constraints_value = constraints[constrain_name]
            face_path = os.path.join(faces_path, '{name}'.format(name=constraints_value))
            if not os.path.exists(face_path):
                print('Could not find the specified face: {name}'.format(name=constraints_value))
                return
            with open(face_path, 'rb') as f:
                encoding = pickle.load(f)
            self.encodings.append(encoding)

    def check(self, img_path, frame):
        img = face_recognition.load_image_file(img_path)
        face_encodings = face_recognition.face_encodings(img)
        results = face_recognition.compare_faces(self.encodings, face_encodings)
        return all(results)
