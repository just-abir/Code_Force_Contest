#pragma GCC optimize("Ofast")
#include <bits/stdc++.h>
using namespace std;

void abir()
{
    int n;
    cin >> n;
    if (n >= 0 && n <= 66)
        cout << n + 1 << endl;
    else if (n == 67)
        cout << 67 << endl;
    else
        cout << n + 1 << endl;
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