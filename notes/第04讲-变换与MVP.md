# 第 04 讲：变换（模型、视图、投影）

这一讲只解决一件事：**一个三维物体，怎么一步步变成屏幕上的像素坐标。**

整条链路：

\[
\mathbf{p}_{screen}
\sim
\text{viewport}
\cdot
\underbrace{P}_{\text{投影}}
\cdot
\underbrace{V}_{\text{视图}}
\cdot
\underbrace{M}_{\text{模型}}
\cdot
\mathbf{p}_{local}
\]

本讲负责 \(M\)、\(V\)、\(P\) 三个矩阵；viewport 那一步由光栅器的 `draw()` 代劳。

---

## 1. 三维变换：4×4 齐次矩阵

二维用 3×3，三维用 4×4，道理一样：多出来的一维让平移也能写成矩阵乘法。

点 \((x,y,z,1)\)，向量 \((x,y,z,0)\)。

### 缩放

\[
S(s_x,s_y,s_z)=
\begin{bmatrix}
s_x&0&0&0\\
0&s_y&0&0\\
0&0&s_z&0\\
0&0&0&1
\end{bmatrix}
\]

### 平移

\[
T(t_x,t_y,t_z)=
\begin{bmatrix}
1&0&0&t_x\\
0&1&0&t_y\\
0&0&1&t_z\\
0&0&0&1
\end{bmatrix}
\]

### 绕坐标轴旋转

绕 \(x\) 轴：

\[
R_x(\alpha)=
\begin{bmatrix}
1&0&0&0\\
0&\cos\alpha&-\sin\alpha&0\\
0&\sin\alpha&\cos\alpha&0\\
0&0&0&1
\end{bmatrix}
\]

绕 \(y\) 轴：

\[
R_y(\alpha)=
\begin{bmatrix}
\cos\alpha&0&\sin\alpha&0\\
0&1&0&0\\
-\sin\alpha&0&\cos\alpha&0\\
0&0&0&1
\end{bmatrix}
\]

绕 \(z\) 轴：

\[
R_z(\alpha)=
\begin{bmatrix}
\cos\alpha&-\sin\alpha&0&0\\
\sin\alpha&\cos\alpha&0&0\\
0&0&1&0\\
0&0&0&1
\end{bmatrix}
\]

作业 1 的基础题就是 \(R_z\)。角度用弧度。

### 绕任意轴旋转：Rodrigues 公式

轴 \(\mathbf{n}=(n_x,n_y,n_z)\)，先归一化，角度 \(\alpha\)：

\[
R(\mathbf{n},\alpha)=
\cos\alpha\, I
+(1-\cos\alpha)\,\mathbf{n}\mathbf{n}^T
+\sin\alpha\,[\mathbf{n}]_\times
\]

其中

\[
[\mathbf{n}]_\times=
\begin{bmatrix}
0&-n_z&n_y\\
n_z&0&-n_x\\
-n_y&n_x&0
\end{bmatrix}
\]

这是作业 1 的提高题。先别急，基础题过掉再写。

---

## 2. MVP 分别干什么

| 矩阵 | 作用 | 坐标系变化 |
| --- | --- | --- |
| \(M\) 模型 | 把物体从自己的局部坐标摆到世界 | local → world |
| \(V\) 视图 | 把相机移到原点、看向 \(-z\) | world → camera |
| \(P\) 投影 | 把视锥/盒子压到 \([-1,1]^3\) | camera → NDC |

最后 viewport 把 NDC 的 \([-1,1]^2\) 映射到屏幕像素，深度映射到 \([0,1]\) 或深度缓冲区间。

矩阵乘法顺序：**右边的先作用**。所以是 \(P\cdot V\cdot M\cdot p\)，不是 \(M\cdot V\cdot P\cdot p\)。

---

## 3. 视图变换 \(V\)

作业 1 里相机在 \((0,0,5)\)，看向 \(-z\)，上方向 \(+y\)。把相机移到原点，世界就整体平移 \(-\text{eye}\)：

\[
V=
\begin{bmatrix}
1&0&0&-5\\
0&1&0&0\\
0&0&1&0\\
0&0&0&1
\end{bmatrix}
\]

框架里的 `get_view_matrix` 已经写好，不用改。

更一般的情况：相机在 `eye`，看向 `center`，上方向 `up`：

\[
\mathbf f=\text{normalize}(\text{center}-\text{eye}),\quad
\mathbf s=\text{normalize}(\mathbf f\times\mathbf{up}),\quad
\mathbf u=\mathbf s\times\mathbf f
\]

\[
R_{view}=
\begin{bmatrix}
s_x&s_y&s_z&0\\
u_x&u_y&u_z&0\\
-f_x&-f_y&-f_z&0\\
0&0&0&1
\end{bmatrix},
\qquad
V=R_{view}\cdot T(-\text{eye})
\]

