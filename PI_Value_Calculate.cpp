#include <iostream>
#include <cstdlib>
#include <ctime>
using namespace std;

int main()
{
    int inside = 0;
    int total = 1000000;

    srand(time(0));

    for (int i = 0; i < total; i++)
    {
        double x = (double)rand() / RAND_MAX * 2 - 1;
        double y = (double)rand() / RAND_MAX * 2 - 1;

        if (x * x + y * y <= 1)
        {
            inside++;
        }
    }

    double pi = 4.0 * inside / total;

    cout << "Approximate value of pi = " << pi << endl;

    return 0;
}