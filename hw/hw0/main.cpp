#include <cmath>
#include <eigen3/Eigen/Dense>
#include <iostream>

// 作业 0：把点 P = (2, 1) 先绕原点逆时针旋转 45°，再平移 (1, 2)。
// 要求用齐次坐标完成，手算结果应为 (1.7071, 4.1213)。
//
// 只改 R 和 T 两个矩阵，框架不要动。
//   R：绕 Z 轴逆时针旋转 theta 的 3x3 齐次矩阵
//   T：平移 (1, 2) 的 3x3 齐次矩阵
// M = T * R 已经写好，先想清楚为什么后做的平移在左边，再动手。

int main()
{
    const float PI = std::acos(-1.0f);
    const float theta = 45.0f / 180.0f * PI;

    Eigen::Vector3f p(2.0f, 1.0f, 1.0f); // 齐次坐标 (x, y, 1)

    // TODO 1: 绕 Z 轴逆时针旋转 theta
    Eigen::Matrix3f R = Eigen::Matrix3f::Identity();
    float c = cos(theta);
    float s = sin(theta);
    R << c,-s,0,
         s, c,0,
         0, 0,1;
    


    // TODO 2: 平移 (1, 2)
    Eigen::Matrix3f T = Eigen::Matrix3f::Identity();
    T << 1,0,1,
         0,1,2,
         0,0,1;

    // 组合顺序已经给出：先旋转、后平移 → M = T * R
    Eigen::Matrix3f M = T * R;

    Eigen::Vector3f q = M * p;

    std::cout << "q = (" << q.x() << ", " << q.y() << ")" << std::endl;
    return 0;
}
