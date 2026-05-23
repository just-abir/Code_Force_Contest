#pragma GCC optimize("Ofast")
#include <bits/stdc++.h>
using namespace std;

void abir()
{
    int n;
    cin >> n;
    int arr[n];
    int one = 0, zero = 0, two = 0, ans = 0;
    for (int i = 0; i < n; i++)
    {
        cin >> arr[i];
        if (arr[i] == 1)
            one++;
        else if (arr[i] == 2)
            two++;
        else
            zero++;
    }
    int mn = min(two, one);
    ans = ans + mn;
    one -= mn;
    two -= mn;

    ans += one / 3;
    ans += two / 3;
    cout << ans << endl;
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