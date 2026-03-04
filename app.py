import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
from sklearn.cluster import KMeans
import gradio as gr
import tempfile
import os

# ── Core image processing ─────────────────────────────────────────────────────
def kmeans_quantize(image, n_colors):
    img_array = np.array(image.convert("RGB"), dtype=np.float32)
    H, W, _ = img_array.shape
    pixels = img_array.reshape(-1, 3)
    kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init="auto")
    kmeans.fit(pixels)
    compressed = kmeans.cluster_centers_[kmeans.labels_]
    result = compressed.reshape(H, W, 3)
    result = np.clip(result, 0, 255).astype(np.uint8)
    return Image.fromarray(result)

def resize(image, max_size=512):
    w, h = image.size
    if max(w, h) > max_size:
        scale = max_size / max(w, h)
        image = image.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    return image

def cartoon(image):
    if image is None:
        return None, None
    image = resize(image)
    # Pure KMeans color reduction — no blur, no filters, just like the original exercise
    result = kmeans_quantize(image, n_colors=6)
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    result.save(tmp.name)
    return result, tmp.name

def compress(image):
    if image is None:
        return None, None
    image = resize(image)
    result = kmeans_quantize(image, n_colors=64)
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    result.save(tmp.name)
    return result, tmp.name

# ── Custom CSS — Dark theme ───────────────────────────────────────────────────
css = """
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

* { box-sizing: border-box; }

body, .gradio-container {
    background: #0e0e0e !important;
    font-family: 'DM Sans', sans-serif !important;
}

.gradio-container {
    max-width: 980px !important;
    margin: 0 auto !important;
    padding: 0 24px 60px !important;
}

#header {
    text-align: center;
    padding: 52px 0 36px;
}

#header h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 3.4rem !important;
    font-weight: 800 !important;
    letter-spacing: -1.5px;
    color: #ffffff !important;
    margin: 0 0 8px !important;
    line-height: 1.05;
}

#header h1 span { color: #f5c542; }

#header p {
    font-size: 1.05rem;
    color: #666;
    font-weight: 300;
    margin: 0;
}

/* Upload zone */
#upload-col .wrap {
    border: 2px dashed #2a2a2a !important;
    border-radius: 20px !important;
    background: #161616 !important;
    min-height: 320px !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
#upload-col .wrap:hover {
    border-color: #f5c542 !important;
    box-shadow: 0 0 0 4px rgba(245,197,66,0.08) !important;
}

/* Output zone */
#output-col .wrap {
    background: #161616 !important;
    border-radius: 20px !important;
    border: 2px solid #222 !important;
    min-height: 320px !important;
}

/* Action buttons */
#btn-cartoon, #btn-compress {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.3px;
    border-radius: 16px !important;
    height: 62px !important;
    border: none !important;
    cursor: pointer !important;
    transition: transform 0.15s, box-shadow 0.15s, opacity 0.15s !important;
    width: 100% !important;
}

#btn-cartoon {
    background: #f5c542 !important;
    color: #0e0e0e !important;
    box-shadow: 0 4px 20px rgba(245,197,66,0.3) !important;
}

#btn-compress {
    background: #1e1e1e !important;
    color: #ffffff !important;
    border: 2px solid #333 !important;
}

#btn-cartoon:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(245,197,66,0.45) !important;
}
#btn-compress:hover {
    transform: translateY(-2px) !important;
    background: #2a2a2a !important;
}

/* Big download button */
#download-row {
    margin-top: 10px;
}
#download-row button, #download-row a {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    background: #ffffff !important;
    color: #0e0e0e !important;
    border-radius: 16px !important;
    height: 68px !important;
    width: 100% !important;
    border: none !important;
    cursor: pointer !important;
    transition: opacity 0.15s, transform 0.15s !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-decoration: none !important;
    letter-spacing: 0.3px;
}
#download-row button:hover, #download-row a:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}

.section-label {
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #444;
    margin-bottom: 10px;
    padding-left: 2px;
}

footer { display: none !important; }
.built-with { display: none !important; }
"""

# ── UI Layout ─────────────────────────────────────────────────────────────────
with gr.Blocks(css=css, theme=gr.themes.Base()) as demo:

    gr.HTML("""
    <div id="header">
        <h1>PicT<span>Magic</span></h1>
        <p>Change any face to a cartoon or compress any image — in one click.</p>
    </div>
    """)

    with gr.Row(equal_height=True):
        with gr.Column(elem_id="upload-col"):
            gr.HTML('<div class="section-label">Your photo</div>')
            input_image = gr.Image(type="pil", label="", show_label=False)

        with gr.Column(elem_id="output-col"):
            gr.HTML('<div class="section-label">Result</div>')
            output_image = gr.Image(type="pil", label="", show_label=False)

    with gr.Row():
        btn_cartoon = gr.Button("🎨  Cartoon", elem_id="btn-cartoon")
        btn_compress = gr.Button("🗜  Compress", elem_id="btn-compress")

    # Hidden file path state
    file_path = gr.State(value=None)

    with gr.Row(elem_id="download-row", visible=False) as download_row:
        download_btn = gr.DownloadButton("⬇  Download your image", visible=True)

    def run_cartoon(image):
        result, path = cartoon(image)
        return result, path, gr.Row(visible=True), gr.DownloadButton(value=path, visible=True, label="⬇  Download your image")

    def run_compress(image):
        result, path = compress(image)
        return result, path, gr.Row(visible=True), gr.DownloadButton(value=path, visible=True, label="⬇  Download your image")

    btn_cartoon.click(
        fn=run_cartoon,
        inputs=input_image,
        outputs=[output_image, file_path, download_row, download_btn]
    )
    btn_compress.click(
        fn=run_compress,
        inputs=input_image,
        outputs=[output_image, file_path, download_row, download_btn]
    )

if __name__ == "__main__":
    demo.launch()
