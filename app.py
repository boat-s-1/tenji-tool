from PIL import Image, ImageDraw, ImageFont

# 白背景作成
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

# 保存
img.save("output.jpg")

print("完了")
