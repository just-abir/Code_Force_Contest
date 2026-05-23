#pragma GCC optimize("Ofast")
#include <bits/stdc++.h>
using namespace std;

void abir()
{
    int n;
    cin >> n;

    int minVal = -2;
    int flag = 0;
    int pos = -1;
    vector<int> v;
    for (int i = 0; i < n; i++)
    {
        int x;
        cin >> x;

        v.push_back(x);
    }
    auto mx = *max_element(v.begin(), v.end());
    cout << count(v.begin(), v.end(), mx) << endl;
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