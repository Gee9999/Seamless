import streamlit as st
from PIL import Image
import numpy as np
import io

def create_mirrored_tile(img: Image.Image) -> Image.Image:
    img = img.convert("RGB")
    w, h = img.size

    # Create 2x2 grid with mirrored edges
    left_top = img
    right_top = img.transpose(Image.FLIP_LEFT_RIGHT)
    left_bottom = img.transpose(Image.FLIP_TOP_BOTTOM)
    right_bottom = img.transpose(Image.ROTATE_180)

    new_img = Image.new("RGB", (w * 2, h * 2))
    new_img.paste(left_top, (0, 0))
    new_img.paste(right_top, (w, 0))
    new_img.paste(left_bottom, (0, h))
    new_img.paste(right_bottom, (w, h))

    # Crop to center
    center_crop = new_img.crop((w // 2, h // 2, w + w // 2, h + h // 2))
    return center_crop

# Streamlit UI
st.set_page_config(page_title="Mirrored Seamless Tile Generator", layout="centered")
st.title("🪞 Mirrored Seamless Tile Generator")
st.markdown("Upload an image to generate a truly seamless tile using edge mirroring.")

uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)

    with st.spinner("Creating seamless tile..."):
        seamless_tile = create_mirrored_tile(image)

    st.success("Seamless tile created!")
    st.image(seamless_tile, caption="Mirrored Seamless Tile Preview", use_column_width=True)

    buf = io.BytesIO()
    seamless_tile.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="📥 Download Seamless Tile",
        data=byte_im,
        file_name="mirrored_seamless_tile.png",
        mime="image/png"
    )
