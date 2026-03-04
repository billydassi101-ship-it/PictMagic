---
title: CartoonifyAI
emoji: 🎨
colorFrom: pink
colorTo: yellow
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---

# 🎨 CartoonifyAI — K-Means Color Reduction

Transform any photo into a cartoon using a K-Means clustering algorithm built from scratch in Python!

## ✨ How it works

Every image is made of millions of colors. This app reduces the image to only **K colors** using the K-Means algorithm:

1. Each pixel (R, G, B) is treated as a data point in 3D color space
2. K-Means groups all pixels into K clusters
3. Each pixel is replaced by the average color of its cluster
4. The result is a simplified, cartoon-like version of the original image

The fewer colors you choose, the stronger the cartoon effect!

## 🚀 Run it locally

**1. Clone the project**
```bash
git clone https://github.com/YOUR_USERNAME/cartoonify-app.git
cd cartoonify-app
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Launch the app**
```bash
python app.py
```

Then open your browser at `http://localhost:7860`

## 🛠️ Tech Stack

- **Python** — core language
- **NumPy** — K-Means algorithm and pixel manipulation
- **Pillow** — image loading and saving
- **Gradio** — web interface

## 💡 Tips

- Try **4 to 12 colors** for the best cartoon effect
- Works best with portraits, landscapes, and high-contrast photos
- Large images are automatically resized to 512px for faster processing

## 👨‍💻 Author

Built with ❤️ by [YOUR NAME]
