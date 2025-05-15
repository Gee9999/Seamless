import streamlit as st
from PIL import Image
import numpy as np
import io

def make_seamless_tile(img: Image.Image, blend_width=20) -> Image.Image:
    img = img.convert("RGB")
    arr = np.array(img)
    h, w, _ = arr.shape

    # Offset image by 50% in both directions
    offset_arr = np.roll(arr, shift=(h // 2, w // 2), axis=(0, 1))

    # Blend vertical seam
    for i in range(-blend_width, blend_width):
        alpha = 0.5 + 0.5 * (i / blend_width)
        offset_arr[:, (w // 2) + i, :] = (
            alpha * offset_arr[:, (w // 2) + i, :] +
            (1 - alpha) * offset_arr[:, (w // 2) + i - 1, :]
        ).astype(np.uint8)

    # Blend horizontal seam
    for i in range(-blend_width, blend_width):
        alpha = 0.5 + 0.5 * (i / blend_width)
        offset_arr[(h // 2) + i, :, :] = (
            alpha * offset_arr[(h // 2) + i, :, :] +
            (1 - alpha) * offset_arr[(h // 2) + i - 1, :, :]
        ).astype(np.uint8)

    return Image.fromarray(offset_arr)

# Streamlit UI
st.set_page_config(page_title="Seamless Tile Generator", layout="centered")
st.title("🧩 Seamless Tile Generator")
st.markdown("Upload an image and generate a seamless tile pattern.")

uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)

    with st.spinner("Creating seamless tile..."):
        seamless_tile = make_seamless_tile(image)

    st.success("Seamless tile created!")
    st.image(seamless_tile, caption="Seamless Tile Preview", use_column_width=True)

    buf = io.BytesIO()
    seamless_tile.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="📥 Download Seamless Tile",
        data=byte_im,
        file_name="seamless_tile.png",
        mime="image/png"
    )
