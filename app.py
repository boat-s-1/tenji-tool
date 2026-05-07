import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# 白背景画像
img = Image.new("RGB", (1080, 1920), "white")

draw = ImageDraw.Draw(img)

# フォント
font = ImageFont.load_default()

# テキスト
draw.text(
    (100, 100),
    "TEST",
    fill="black",
    font=font
)

# Streamlit表示
st.image(img)

print("完了")
