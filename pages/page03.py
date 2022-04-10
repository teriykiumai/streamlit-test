import time

import streamlit as st
from streamlit_cropper import st_cropper
from PIL import Image

# https://openbase.com/python/streamlit-cropper/documentation

def app():
    st.header("Crop a Picture")

    img_file = st.file_uploader(label='Please Upload Picture', type=['png', 'jpg'])

    if img_file:
        img = Image.open(img_file)

        with st.sidebar:
            st.sidebar.title("⚙️ Parameters")
            cc = st.columns(2)
            realtime_update = cc[0].checkbox(label="Update in Real Time", value=True)
            box_color = cc[1].color_picker(label="Box Color", value='#FF0000')
            aspect_choice = st.radio(label="Aspect Ratio", options=["1:1", "16:9", "4:3", "2:3", "Free"])
            aspect_dict = {
                "1:1": (1, 1),
                "16:9": (16, 9),
                "4:3": (4, 3),
                "2:3": (2, 3),
                "Free": None
            }
            aspect_ratio = aspect_dict[aspect_choice]

            # FullHD解像度を最大としてPreviewする
            image_resolution = 1200
            st.subheader("New Image Size")
            thumbnail_size = st.slider("Size [px]", max_value=image_resolution, min_value=0, value=int(image_resolution/2))


        # パラメータ情報を元に画像をクリップする
        if not realtime_update:
            st.warning("ダブルクリックで位置を更新します")

        st.info("赤枠をドラッグして任意の位置に動かします")
        cropped_img = st_cropper(img, realtime_update=realtime_update, box_color=box_color,
                            aspect_ratio=aspect_ratio)       
        # Manipulate cropped image at will
        st.subheader("New Image Preview")
        _ = cropped_img.thumbnail((thumbnail_size, thumbnail_size))
        st.image(cropped_img)
