# -*- coding: utf-8 -*-
"""Find My Pic - CNM.ipynb

Automatically generated by Colab.


# **Find My Pic - ABHILASH s POLE**
*Using ChromaDB and Vector Emebddings*
"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install chromadb
# !pip install pillow
# !pip install open-clip-torch
# !pip install matplotlib
# !pip install gradio

import os
import shutil
import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
from matplotlib import pyplot as plt
import gradio as gr
from PIL import Image

images_folder = '/content/drive/MyDrive/fotos_folder'
img_files = os.listdir(images_folder)

# Create database file at folder "my_vectordb"
chroma_client_cnm = chromadb.PersistentClient(path="my_vector_db")
chroma_client_cnm.read_only = False

# Instantiate image loader helper.
image_loader = ImageLoader()
# Instantiate multimodal embedding function.
multimodal_fnc = OpenCLIPEmbeddingFunction()

# Create the imeags database to store the embeddings
images_db = chroma_client_cnm.get_or_create_collection(name="images_db", embedding_function=multimodal_fnc, data_loader=image_loader)

# Add the images to the database
for file in img_files:
    file_path = os.path.join(images_folder, file)
    images_db.add(
        ids=[file],
        uris=[file_path],
        metadatas=[{'img_category': 'everything'}]

    )

print("The Number of Images in your folder is", images_db.count())

def search_images(query):
    query_results = images_db.query(
        query_texts=[query],
        n_results=2,
        include=['documents', 'distances', 'metadatas', 'data', 'uris']
    )

    result_uris = query_results['uris'][0]
    result_images = [Image.open(uri) for uri in result_uris]

    return result_images

iface = gr.Interface(
    fn=search_images,
    inputs=gr.Textbox(label="Search Query"),
    outputs=gr.Gallery(label="Matching Images"),
    title="Local Image Search Tool",
    description="Enter a description of the image you are looking for."
)

iface.launch(debug=True)