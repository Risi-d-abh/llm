#include <bits/stdc++.h>
using namespace std;

static inline double calculate(long long iterations, double p1, double p2) {
    double result = 1.0;
    for (long long i = 1; i <= iterations; ++i) {
        double j = i * p1 - p2;
        result -= 1.0 / j;
        j = i * p1 + p2;
        result += 1.0 / j;
    }
    return result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    const long long ITER = 200000000LL;
    const double PARAM1 = 4.0;
    const double PARAM2 = 1.0;

    auto t0 = chrono::high_resolution_clock::now();
    double result = calculate(ITER, PARAM1, PARAM2) * 4.0;
    auto t1 = chrono::high_resolution_clock::now();

    chrono::duration<double> elapsed = t1 - t0;

    cout.setf(ios::fixed);
    cout << setprecision(12) << "Result: " << result << "\n";
    cout << setprecision(6) << "Execution Time: " << elapsed.count() << " seconds\n";

    return 0;
}