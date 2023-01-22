from fastapi import FastAPI, UploadFile, File
import numpy as np
import pandas as pd
from tensorflow.keras.utils import img_to_array
from keras.models import load_model
import uvicorn 
from PIL import Image
import io



def prepare_image(image, target):
    if image.mode != "RGB":
        image = image.convert("RGB")

    image = image.resize(target)
    image = img_to_array(image)
    image = image / 255 
    image = np.expand_dims(image, axis=0)

    return image



categories = pd.read_csv('category_names.csv')

category_array = [
1000011448, 1000017189, 1000011456, 1000011454, 1000011450, 1000011470, 1000011460, 1000011462, 1000011464, 1000011466,
1000011468, 1000004530, 1000003934, 1000003992, 1000015331, 1000003955, 1000003960, 1000003940, 1000003938, 1000004210,
1000003967, 1000003971, 1000015912, 1000003964, 1000008094, 1000003952, 1000004582, 1000004006, 1000013150, 1000003973,
1000003985, 1000003980, 1000003945, 1000003989, 1000003997, 1000004012, 1000017187, 1000004009, 1000003949, 1000004002, 
1000004000, 1000003977, 1000004014, 1000004085, 1000004056, 1000004019, 1000004526, 1000004016, 1000004067, 1000004024, 
1000004041, 1000004079, 1000004035, 1000004088, 1000004090, 1000004061, 1000007833, 1000008363, 1000004137, 1000004142, 
1000012869, 1000004159, 1000004145, 1000004151, 1000004148, 1000004154, 1000004157, 1000011473, 1000011475, 1000011427, 
1000013218, 1000011435, 1000012886, 1000011443, 1000021450, 1000011445, 1000011437, 1000011429, 1000011431, 1000011439, 
1000011433, 1000011423, 1000004161, 1000004167, 1000004591, 1000004176, 1000004164, 1000004212, 1000004171, 1000004192, 
1000004187, 1000004184, 1000004181, 1000011420, 1000016073, 1000022312, 1000011418, 1000022309, 1000003947, 1000004004, 
1000003943, 1000003950, 1000003957, 1000004682, 1000004540, 1000003986, 1000004022, 1000007984, 1000004097, 1000004115, 
1000004135, 1000017742, 1000004536, 1000004141, 1000004147, 1000011383, 1000004153, 1000004163, 1000004169, 1000004676, 
1000004174, 1000011391, 1000011397, 1000011393, 1000011401, 1000011403, 1000022303, 1000011395, 1000011405, 1000011407, 
1000011409, 1000011411, 1000011415, 1000011386, 1000022305, 1000011388, 1000022307, 1000011377, 1000011375, 1000010608, 
1000022319, 1000010610, 1000022321]

category_array = sorted(category_array)

def get_category_id(index):
    global category_array
    print(category_array[index+1])

    return category_array[index]


def get_label(index):
    global category_id, category
    category_id = get_category_id(index)
    category = categories.loc[categories['category_id'] == category_id]
    return category['category_level3_en'].array[0]

app = FastAPI()
model = load_model('./model/0610_1906.h5') 
model.load_weights('./model/0610_1906.h5')


def predict(image):
    image = Image.open(io.BytesIO(image))
    # image = Image.open(image)
    image = prepare_image(image, target=(150, 150))
    preds = model.predict(image, batch_size=8)
    print(preds)
    category_index = preds.argmax(1).tolist()
    return get_label(category_index[0])


@app.post("/predict")
async def predict_label(image: UploadFile = File(...)):

    extension = image.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"

    image = await image.read()

    return predict(image)


@app.get("/")
async def root():
    return {"message": "App is running"}

