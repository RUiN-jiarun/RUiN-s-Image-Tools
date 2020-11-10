# -*- coding: utf-8 -*-
import os
from PIL import Image

DST_PATH = "static/img/res"
WM_PATH = os.path.join("static/img", "watermark.jpg")

def enco(s, w):
    # s为原图，w为水印
    # X & 1100 0000 可以得到X的最高2位
    # X & 1111 1100 可以得到X除最低2位外其他部分
    return int((w & 192) / 85) + (s & 252)


def deco(s):
    # X & 0000 0011 可以得到X的最低2位
    return (s & 3) * 85


def add_watermark(src, watermark=WM_PATH):
    filename = src.split("\\")[-1].split(".")[0]
    path_dst = os.path.join(DST_PATH, filename + "_res.png")

    s_img = Image.open(src).convert("RGB")
    s_p = s_img.load()
    width, height = s_img.size
    w_img = Image.open(watermark)
    w_p = w_img.resize((width, height)).load()
    d_img = Image.new("RGB", (width, height))
    d_p = d_img.load()

    for x in range(width):
        for y in range(height):
            (rw, gw, bw) = w_p[x, y]
            (rs, gs, bs) = s_p[x, y]
            rd = enco(rs, rw)
            gd = enco(gs, gw)
            bd = enco(bs, bw)
            d_p[x, y] = (rd, gd, bd)

    d_img.save(path_dst)

    s_img.close()
    w_img.close()
    d_img.close()


def read_watermark(src):
    filename = src.split("\\")[-1].split(".")[0]
    path_dst = os.path.join(DST_PATH, filename + "_extract.png")

    s_img = Image.open(src)
    s_p = s_img.load()
    w, h = s_img.size

    d_img = Image.new("RGB", (w, h))
    d_p = d_img.load()
    for x in range(w):
        for y in range(h):
            (rs, gs, bs) = s_p[x, y]
            rd = deco(rs)
            gd = deco(gs)
            bd = deco(bs)
            d_p[x, y] = (rd, gd, bd)

    d_img.save(path_dst)

    s_img.close()
    d_img.close()


if __name__ == '__main__':
    # for testing
    result_file = os.path.join(DST_PATH, "kanata_res.png")
    read_watermark(result_file)
