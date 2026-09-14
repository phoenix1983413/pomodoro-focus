#!/usr/bin/env python3
"""
番茄工作钟 · PWA 图标生成器
- 192x192 (manifest)
- 512x512 (manifest)
- 180x180 (apple-touch-icon)
- 64x64  (favicon)
"""
from PIL import Image, ImageDraw, ImageFilter
import math, os

OUT = os.path.dirname(os.path.abspath(__file__))
SIZES = {
    "icon-192.png": 192,
    "icon-512.png": 512,
    "apple-touch-icon.png": 180,
    "favicon-64.png": 64,
}

# 设计——将整个图标面视为 1024² 坐标系，方便缩放
def render(size: int) -> Image.Image:
    S = size
    # 1024 坐标 -> size 坐标
    k = S / 1024.0

    def s(x): return int(round(x * k))

    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # ---- 圆角矩形背景（深色，带微渐变感） ----
    pad = s(56)            # 离开边缘的安全距离（maskable 要求 ~10%）
    box = (pad, pad, S - pad, S - pad)
    radius = s(220)
    # 第一层：稍亮的底色，制造轻微立体感
    d.rounded_rectangle(box, radius=radius, fill=(45, 45, 48, 255))
    # 在其上画一个稍小的圆，让边有"凹槽"光感
    inner_pad = s(72)
    inner_box = (inner_pad, inner_pad, S - inner_pad, S - inner_pad)
    d.rounded_rectangle(inner_box, radius=radius - s(16), fill=(29, 29, 31, 255))

    # ---- 进度环（70%，accent 色 #2997FF） ----
    cx, cy = S // 2, S // 2
    r_outer = s(330)
    r_track = s(354)
    ring_w = s(36)

    # 底环（灰）
    d.arc((cx - r_track, cy - r_track, cx + r_track, cy + r_track),
          start=0, end=360, fill=(80, 80, 84, 200), width=ring_w)
    # 主环（70%，从 -90 度开始）
    sweep = int(360 * 0.70)
    d.arc((cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer),
          start=-90, end=-90 + sweep, fill=(41, 151, 255, 255), width=ring_w)

    # 进度终点的小圆点
    end_angle = math.radians(-90 + sweep)
    ex = cx + r_outer * math.cos(end_angle)
    ey = cy + r_outer * math.sin(end_angle)
    d.ellipse((ex - ring_w//2 - s(6), ey - ring_w//2 - s(6),
               ex + ring_w//2 + s(6), ey + ring_w//2 + s(6)),
              fill=(255, 255, 255, 255))

    # ---- 番茄（中央球体，红色） ----
    tomato_r = s(178)
    # 阴影层（垂直下沉，保证番茄视觉居中）
    sh_y = s(30)
    shadow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse((cx - tomato_r, cy - tomato_r + sh_y,
                cx + tomato_r, cy + tomato_r + sh_y),
               fill=(0, 0, 0, 80))
    shadow = shadow.filter(ImageFilter.GaussianBlur(s(26)))
    img.alpha_composite(shadow)

    # 主体（用一个简单的双圆叠加模拟球体光感）
    tx0, ty0, tx1, ty1 = cx - tomato_r, cy - tomato_r, cx + tomato_r, cy + tomato_r
    d.ellipse((tx0, ty0, tx1, ty1), fill=(231, 76, 60, 255))         # 主体红
    # 高光（偏左上）
    hl_r = tomato_r // 2
    hx, hy = cx - tomato_r // 3, cy - tomato_r // 3
    d.ellipse((hx - hl_r, hy - hl_r, hx + hl_r, hy + hl_r), fill=(241, 110, 95, 255))
    # 高光小白点
    sp_r = tomato_r // 8
    sx, sy = hx - hl_r // 2, hy - hl_r // 2
    d.ellipse((sx - sp_r, sy - sp_r, sx + sp_r, sy + sp_r), fill=(255, 255, 255, 230))

    # ---- 顶部绿色蒂 ----
    leaf_w = s(150)
    leaf_h = s(40)
    leaf_box = (cx - leaf_w // 2, cy - tomato_r - leaf_h + s(20),
                cx + leaf_w // 2, cy - tomato_r + s(40))
    d.rounded_rectangle(leaf_box, radius=s(28), fill=(52, 199, 89, 255))
    # 小茎
    stem_w = s(18)
    stem_h = s(50)
    stem_box = (cx - stem_w // 2, cy - tomato_r - stem_h + s(8),
                cx + stem_w // 2, cy - tomato_r - s(8))
    d.rounded_rectangle(stem_box, radius=s(10), fill=(46, 168, 73, 255))

    return img

if __name__ == "__main__":
    for fname, size in SIZES.items():
        out_path = os.path.join(OUT, fname)
        render(size).save(out_path, "PNG", optimize=True)
        kb = os.path.getsize(out_path) / 1024
        print(f"OK  {fname:28s}  {size}x{size}   {kb:5.1f} KB")
