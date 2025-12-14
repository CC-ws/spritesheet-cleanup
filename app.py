import gradio as gr
import cv2
import numpy as np
from spritesheet_cleanup import process_spritesheet
import os

def cleanup_sprite(image):
    # image 是 numpy array (H, W, C)
    if image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = list(process_spritesheet(image, no_segment=False, sample_center_pct=60))
    if not results:
        return None
    # 取第一个结果（假设单图）
    clean = results[0].image
    if clean.shape[2] == 4:
        clean = cv2.cvtColor(clean, cv2.COLOR_BGRA2RGBA)
    else:
        clean = cv2.cvtColor(clean, cv2.COLOR_BGR2RGB)
    return clean

gr.Interface(
    fn=cleanup_sprite,
    inputs=gr.Image(type="numpy", label="上传像素图（可能模糊/有抗锯齿）"),
    outputs=gr.Image(type="numpy", label="清理后的像素图"),
    title="SpriteSheet Cleanup Online",
    description="自动去除抗锯齿、对齐像素网格、还原干净 sprite"
).launch()
