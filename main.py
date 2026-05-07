from fastapi import FastAPI, File, UploadFile
import numpy as np
from PIL import Image
import io
import tensorflow.lite as tflite

app = FastAPI()

# تحميل موديل TFLite
interpreter = tflite.Interpreter(model_path="currency_model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

@app.get("/")
def home():
    return {"message": "Fake Currency API is working 🚀"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = await file.read()

    img = Image.open(io.BytesIO(image)).convert("RGB")
    img = img.resize((224, 224))

    img = np.array(img, dtype=np.float32) / 255.0
    img = np.expand_dims(img, axis=0)

    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()

    output = interpreter.get_tensor(output_details[0]['index'])

    result = "Fake 💰" if output[0][0] > 0.5 else "Real 💵"

    return {"result": result}