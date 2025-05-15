import streamlit as st
from PIL import Image
import numpy as np
import io

def fft_seamless_tile(img: Image.Image, border_width=32) -> Image.Image:
    img = img.convert("RGB")
    arr = np.array(img)
    h, w, c = arr.shape

    # Pad with wrap to make edges tileable
    padded = np.pad(arr, ((0, border_width), (0, border_width), (0, 0)), mode='wrap')

    # Apply a linear blend to smooth the seams
    blend = np.linspace(0, 1, border_width).reshape(1, -1, 1)
    for i in range(border_width):
        alpha = i / border_width
        padded[-border_width + i, :, :] = (1 - alpha) * padded[-border_width + i, :, :] + alpha * padded[i, :, :]
        padded[:, -border_width + i, :] = (1 - alpha) * padded[:, -border_width + i, :] + alpha * padded[:, i, :]

    # Crop to original size
    seamless = padded[:h, :w, :]
    return Image.fromarray(seamless.astype(np.uint8))

# Streamlit UI
st.set_page_config(page_title="True Seamless Tile Generator", layout="centered")
st.title("🎨 True Seamless Tile Generator (Tapestry Style)")
st.markdown("Upload a floral or texture image and get a perfectly seamless tile — no mirrors, just flow.")

uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)

    with st.spinner("Generating seamless tile..."):
        seamless_tile = fft_seamless_tile(image)

    st.success("Seamless tile ready!")
    st.image(seamless_tile, caption="Seamless Tapestry Tile Preview", use_column_width=True)

    buf = io.BytesIO()
    seamless_tile.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="📥 Download Seamless Tile",
        data=byte_im,
        file_name="true_seamless_tile.png",
        mime="image/png"
    )
