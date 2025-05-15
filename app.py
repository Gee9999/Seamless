import streamlit as st
from PIL import Image
import numpy as np
import io

def patch_blend_tile(img: Image.Image, blend_width=50) -> Image.Image:
    img = img.convert("RGB")
    arr = np.array(img)
    h, w, c = arr.shape

    # Offset the image so seams are in the center
    rolled = np.roll(arr, shift=(h//2, w//2), axis=(0, 1))

    # Blend horizontal seam
    for i in range(-blend_width, blend_width):
        alpha = 0.5 + 0.5 * (i / blend_width)
        if 0 <= (h//2 + i) < h and 0 <= (h//2 + i - 1) < h:
            rolled[h//2 + i, :, :] = (
                alpha * rolled[h//2 + i, :, :] +
                (1 - alpha) * rolled[h//2 + i - 1, :, :]
            ).astype(np.uint8)

    # Blend vertical seam
    for i in range(-blend_width, blend_width):
        alpha = 0.5 + 0.5 * (i / blend_width)
        if 0 <= (w//2 + i) < w and 0 <= (w//2 + i - 1) < w:
            rolled[:, w//2 + i, :] = (
                alpha * rolled[:, w//2 + i, :] +
                (1 - alpha) * rolled[:, w//2 + i - 1, :]
            ).astype(np.uint8)

    return Image.fromarray(rolled)

# Streamlit UI
st.set_page_config(page_title="Patch Seamless Tile Generator", layout="centered")
st.title("🧵 Patch Seamless Tile Generator (No Mirror, No FFT)")
st.markdown("""Upload a photo and get a grid-perfect seamless tile with patch blending —
great for natural textures, florals, and wallpapers.""")

uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)

    with st.spinner("Stitching your tile..."):
        seamless_tile = patch_blend_tile(image)

    st.success("Perfectly stitched tile ready!")
    st.image(seamless_tile, caption="Seamless Tile Preview", use_column_width=True)

    buf = io.BytesIO()
    seamless_tile.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="📥 Download Seamless Tile",
        data=byte_im,
        file_name="patch_seamless_tile.png",
        mime="image/png"
    )
