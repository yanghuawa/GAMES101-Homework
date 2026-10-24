from PIL import Image, ImageDraw, ImageFont

S = 2
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
    px, py = -uy, ux
    bx, by = x1 - ux * head, y1 - uy * head
    pts = [P(x1, y1), P(bx + px * head * 0.45, by + py * head * 0.45),
           P(bx - px * head * 0.45, by - py * head * 0.45)]
    d.polygon(pts, fill=color)

def double_arrow(d, p0, p1, color=ORANGE, width=2, head=8):
    arrow(d, p0, p1, color, width, head)
    arrow(d, p1, p0, color, width, head)

def text(d, xy, s, size=22, color=DARK, anchor="mm", bold=False):
    path = r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc"
    font = ImageFont.truetype(path, sc(size), index=0)
    d.text(P(*xy), s, font=font, fill=color, anchor=anchor,
           stroke_width=sc(2), stroke_fill=BG)

img = Image.new("RGB", (W * S, H * S), BG)
d = ImageDraw.Draw(img)

# ================= 左图：相似三角形（俯视图） =================
O = (150, 300)
near_x, far_x = 470, 700
r = 60
far_half = r * (far_x - O[0]) / (near_x - O[0])

near_top = (near_x, O[1] - r)
near_bot = (near_x, O[1] + r)
far_top = (far_x, O[1] - far_half)
far_bot = (far_x, O[1] + far_half)

# 中轴
dash_line(d, (O[0] - 10, O[1]), (far_x + 55, O[1]), GRAY, 2)
text(d, (far_x + 80, O[1]), "-z", 22, GRAY)
arrow(d, (far_x + 25, O[1]), (far_x + 65, O[1]), GRAY, 2, 8)

# 视线
line(d, O, far_top, BLUE, 3)
line(d, O, far_bot, BLUE, 3)

# 近平面（整条）
line(d, near_top, near_bot, DARK, 4)
# 远平面（整条）
line(d, far_top, far_bot, GRAY, 3)

# 标出近平面半宽 r（橙色上半段）
line(d, (near_x, O[1]), near_top, ORANGE, 4)
text(d, (near_x + 20, (O[1] + near_top[1]) / 2), "r", 24, ORANGE, anchor="lm", bold=True)

# 标出深度 z 处半宽 x_visible（橙色上半段）
line(d, (far_x, O[1]), far_top, ORANGE, 4)
text(d, (far_x - 15, (O[1] + far_top[1]) / 2), "x_visible", 22, ORANGE, anchor="rm", bold=True)

# 距离标注：n 和 -z
line(d, (O[0], 205), (near_x, 205), GRAY, 2)
line(d, (O[0], 195), (O[0], 215), GRAY, 2)
line(d, (near_x, 195), (near_x, 215), GRAY, 2)
text(d, ((O[0] + near_x) / 2, 185), "n", 22, DARK, bold=True)

line(d, (O[0], 165), (far_x, 165), GRAY, 2)
line(d, (O[0], 155), (O[0], 175), GRAY, 2)
line(d, (far_x, 155), (far_x, 175), GRAY, 2)
text(d, ((O[0] + far_x) / 2, 145), "-z（z < 0）", 22, DARK, bold=True)

# 平面标签
text(d, (near_x, 395), "近平面", 22, DARK, bold=True)
text(d, (near_x, 420), "z = -n", 20, GRAY)
text(d, (far_x, 445), "深度 z 的平面", 22, DARK, bold=True)
text(d, (far_x, 470), "z < 0", 20, GRAY)

# 相机
text(d, (O[0] - 5, 340), "相机 O", 22, DARK, anchor="lm")

# 结论
text(d, (450, 525), "两个直角三角形相似（共享 O 处的角）", 22, DARK, bold=True)
text(d, (450, 555), "x_visible / r = (-z) / n", 22, ORANGE, bold=True)

# 左图标题
text(d, (450, 70), "1) 俯视图：相似三角形", 24, DARK, bold=True)

# ================= 右图：映射到 NDC =================
cx, cy1, cy2 = 1010, 270, 390
half = 120
L, R = cx - half, cx + half

# 空间轴
line(d, (L - 30, cy1), (R + 30, cy1), GRAY, 2)
for x in (L, cx, R):
    line(d, (x, cy1 - 8), (x, cy1 + 8), GRAY, 2)
text(d, (L - 10, cy1 - 35), "-x_visible", 20, DARK, anchor="rm")
text(d, (cx, cy1 - 35), "0", 20, DARK)
text(d, (R + 5, cy1 - 35), "+x_visible", 20, DARK, anchor="rm")

# NDC 轴
line(d, (L - 30, cy2), (R + 30, cy2), GRAY, 2)
for x in (L, cx, R):
    line(d, (x, cy2 - 8), (x, cy2 + 8), GRAY, 2)
text(d, (L - 20, cy2 + 35), "-1", 20, DARK, anchor="rm")
text(d, (cx, cy2 + 35), "0", 20, DARK)
text(d, (R + 25, cy2 + 35), "+1", 20, DARK, anchor="lm")

# 连接线
dash_line(d, (L, cy1), (L, cy2), GRAY, 1)
dash_line(d, (cx, cy1), (cx, cy2), GRAY, 1)
dash_line(d, (R, cy1), (R, cy2), GRAY, 1)

# 一个具体点 x，x_ndc = 0.5
px = cx + half * 0.5
line(d, (px, cy1), (px, cy2), ORANGE, 2)
d.ellipse([sc(px - 5), sc(cy1 - 5), sc(px + 5), sc(cy1 + 5)], fill=ORANGE)
d.ellipse([sc(px - 5), sc(cy2 - 5), sc(px + 5), sc(cy2 + 5)], fill=ORANGE)
text(d, (px, cy1 - 70), "x", 22, ORANGE, anchor="mm", bold=True)
text(d, (px + 10, cy2 + 35), "x_ndc", 20, ORANGE, anchor="lm", bold=True)

# 公式
text(d, (1010, 480), "x_ndc = x / x_visible", 22, DARK, bold=True)
text(d, (1010, 515), "= (n/r) · x / (-z)", 22, DARK, bold=True)
text(d, (1010, 555), "除以 -z 就是透视除法；z 越负，物体越小", 20, GRAY)

# 右图标题
text(d, (1010, 70), "2) 映射到 NDC：[-1, 1]", 24, DARK, bold=True)

img = img.resize((W, H), Image.LANCZOS)
img.save("notes/figures/similar_triangles.png")
print("saved notes/figures/similar_triangles.png")
