#include <cmath>
#include <eigen3/Eigen/Dense>
#include <iomanip>
#include <iostream>

// Eigen 操作练习：按顺序跑一遍，和作业 0 的 R/T 对上。
// 编译运行：在 sandbox 目录下执行 run.cmd

int main()
{
    std::cout << std::fixed << std::setprecision(4);

    // 1. 向量：Vector3f 是 3 个 float 的列向量
    Eigen::Vector3f v(1.0f, 2.0f, 3.0f);
    std::cout << "1) v =\n" << v << "\n\n";

    // 2. 矩阵：<< 按“行”填
    Eigen::Matrix3f A;
    A << 1, 2, 3,
         4, 5, 6,
         7, 8, 9;
    std::cout << "2) A =\n" << A << "\n\n";

    // 3. 取元素：下标从 0 开始，用圆括号
    std::cout << "3) A(0,1) = " << A(0, 1) << "   A(2,0) = " << A(2, 0) << "\n\n";

    // 4. 单位阵 / 零矩阵
    Eigen::Matrix3f I = Eigen::Matrix3f::Identity();
    Eigen::Matrix3f Z = Eigen::Matrix3f::Zero();
    std::cout << "4) I =\n" << I << "\n\n";

    // 5. 矩阵乘向量
    Eigen::Vector3f u(1.0f, 0.0f, 0.0f);
    std::cout << "5) A * u =\n" << (A * u) << "\n\n";

    // 6. 转置
    std::cout << "6) A.transpose() =\n" << A.transpose() << "\n\n";

    // 7. 作业 0 的 R：绕 z 轴逆时针转 45°
    const float theta = 45.0f / 180.0f * std::acos(-1.0f);
    const float c = std::cos(theta);
    const float s = std::sin(theta);
    Eigen::Matrix3f R;
    R << c, -s, 0,
         s,  c, 0,
         0,  0, 1;
    std::cout << "7) R =\n" << R << "\n\n";

    // 8. 作业 0 的 T：平移 (1, 2)
    Eigen::Matrix3f T;
    T << 1, 0, 1,
         0, 1, 2,
         0, 0, 1;
    std::cout << "8) T =\n" << T << "\n\n";

    // 9. 齐次坐标点 (2, 1, 1)，先 R 后 T
    Eigen::Vector3f p(2.0f, 1.0f, 1.0f);
    std::cout << "9) R * p =\n" << (R * p) << "\n\n";
    std::cout << "   T * R * p =\n" << (T * R * p) << "\n\n";

    // 10. 组合矩阵 M = T * R，和 T * R * p 等价
    Eigen::Matrix3f M = T * R;
    std::cout << "10) M = T * R =\n" << M << "\n";
    std::cout << "    M * p =\n" << (M * p) << "\n";

    return 0;
}
