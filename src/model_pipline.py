import torch
from PIL import Image
from transformers import AutoModelForImageClassification, ViTImageProcessor   
from PIL import Image
from transformers import pipeline
from PIL import Image
import numpy as np

import os




class nsfwModel():
    '''
    This is the class for nsfw model and the pipline for the model 
    args :
    X - image pixel 
    '''
    def __init__(self) -> None:
        self.model = AutoModelForImageClassification.from_pretrained("Falconsai/nsfw_image_detection")
        self.processor = ViTImageProcessor.from_pretrained('Falconsai/nsfw_image_detection')

    def predict(self,X):

        inputs = self.processor(images=X, return_tensors="pt")
        outputs = self.model(**inputs)
        logits = outputs.logits
        predicted_label = logits.argmax(-1).item()
        return self.model.config.id2label[predicted_label]

# import cv2 
# img  = cv2.imread(r"C:\\Users\shuga\\Pictures\\josh-nuttall-xl2piFfdzyA-unsplash.jpg", cv2.IMREAD_COLOR)
# image = Image.open(r"C:\\Users\shuga\\Pictures\\josh-nuttall-xl2piFfdzyA-unsplash.jpg")
# model  = nsfwModel()

# # print(img)
# print(model.predict(image))

        
        

# Use a pipeline as a high-level helper
# from PIL import Image
# from transformers import pipeline

# img = Image.open(r"C:\\Users\shuga\\Pictures\\josh-nuttall-xl2piFfdzyA-unsplash.jpg")
# classifier = pipeline("image-classification", model="Falconsai/nsfw_image_detection")
# classifier(img)


# Load model directly
# import torch
# from PIL import Image
# from transformers import AutoModelForImageClassification, ViTImageProcessor

# img = Image.open(r"C:\\Users\shuga\Downloads\\my-milf-pussy-is-just-so-lonely-here-in-the-backseat-all-v0-ey5l5sym8gfd1.webp")
# model = AutoModelForImageClassification.from_pretrained("Falconsai/nsfw_image_detection")
# processor = ViTImageProcessor.from_pretrained('Falconsai/nsfw_image_detection')
# with torch.no_grad():
#     inputs = processor(images=img, return_tensors="pt")
#     outputs = model(**inputs)
#     logits = outputs.logits

# predicted_label = logits.argmax(-1).item()
# print(model.config.id2label[predicted_label])
