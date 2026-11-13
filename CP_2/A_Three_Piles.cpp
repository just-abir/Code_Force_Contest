#pragma GCC optimize("Ofast")
#include <bits/stdc++.h>
using namespace std;

void abir()
{
  int a, b, c;
  cin >> a >> b >> c;

  if (a + 1 == b)
  {
    if (b + 1 == c)
    {
      cout << "YES\n";
    }
    else
      cout << "NO\n";
  }
  else
    cout << "NO\n";
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