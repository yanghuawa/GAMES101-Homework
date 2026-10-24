from PIL import Image, ImageDraw, ImageFont

S = 2  # 2x 超采样，最后缩小
W, H = 1200, 600

BG = (255, 255, 255)
BLUE = (46, 117, 182)
DARK = (31, 56, 100)
ORANGE = (197, 90, 17)
GRAY = (120, 120, 120)
LIGHT = (217, 226, 243)

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
    # 垂直方向
    px, py = -uy, ux
    bx, by = x1 - ux * head, y1 - uy * head
    pts = [P(x1, y1), P(bx + px * head * 0.45, by + py * head * 0.45),
           P(bx - px * head * 0.45, by - py * head * 0.45)]
    d.polygon(pts, fill=color)

def double_arrow(d, p0, p1, color=ORANGE, width=3, head=10):
    arrow(d, p0, p1, color, width, head)
    arrow(d, p1, p0, color, width, head)

def text(d, xy, s, size=22, color=DARK, anchor="mm", bold=False):
    # Segoe UI 不含中文字形，统一用微软雅黑
    path = r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc"
    font = ImageFont.truetype(path, sc(size), index=0)
    d.text(P(*xy), s, font=font, fill=color, anchor=anchor,
           stroke_width=sc(2), stroke_fill=BG)

img = Image.new("RGB", (W * S, H * S), BG)
d = ImageDraw.Draw(img)

# ---------------- 左图：侧视图 ----------------
O = (150, 300)
near_x, far_x = 470, 700
near_h = 80
near_top = (near_x, O[1] - near_h)
near_bot = (near_x, O[1] + near_h)

# 视线斜率
slope = (near_top[1] - O[1]) / (near_x - O[0])  # 负
far_top = (far_x, O[1] + slope * (far_x - O[0]))
far_bot = (far_x, O[1] - slope * (far_x - O[0]))

# 中轴
dash_line(d, (O[0] - 10, O[1]), (far_x + 60, O[1]), GRAY, 2)
text(d, (far_x + 85, O[1]), "-z", 22, GRAY)
arrow(d, (far_x + 30, O[1]), (far_x + 70, O[1]), GRAY, 2, 8)

# 两条视线
line(d, O, far_top, BLUE, 3)
line(d, O, far_bot, BLUE, 3)

# 近平面 / 远平面
line(d, near_top, near_bot, DARK, 4)
line(d, far_top, far_bot, GRAY, 3)

# 近平面的一半高度 t
line(d, (near_x, O[1]), near_top, ORANGE, 4)
text(d, (near_x + 18, (O[1] + near_top[1]) / 2), "t", 24, ORANGE, bold=True)

# n：沿中轴画一段橙色，标签压在中轴上（有白色描边）
line(d, (O[0], O[1]), (near_x, O[1]), ORANGE, 2)
text(d, ((O[0] + near_x) / 2, O[1]), "n", 24, ORANGE, bold=True)

# fov/2 圆弧
r = 85
bbox = [sc(O[0] - r), sc(O[1] - r), sc(O[0] + r), sc(O[1] + r)]
d.arc(bbox, start=337, end=360, fill=ORANGE, width=sc(2))
text(d, (O[0] + 95, O[1] - 55), "fov/2", 22, ORANGE)

# 文字标签
text(d, (O[0] - 10, O[1] + 45), "camera (eye)", 20, DARK, anchor="lm")
text(d, (near_x, near_top[1] - 50), "near plane", 22, DARK, bold=True)
text(d, (near_x, near_top[1] - 26), "z = -n", 20, GRAY)
text(d, (far_x, far_top[1] - 45), "far plane", 22, DARK, bold=True)
text(d, (far_x, far_top[1] - 20), "z = -f", 20, GRAY)

# 左图标题
text(d, (450, 70), "1) 侧视图：fov 与近平面高度", 24, DARK, bold=True)

# ---------------- 右图：近平面正面 ----------------
cx, cy = 1000, 300
rw, rh = 150, 100  # 半宽 r，半高 t
L, R = cx - rw, cx + rw
T, B = cy - rh, cy + rh

# 矩形填充
d.rectangle([sc(L), sc(T), sc(R), sc(B)], fill=LIGHT, outline=BLUE, width=sc(3))

# 中轴
dash_line(d, (L - 30, cy), (R + 30, cy), GRAY, 2)
dash_line(d, (cx, T - 30), (cx, B + 30), GRAY, 2)

# x / y 轴
arrow(d, (L - 50, cy), (R + 45, cy), GRAY, 2, 8)
text(d, (R + 60, cy), "x", 20, GRAY)
arrow(d, (cx, B + 45), (cx, T - 40), GRAY, 2, 8)
text(d, (cx, T - 55), "y", 20, GRAY)

# 边界标签
text(d, (R + 18, cy - rh / 2), "r", 24, ORANGE, anchor="lm", bold=True)
text(d, (L - 18, cy - rh / 2), "l = -r", 22, GRAY, anchor="rm")
text(d, (cx + 30, T - 14), "t", 24, ORANGE, anchor="mb", bold=True)
text(d, (cx + 30, B + 14), "b = -t", 22, GRAY, anchor="mt")

# 宽度 / 高度
double_arrow(d, (L, B + 45), (R, B + 45), ORANGE, 2, 8)
text(d, ((L + R) / 2, B + 68), "width = 2r", 20, ORANGE)
double_arrow(d, (R + 55, T), (R + 55, B), ORANGE, 2, 8)
text(d, (R + 80, cy), "2t", 20, ORANGE, anchor="lm")
text(d, (cx, B + 110), "aspect = width / height = r / t", 20, DARK)

# 右图标题
text(d, (1000, 70), "2) 近平面：[-r,r] × [-t,t]", 24, DARK, bold=True)

img = img.resize((W, H), Image.LANCZOS)
img.save("notes/figures/frustum_near_plane.png")
print("saved notes/figures/frustum_near_plane.png")
