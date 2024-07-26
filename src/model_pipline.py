# from transformers import AutoImageProcessor, AutoModelForImageClassification
from transformers import pipeline

# pipe = pipeline("image-classification", model="Falconsai/nsfw_image_detection")


# processor = AutoImageProcessor.from_pretrained("Falconsai/nsfw_image_detection")
# model = AutoModelForImageClassification.from_pretrained("Falconsai/nsfw_image_detection")


# class nsfwModel():
#     '''
#     This is the class for nsfw model and the pipline for the model 
#     args :
#     X - image pixel 
#     '''
#     def __init__(self) -> None:
#         self.pipe = pipeline("image-classification", model="Falconsai/nsfw_image_detection")
#         self.process_pipeline = AutoImageProcessor.from_pretrained("Falconsai/nsfw_image_detection")
#         self.model = AutoModelForImageClassification.from_pretrained("Falconsai/nsfw_image_detection")

#     def predict(self, X):
#         X =  self.pipe(X)
#         X = self.processor(X)
#         X = self.model.predict()
        
#         return X
    

# import cv2 
# img  = cv2.imread(r"C:\\Users\shuga\\Pictures\\josh-nuttall-xl2piFfdzyA-unsplash.jpg", cv2.IMREAD_COLOR)

# model  = nsfwModel()
# print(model.predict(img))

        
        