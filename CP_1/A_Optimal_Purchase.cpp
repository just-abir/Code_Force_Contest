#pragma GCC optimize("Ofast")
#include <bits/stdc++.h>
using namespace std;

void abir()
{
    long long int n, a, b;
    cin >> n >> a >> b;

    if (n * a <= b)
    {
        cout << n * a << endl;
    }
    else
    {
        long long int ans = (n / 3) * b;

        long long int mn = min((n % 3) * a, b);
        cout << ans + mn << endl;
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