import streamlit as st
from PIL import Image
from keras.preprocessing.image import load_img,img_to_array
import numpy as np
from keras.models import load_model
import requests
import json
from constants.Birds_labels import lab

model = load_model('./Model/Birdy.h5',compile=False)
def display_bird_info(bird):
    st.write(f"{bird['description']}")
    st.write(f"**Habitat:** {bird['habitat']}")
    st.write(f"**Migratory Patterns:** {bird['migratory_patterns']}")
    st.write(f"**Diet:** {bird['diet']}")
    st.write(f"**Size:** {bird['size']}")
    st.write(f"**Coloration:** {bird['coloration']}")

def processed_img(img_path):
    img=load_img(img_path,target_size=(224,224,3))
    img=img_to_array(img)
    img=img/255
    img=np.expand_dims(img,[0])
    answer=model.predict(img)
    y_class = answer.argmax(axis=-1)
    y = " ".join(str(x) for x in y_class)
    y = int(y)
    result = lab[y]
    st.success("Predicted Bird is: "+result)
    bird_res = requests.get(f'http://localhost:5000/bird/{y}')
    response = json.loads(bird_res.text)
    display_bird_info(response)

def run():
    img1 = Image.open('./meta/Birdy_logo.png')
    img1 = img1.resize((350,350))
    st.image(img1,use_column_width=False)
    st.title("Birds Species Classification")
    st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>* Data is based "BIRDS 525 SPECIES- IMAGE CLASSIFICATION"</h4>''',
                unsafe_allow_html=True)

    img_file = st.file_uploader("Choose an Image of Bird", type=["jpg", "png"])
    if img_file is not None:
        st.image(img_file,use_column_width=False)
        save_image_path = './upload_images/'+img_file.name
        with open(save_image_path, "wb") as f:
            f.write(img_file.getbuffer())

        if st.button("Predict"):
            processed_img(save_image_path)
            
run()