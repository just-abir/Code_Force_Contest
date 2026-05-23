#pragma GCC optimize("Ofast")
#include <bits/stdc++.h>
using namespace std;

void abir()
{
    int n;
    cin >> n;

    vector<long long> a(n);

    for (int i = 0; i < n; i++)
    {
        cin >> a[i];
    }

    vector<int> ans;

    int flip = 0;

    for (int i = n - 1; i >= 0; i--)
    {
        long long current;

        if (flip & 1)
            current = -a[i];
        else
            current = a[i];

        if (current > 0)
        {
            ans.push_back(i + 1);
            flip++;
        }
    }

    reverse(ans.begin(), ans.end());

    cout << ans.size() << "\n";

    for (int x : ans)
    {
        cout << x << " ";
    }

    cout << "\n";
}

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;

    while (t--)
    {
        abir();
    }

    return 0;
}