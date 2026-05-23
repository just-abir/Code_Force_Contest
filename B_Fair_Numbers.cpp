#pragma GCC optimize("Ofast")
#include <bits/stdc++.h>
using namespace std;

void abir()
{
    long long int n;
    cin >> n;

    while (true)
    {
        long long int temp = n;
        bool ok = true;

        while (temp > 0)
        {
            int digit = temp % 10;

            if (digit != 0 && n % digit != 0)
            {
                ok = false;
                break;
            }

            temp = temp / 10;
        }
        if (ok)
        {
            cout << n << endl;
            break;
        }
        n++;
    }
}

int32_t main()
{
    ios_base::sync_with_stdio(0), cin.tie(0), cout.tie(0);
    int t = 1;
    cin >> t;
    while (t--)
        abir();
    return 0;
}