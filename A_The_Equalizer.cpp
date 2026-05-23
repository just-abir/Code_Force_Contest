#pragma GCC optimize("Ofast")
#include <bits/stdc++.h>
using namespace std;

void abir()
{
    int n, k;
    cin >> n >> k;
    int arr[n];
    int sum = 0;
    for (int i = 0; i < n; i++)
    {
        cin >> arr[i];
        sum = sum + arr[i];
    }

    if (sum % 2 == 1)
        cout << "YES\n";
    else
    {
        if (k % 2 == 0)
            cout << "YES\n";
        else
            cout << "NO\n";
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