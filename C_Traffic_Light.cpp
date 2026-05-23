#pragma GCC optimize("Ofast")
#include <bits/stdc++.h>
using namespace std;

void abir()
{
    int length;
    char cruentValue;
    string str;
    cin >> length >> cruentValue >> str;

    if (cruentValue == 'g')
    {
        cout << 0 << endl;
        return;
    }

    str = str + str;
    //  cout << str << endl;

    int lastG = -1;
    int ans = 0;

    for (int i = length * 2 - 1; i >= 0; i--)
    {
        if (str[i] == 'g')
            lastG = i;

        if (str[i] == cruentValue)
            ans = max(ans, lastG - i);
    }

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