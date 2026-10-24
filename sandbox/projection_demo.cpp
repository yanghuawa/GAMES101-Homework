#include <cmath>
#include <eigen3/Eigen/Dense>
#include <iomanip>
#include <iostream>

// 投影矩阵数值演示：把 5.3 / 5.4 的矩阵代进去，看它到底把点变成了什么。
// 运行：在本目录下执行 run_projection.cmd

constexpr float PI = 3.14159265358979323846f;

Eigen::Matrix4f make_projection(float fov_deg, float aspect, float n, float f)
{
    float t = n * std::tan(fov_deg / 180.0f * PI / 2.0f);
    float r = t * aspect;

    Eigen::Matrix4f P = Eigen::Matrix4f::Zero();
    P(0, 0) = n / r;
    P(1, 1) = n / t;
    P(2, 2) = (n + f) / (n - f);
    P(2, 3) = 2.0f * n * f / (n - f);
    P(3, 2) = -1.0f;
    return P;
}

void show(const char* label, const Eigen::Matrix4f& P, float x, float y, float z)
{
    Eigen::Vector4f p(x, y, z, 1.0f);
    Eigen::Vector4f clip = P * p;
    Eigen::Vector4f ndc = clip / clip.w();

    std::cout << label << "\n";
    std::cout << "  p    = (" << x << ", " << y << ", " << z << ", 1)\n";
    std::cout << "  clip = (" << clip.x() << ", " << clip.y() << ", "
              << clip.z() << ", " << clip.w() << ")\n";
    std::cout << "  ndc  = (" << ndc.x() << ", " << ndc.y() << ", "
              << ndc.z() << ", " << ndc.w() << ")\n\n";
}

int main()
{
    std::cout << std::fixed << std::setprecision(4);

    const float fov = 45.0f, aspect = 1.0f;
    const float n = 0.1f, f = 50.0f;
    const float t = n * std::tan(fov / 180.0f * PI / 2.0f);
    const float r = t * aspect;

    Eigen::Matrix4f P = make_projection(fov, aspect, n, f);

    std::cout << "n = " << n << ", f = " << f
              << ", fov = " << fov << " deg, aspect = " << aspect << "\n";
    std::cout << "t = " << t << ", r = " << r << "\n\n";

    std::cout << "P =\n" << P << "\n\n";

    std::cout << "=== 近平面中心：z = -n ===\n";
    show("near center", P, 0, 0, -n);

    std::cout << "=== 近平面右边缘：x = r, z = -n ===\n";
    show("near right edge", P, r, 0, -n);

    std::cout << "=== 同一个 x = r，但深度变成两倍：z = -2n ===\n";
    show("same x, twice depth", P, r, 0, -2 * n);

    std::cout << "=== 远平面中心：z = -f ===\n";
    show("far center", P, 0, 0, -f);

    std::cout << "=== 三角形实际所在的深度：z = -7 ===\n";
    show("triangle center", P, 0, 0, -7);

    std::cout << "=== 深度 z 和 z_ndc 的对应 ===\n";
    const float zs[] = {-n, -0.2f, -0.5f, -1.0f, -2.0f, -7.0f, -20.0f, -f};
    for (float z : zs) {
        Eigen::Vector4f clip = P * Eigen::Vector4f(0, 0, z, 1);
        float zndc = clip.z() / clip.w();
        std::cout << "  z = " << std::setw(8) << z
                  << "   ->   z_ndc = " << zndc << "\n";
    }

    std::cout << "\n=== 反例：最后一行写成 (0,0,1,0) 会怎样 ===\n";
    Eigen::Matrix4f Q = P;
    Q(3, 2) = 1.0f;
    show("wrong w = +z, near right edge", Q, r, 0, -n);
    show("wrong w = +z, far center", Q, 0, 0, -f);

    return 0;
}