作业 1 的相机正好看向 \(-z\)，所以 \(R_{view}=I\)，只剩平移。

---

## 4. 正交投影

把轴对齐盒子 \([l,r]\times[b,t]\times[-n,-f]\) 映射到 \([-1,1]^3\)。

两步：

1. 把盒子中心平移到原点；
2. 把每个方向的长度缩放到 2。

\[
M_{ortho}=S\cdot T
\]

\[
S=
\begin{bmatrix}
\frac{2}{r-l}&0&0&0\\
0&\frac{2}{t-b}&0&0\\
0&0&\frac{2}{n-f}&0\\
0&0&0&1
\end{bmatrix},
\qquad
T=
\begin{bmatrix}
1&0&0&-\frac{l+r}{2}\\
0&1&0&-\frac{b+t}{2}\\
0&0&1&-\frac{n+f}{2}\\
0&0&0&1
\end{bmatrix}
\]

注意 \(z\) 的缩放分母是 \(n-f\)（负数），因为相机看向 \(-z\)，近平面在 \(z=-n\)，远平面在 \(z=-f\)。代入 \(z=-n\) 得 \(-1\)，代入 \(z=-f\) 得 \(+1\)。

---

## 5. 透视投影

### 5.1 视锥

相机在原点，看向 \(-z\)。近平面 \(z=-n\)，远平面 \(z=-f\)。垂直视场角 `fov`：

\[
t=n\tan\frac{\text{fov}}{2},\qquad r=t\cdot\text{aspect},\qquad l=-r,\qquad b=-t
\]

### 5.2 相似三角形

在深度 \(z\)（\(z<0\)）处，可见的 \(x\) 范围是近平面的一半宽度按 \((-z)/n\) 放大：

\[
\frac{x_{\text{visible}}}{r}=\frac{-z}{n}
\]

所以把 \(x\) 压到 \([-1,1]\)：

\[
x_{ndc}=\frac{n}{r}\cdot\frac{x}{-z}
\]

同理

\[
y_{ndc}=\frac{n}{t}\cdot\frac{y}{-z}
\]

这个除以 \((-z)\) 就是**透视除法**，也是“近大远小”的来源。

### 5.3 投影矩阵

用齐次坐标把除法藏进 \(w\)：

\[
P=
\begin{bmatrix}
\frac{n}{r}&0&0&0\\
0&\frac{n}{t}&0&0\\
0&0&A&B\\
0&0&-1&0
\end{bmatrix}
\]

这样

\[
P\begin{bmatrix}x\\y\\z\\1\end{bmatrix}
=
\begin{bmatrix}
\frac{n}{r}x\\
\frac{n}{t}y\\
Az+B\\
-z
\end{bmatrix}
\]

除以 \(w=-z\) 就得到上面的 \(x_{ndc},y_{ndc}\)。最后一行必须是 \((0,0,-1,0)\)：相机看向 \(-z\)，\(w=-z>0\)。

### 5.4 求 \(A,B\)

要求近平面映射到 \(z_{ndc}=-1\)，远平面映射到 \(z_{ndc}=+1\)：

\[
\frac{A(-n)+B}{n}=-1,
\qquad
\frac{A(-f)+B}{f}=+1
\]

解得

\[
A=\frac{n+f}{n-f},
\qquad
B=\frac{2nf}{n-f}
\]

所以

\[
P=
\begin{bmatrix}
\frac{n}{r}&0&0&0\\
0&\frac{n}{t}&0&0\\
0&0&\frac{n+f}{n-f}&\frac{2nf}{n-f}\\
0&0&-1&0
\end{bmatrix}
\]

验算：

- \(z=-n\)：分子 \(-\frac{n(n+f)}{n-f}+\frac{2nf}{n-f}=\frac{n(f-n)}{n-f}=-n\)，除以 \(n\) 得 \(-1\)。
- \(z=-f\)：分子 \(-\frac{f(n+f)}{n-f}+\frac{2nf}{n-f}=\frac{f(n-f)}{n-f}=f\)，除以 \(f\) 得 \(+1\)。

### 5.5 和课件“挤压 + 正交”的关系

课件把透视拆成两步：先把视锥“挤”成盒子，再做正交投影。两种写法等价，但符号约定容易混。上面这个单矩阵是直接按 NDC 定义推的，作业 1 用它最省事，也不会出现“三角形上下颠倒”的问题。

---

## 6. 作业 1 要写什么

`hw/hw1/main.cpp` 里只有两个 TODO：

1. `get_model_matrix(float rotation_angle)`：返回 \(R_z\) 的 4×4 形式。
2. `get_projection_matrix(float eye_fov, float aspect_ratio, float zNear, float zFar)`：返回上面的 \(P\)。

