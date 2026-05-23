#pragma GCC optimize("Ofast")
#include <bits/stdc++.h>
using namespace std;

void abir()
{

    int n;
    cin >> n;

    vector<int> v(n);

    for (int i = 0; i < n; i++)
        cin >> v[i];

    int valCnt = 0;

    for (int i = 0; i < n; i++)
    {
        int j = i;

        while (j < n && v[j] == v[i])
        {
            j++;
        }

        if ((v[i] < v[i - 1] || i == 0) && (j == n || v[j - 1] < v[j]))
        {
            valCnt++;
        }

        i = j;
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