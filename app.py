
import streamlit as st
from PIL import Image
import numpy as np
import os

def create_seamless_tile(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    w, h = image.size

    top_left = image.crop((0, 0, w // 2, h // 2))
    top_right = top_left.transpose(Image.FLIP_LEFT_RIGHT)
    bottom_left = top_left.transpose(Image.FLIP_TOP_BOTTOM)
    bottom_right = top_right.transpose(Image.FLIP_TOP_BOTTOM)

    new_img = Image.new("RGBA", (w, h))
    new_img.paste(top_left, (0, 0))
    new_img.paste(top_right, (w // 2, 0))
    new_img.paste(bottom_left, (0, h // 2))
    new_img.paste(bottom_right, (w // 2, h // 2))

    return new_img

st.set_page_config(page_title="Seamless Tile Creator", layout="centered")
st.title("🧱 Seamless Tile Creator")
st.markdown("Upload any image and get a perfectly seamless tile for wallpapers, floors, fabrics, and more.")

uploaded_file = st.file_uploader("Upload an image (PNG or JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)

    with st.spinner("Creating seamless tile..."):
        seamless_tile = create_seamless_tile(image)

    st.image(seamless_tile, caption="Seamless Tile", use_column_width=True)

    output_path = "seamless_tile.png"
    seamless_tile.save(output_path)
    with open(output_path, "rb") as f:
        st.download_button("📥 Download Seamless Tile", f, file_name="seamless_tile.png", mime="image/png")
