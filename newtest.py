from deepface import DeepFace
import os
import json

dataset_path = "D:\kandupidtham\ArjunProjectDefense\images"
embeddings = {}
print('helo')
for person_folder in os.listdir(dataset_path):
    person_path = os.path.join(dataset_path, person_folder)
    print('pers   ::  ' + person_path)
    if os.path.isdir(person_path):
        embeddings[person_folder] = []
        for image_file in os.listdir(person_path):
            image_path = os.path.join(person_path, image_file)
            embedding = DeepFace.represent(image_path, model_name="Facenet", enforce_detection=False)
            embeddings[person_folder].append(embedding)

# print("embedding -------------" + embeddings)
with open("embeddings.json", "w") as f:
    json.dump(embeddings, f)
