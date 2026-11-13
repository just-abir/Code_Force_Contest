#include <bits/stdc++.h>
using namespace std;

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;

    while (t--)
    {
        int k, n;
        cin >> k >> n;

        vector<int> a;
        a.push_back(1);

        int cur = 1;
        int diff = 1;

        for (int i = 1; i < k; i++)
        {
            int rem = k - i - 1;

            if (cur + diff + rem <= n)
            {
                cur += diff;
                diff++;
            }
            else
            {
                cur++;
            }

            a.push_back(cur);
        }

        for (int x : a)
            cout << x << " ";
        cout << '\n';
    }

    return 0;
}