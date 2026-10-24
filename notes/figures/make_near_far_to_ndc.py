from PIL import Image, ImageDraw, ImageFont

S = 2
W, H = 1200, 600

BG = (255, 255, 255)
BLUE = (46, 117, 182)
DARK = (31, 56, 100)
ORANGE = (197, 90, 17)
GRAY = (120, 120, 120)
LIGHT = (217, 226, 243)
LIGHT_ORANGE = (252, 228, 214)

def sc(v):
    return int(round(v * S))

def P(x, y):
    return (sc(x), sc(y))

def line(d, p0, p1, color=BLUE, width=3):
    d.line([P(*p0), P(*p1)], fill=color, width=sc(width))

def dash_line(d, p0, p1, color=GRAY, width=2, dash=8, gap=6):
    x0, y0 = p0
    x1, y1 = p1
    dx, dy = x1 - x0, y1 - y0
    length = (dx * dx + dy * dy) ** 0.5
    if length == 0:
        return
    ux, uy = dx / length, dy / length
    t = 0.0
    while t < length:
        a = (x0 + ux * t, y0 + uy * t)
        b = (x0 + ux * min(t + dash, length), y0 + uy * min(t + dash, length))
        d.line([P(*a), P(*b)], fill=color, width=sc(width))
        t += dash + gap

def arrow(d, p0, p1, color=BLUE, width=3, head=12):
    line(d, p0, p1, color, width)
    x0, y0 = p0
    x1, y1 = p1
    dx, dy = x1 - x0, y1 - y0
    length = (dx * dx + dy * dy) ** 0.5
    if length == 0:
        return
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    bx, by = x1 - ux * head, y1 - uy * head
    pts = [P(x1, y1), P(bx + px * head * 0.45, by + py * head * 0.45),
           P(bx - px * head * 0.45, by - py * head * 0.45)]
    d.polygon(pts, fill=color)

def text(d, xy, s, size=22, color=DARK, anchor="mm", bold=False):
    path = r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc"
    font = ImageFont.truetype(path, sc(size), index=0)
    d.text(P(*xy), s, font=font, fill=color, anchor=anchor,
           stroke_width=sc(2), stroke_fill=BG)

def square(d, cx, cy, size, fill, outline, width=3):
    half = size / 2
    d.rectangle([sc(cx - half), sc(cy - half), sc(cx + half), sc(cy + half)],
                fill=fill, outline=outline, width=sc(width))

img = Image.new("RGB", (W * S, H * S), BG)
d = ImageDraw.Draw(img)

# 左：世界空间
text(d, (290, 45), "世界空间：视锥的两个截面", 24, DARK, bold=True)

# 近平面（小）
square(d, 290, 190, 150, LIGHT, BLUE)
text(d, (290, 100), "近平面", 22, DARK, bold=True)
text(d, (290, 124), "z = -n", 20, GRAY)

# 远平面（大）
square(d, 290, 445, 240, LIGHT, BLUE)
text(d, (290, 283), "远平面", 22, DARK, bold=True)
text(d, (290, 308), "z = -f", 20, GRAY)

# 右：NDC 空间
text(d, (900, 45), "NDC 空间：立方体的前后两个面", 24, DARK, bold=True)

# 前面 z=-1
square(d, 900, 190, 200, LIGHT_ORANGE, ORANGE)
text(d, (900, 100), "前面", 22, DARK, bold=True)
text(d, (900, 124), "z_ndc = -1", 20, GRAY)

# 后面 z=+1
square(d, 900, 430, 200, LIGHT_ORANGE, ORANGE)
text(d, (900, 340), "后面", 22, DARK, bold=True)
text(d, (900, 364), "z_ndc = +1", 20, GRAY)

# 箭头：近 -> 前面
arrow(d, (365, 190), (800, 190), BLUE, 3, 14)
text(d, (580, 165), "x,y 都映射到 [-1,1]", 20, BLUE)

# 箭头：远 -> 后面
arrow(d, (410, 445), (800, 445), BLUE, 3, 14)
text(d, (600, 420), "远平面更大，被挤压到同样大小", 20, BLUE)

# 说明
text(d, (600, 580), "两个面都是 [-1,1] × [-1,1]；区别只在 z_ndc：-1 和 +1", 22, DARK, bold=True)

img = img.resize((W, H), Image.LANCZOS)
img.save("notes/figures/near_far_to_ndc.png")
print("saved notes/figures/near_far_to_ndc.png")
