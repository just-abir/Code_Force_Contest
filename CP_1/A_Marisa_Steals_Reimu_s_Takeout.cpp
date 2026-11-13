#pragma GCC optimize("Ofast")
#include <bits/stdc++.h>
using namespace std;

void abir()
{
    int n;
    cin >> n;

    int one = 0, two = 0, zero = 0;

    for (int i = 0; i < n; i++)
    {
        int x;
        cin >> x;

        if (x == 0)
            zero++;
        else if (x == 1)
            one++;
        else
            two++;
    }

    int mn = min(one, two);

    int ans = zero + mn;

    one -= mn;
    two -= mn;

    ans += one / 3;
    ans += two / 3;

    cout << ans << '\n';
}

int32_t main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;

    while (t--)
    {
        abir();
    }

    return 0;
}