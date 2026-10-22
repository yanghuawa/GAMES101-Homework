# GAMES101 作业与笔记

课程：[GAMES101-现代计算机图形学入门-闫令琪](https://www.bilibili.com/video/BV1X7411F744)
参考仓库：[DrFlower/GAMES_101_202_Homework](https://github.com/DrFlower/GAMES_101_202_Homework)

这个仓库是我自己的学习记录：22 讲笔记 + 作业 0–8。参考仓库（含完整答案）只放在 `_ref/` 里对照，**不提交**。

## 目录

```
games101/
├─ README.md
├─ build.cmd          # 一键构建某个作业
├─ run.cmd            # 一键运行某个作业
├─ notes/             # 课程大纲、学习计划、每讲笔记
├─ hw/
│  ├─ hw0/            # 作业 0：齐次坐标与二维变换
│  └─ hw1/            # 作业 1：旋转与投影
├─ build/             # CMake 构建产物（忽略）
└─ _ref/              # 参考仓库，含答案（忽略）
```

## 环境

| 组件 | 版本 / 位置 |
| --- | --- |
| 编译器 | g++ 16.2.0（MSYS2 mingw64） |
| CMake | 4.4.4（`C:\msys64\mingw64\bin\cmake.exe`） |
| Eigen | 5.0.1（`C:\msys64\mingw64\include\eigen3`） |
| OpenCV | 5.0.0（`C:\msys64\mingw64`） |
| Git | 2.54.0 |

注意：

- OpenCV 5 的头文件在 `include\opencv5`，CMake 的 `find_package(OpenCV)` 会自动设置 include 路径，不要手写 `opencv4`。
- `cv::imshow` 需要 Qt6 平台插件；作业截图用命令行模式（只 `imwrite`，不开窗口）最稳。
- 本机 Git 的 schannel 后端在此环境下会报 `SEC_E_NO_CREDENTIALS`，已把 `http.sslBackend` 全局设为 `openssl`；换机器时需要重新设置。

## 构建 / 运行

```bat
build.cmd hw0
run.cmd hw0

build.cmd hw1
run.cmd hw1 -r 0  hw1_0.png
run.cmd hw1 -r 45 hw1_45.png
run.cmd hw1 -r 90 hw1_90.png
```

`run.cmd` 会先 `cd` 到 `hw\hwN` 再启动，所以生成的 png 就在作业目录里。

## 进度

| 作业 | 内容 | 课程 | 状态 |
| --- | --- | --- | --- |
| hw0 | 齐次坐标：旋转 45° + 平移 (1,2) | 2–3 | ⬜ |
| hw1 | 旋转与投影矩阵 | 4 | ⬜ |
| hw2 | 三角形光栅化与 Z-buffer | 5–6 | ⬜ |
| hw3 | 管线、Blinn-Phong、纹理 | 7–8 | ⬜ |
| hw4 | Bézier 曲线 | 11 | ⬜ |
| hw5 | 光线与三角形求交 | 13 | ⬜ |
| hw6 | BVH 加速结构 | 14 | ⬜ |
| hw7 | 路径追踪 | 16 | ⬜ |
| hw8 | 质点弹簧系统 | 21 | ⬜ |

## 提交到 GitHub

远端：<https://github.com/yanghuawa/GAMES101-Homework>

每完成一次作业：

```bash
git add hw/hw1 notes/
git commit -m "hw1: 实现旋转与投影，附 0/45/90 度截图"
git push
```

约定：

- 一次作业一个 commit，message 用 `hwN: ...`。
- `_ref/` 是参考仓库（含答案），已在 `.gitignore` 中；不要 `git add -f`。
- 截图放在对应 `hw/hwN/` 下一起提交。

## 对框架做的小修正

从参考仓库复制 hw1 框架时改了两处（不影响作业本身）：

1. `rasterizer.cpp` 的 `set_pixel` / `get_index` 用 `height - 1 - y`，避免 y = 0 时越界。
2. `draw()` 里连续三次 `setVertex` 合并为一次。

## 学习方式

每讲固定节奏：**讲原理 → 手推一遍 → 写代码 → 跑图验收 → 记笔记**。
笔记在 `notes/`，作业在 `hw/`，两者都进 Git。
