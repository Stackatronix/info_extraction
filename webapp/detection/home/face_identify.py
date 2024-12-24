# import json
# import numpy as np
# from deepface import DeepFace

# def cosine_distance(embedding1, embedding2):
#     embedding1 = np.array(embedding1).flatten()
#     embedding2 = np.array(embedding2).flatten()
    
#     # Check if they have the same shape
#     print('-------------------------uploaded_embedding')
#     print(embedding1.shape)
#     # print(embedding1)
#     print('-----------------------our embedding')
#     print(embedding2.shape)
#     # print(embedding2)
#     if embedding1.shape != embedding2.shape:
#         print(f"Shape mismatch: {embedding1.shape} != {embedding2.shape}")
#         raise ValueError("Embeddings must have the same shape")

#     print('------------')
#     print(f"Type of embedding1: {type(embedding1)}")
#     print(f"Type of embedding2: {type(embedding2)}")
#     # Calculate cosine distance
#     return 1 - (np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2)))

# # Load saved embeddings
# with open("embeddings.json", "r") as f:
#     embeddings = json.load(f)

# uploaded_image_path = "1test.jpeg"
# uploaded_embedding = DeepFace.represent(uploaded_image_path, model_name="Facenet", enforce_detection=False)


# threshold = 0.3  # Set based on testing
# best_match = None
# best_score = float("inf")

# print("Shape of uploaded embedding:", np.array(uploaded_embedding[0]['embedding']).shape)
# # print("Shape of a saved embedding (first person):", np.array(embeddings['facial_area'][0]).shape)  # Adjust the key 'person_name'

# for person, person_embeddings in embeddings.items():
#     for embedding in person_embeddings:
#         # Ensure the embeddings are the same shape before calculating distance
#         score = cosine_distance(uploaded_embedding[0]['embedding'], embedding[0]['embedding'])
#         if score < best_score and score < threshold:
#             best_match = person
#             best_score = score

# if best_match:
#     print(f"Match found: {best_match}")
#     print(f"Match score: {best_score}")
# else:
#     print("No match found.")
