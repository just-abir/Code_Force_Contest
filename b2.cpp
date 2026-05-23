#pragma GCC optimize("Ofast")
#include <bits/stdc++.h>
using namespace std;

void abir()
{
    int n = 7;
    int arr[n];
    int sum = 0, mx = -100;
    for (int i = 0; i < n; i++)
    {
        cin >> arr[i];
        sum = sum + arr[i];
        mx = max(mx, arr[i]);
    }
    cout << 2 * mx - sum << endl;
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