`get_view_matrix` 已经写好。

### 检查清单

- 角度转弧度：`rad = angle / 180.0f * PI`。
- `fov` 也要转弧度，再取一半：`t = n * tan(fov / 2)`。
- `zNear`、`zFar` 是正的距离（0.1、50），不是坐标；坐标是 \(-n\)、\(-f\)。
- 矩阵 \(P\) 的 `(3,2)` 是 \(-1\)，不是 \(+1\)。
- Eigen 的 `<<` 按行填；用 `Matrix4f::Zero()` 再逐项赋值更不容易错。
- 乘法顺序：`projection * view * model`（框架的 `draw()` 已经这么写）。

### 验收

```bat
build.cmd hw1
run.cmd hw1 -r 0  hw1_0.png
run.cmd hw1 -r 45 hw1_45.png
run.cmd hw1 -r 90 hw1_90.png
```

三角形顶点（模型空间）：\((2,0,-2)\)、\((0,2,-2)\)、\((-2,0,-2)\)；相机 \((0,0,5)\)，fov 45°，aspect 1，near 0.1，far 50。

0° 时的像素位置（700×700，图像坐标 y 向下）：

| 顶点 | NDC | 像素 |
| --- | --- | --- |
| \((2,0,-2)\) | \((0.6897,\ 0)\) | \((591,\ 349)\) |
| \((0,2,-2)\) | \((0,\ 0.6897)\) | \((350,\ 108)\) |
| \((-2,0,-2)\) | \((-0.6897,\ 0)\) | \((109,\ 349)\) |

也就是：底边从 \(x\approx109\) 到 \(591\)，在 \(y\approx349\)；顶点在 \((350,108)\)。如果你的图上下颠倒，检查 \(w\) 的符号和 \(z\) 的映射；如果整体太小/太大，检查 `fov` 是否转成了弧度、`aspect` 是否用对。

### 常见错误

| 现象 | 可能原因 |
| --- | --- |
| 全黑 | 投影矩阵把 \(w\) 弄成负数，或者三角形被裁掉；打印 MVP 后的 \(w\) 看看 |
| 三角形上下颠倒 | \(z\) 的符号约定和 \(w\) 行不匹配；用本文的 \(P\) 不会出现 |
| 三角形比预期大很多 | `fov` 忘了转弧度（45 弧度） |
| 旋转方向反了 | \(R_z\) 的 \(\sin\) 符号；图像 y 向下，屏幕上看是反的，正常 |
| 编译过但运行崩 | OpenCV 找不到 Qt 插件；用命令行模式 `run.cmd hw1 -r 0 out.png`，不要开 `imshow` |

### 数值自检

在 `get_projection_matrix` 里临时打印：

```cpp
Eigen::Vector4f p = P * Eigen::Vector4f(0, 2, -7, 1);
std::cout << p.transpose() << " -> " << (p / p.w()).transpose() << std::endl;
```

对 \((0,2,-7,1)\)，期望 \(y_{ndc}=0.6897\)，\(z_{ndc}\approx0.974\)。

---

## 7. 提高题：绕任意轴旋转

基础题通过后再做。把 `get_model_matrix` 换成 Rodrigues：

1. 归一化轴 \(\mathbf n\)；
2. 算 \(R=\cos\alpha I+(1-\cos\alpha)\mathbf n\mathbf n^T+\sin\alpha[\mathbf n]_\times\)；
3. 填进 4×4 的左上角 3×3。

在 `main()` 里把 `get_model_matrix(angle)` 换成 `get_rotation(axis, angle)`，轴取 \((1,1,0)\)，转 45°，观察三角形绕斜轴翻转。

注意事项：

- 归一化是 \(\sqrt{n_x^2+n_y^2+n_z^2}\)，别抄错成 \(n_z+n_z\)。
- 先归一化再算 \(\mathbf n\mathbf n^T\)。
- 4×4 的平移列保持 0，最后一行 \((0,0,0,1)\)。

---

## 8. 自测题

1. 为什么透视投影矩阵的第四行是 \((0,0,-1,0)\)？如果写成 \((0,0,1,0)\) 会怎样？
2. 近平面和远平面分别映射到 NDC 的什么位置？为什么 \(z\) 的缩放分母是 \(n-f\) 而不是 \(f-n\)？
3. 如果 `aspect_ratio` 从 1 变成 2，三角形会变宽还是变窄？用公式解释。
4. 为什么矩阵顺序是 \(P\cdot V\cdot M\)？把顺序换成 \(M\cdot V\cdot P\) 几何上发生了什么？
5. 正交投影和透视投影的本质区别是什么？为什么正交投影不需要除以 \(w\)？
