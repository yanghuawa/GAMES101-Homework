#include <cmath>
#include <eigen3/Eigen/Dense>
#include <iostream>

// 作业 0：把点 P = (2, 1) 先绕原点逆时针旋转 45°，再平移 (1, 2)。
// 要求用齐次坐标完成，手算结果应为 (1.7071, 4.1213)。
//
// 只改三个 TODO，框架不要动：
//   1) R：旋转矩阵（3x3 齐次形式）
//   2) T：平移矩阵（3x3 齐次形式）
//   3) M：组合顺序（先旋转、后平移，谁在左边？）

int main()
{
    const float PI = std::acos(-1.0f);
    const float theta = 45.0f / 180.0f * PI;

    Eigen::Vector3f p(2.0f, 1.0f, 1.0f); // 齐次坐标 (x, y, 1)

    // TODO 1: 绕 Z 轴逆时针旋转 theta
    Eigen::Matrix3f R = Eigen::Matrix3f::Identity();

    // TODO 2: 平移 (1, 2)
    Eigen::Matrix3f T = Eigen::Matrix3f::Identity();

    // TODO 3: 先旋转、再平移
    Eigen::Matrix3f M = T * R;

    Eigen::Vector3f q = M * p;

    std::cout << "q = (" << q.x() << ", " << q.y() << ")" << std::endl;
    return 0;
}
