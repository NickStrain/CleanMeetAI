import torch
from PIL import Image
from transformers import AutoModelForImageClassification, ViTImageProcessor ,pipeline,Speech2TextProcessor, Speech2TextForConditionalGeneration
from PIL import Image
from fastapi import WebSocket, WebSocketDisconnect
import numpy as np
import os
import soundfile as sf
import io
from transformers import pipeline
from transformers import AutoTokenizer,AutoModelForSequenceClassification
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
model_id = "distil-whisper/distil-medium.en"
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

        input_features = self.processor(images=X, return_tensors="pt")
        outputs = self.model(**input_features)
        logits = outputs.logits
        predicted_label = logits.argmax(-1).item()
        return self.model.config.id2label[predicted_label]
    

class speech2text():
    '''
    This class is for the speech2text

    '''
    def __init__(self) -> None:
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True).to(device)
        self.processor = AutoProcessor.from_pretrained(model_id)
        self.pipe = pipeline("automatic-speech-recognition",model=self.model,
                                    tokenizer=self.processor.tokenizer,
                                    feature_extractor=self.processor.feature_extractor,
                                    max_new_tokens=128,
                                    torch_dtype=torch_dtype,
                                    device=device,)

    def predict(self,X):
        res = self.pipe(X)
        return res
class Textclassifier():
    def __init__(self) -> None:
        '''
        init all the args from the HF :);
        '''
        self.tokenizer = AutoTokenizer.from_pretrained("JungleLee/bert-toxic-comment-classification")
        self.model = AutoModelForSequenceClassification.from_pretrained("JungleLee/bert-toxic-comment-classification")
        self.pipe = pipeline("text-classification", model="JungleLee/bert-toxic-comment-classification")
    def pred(self,x) -> any  :
        '''
        Predict function:
        x: Input value 
        '''
        a  = self.pipe(x)

        return a

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_transcript(self, websocket: WebSocket, message: str):
        await websocket.send_text(message)

# model = Speech2TextForConditionalGeneration.from_pretrained("facebook/s2t-medium-mustc-multilingual-st")
# processor = Speech2TextProcessor.from_pretrained("facebook/s2t-medium-mustc-multilingual-st")
# if __name__ == "__main__":
#     from datasets import load_dataset
#     import soundfile as sf
#     def map_to_array(batch):
#         speech, _ = sf.read(batch["file"])
#         batch["speech"] = speech
#         return batch

#     ds = load_dataset("patrickvonplaten/librispeech_asr_dummy", "clean", split="validation")
#     ds = ds.map(map_to_array)

#     print(ds["speech"][0])