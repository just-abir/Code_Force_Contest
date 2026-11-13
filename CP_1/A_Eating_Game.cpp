#pragma GCC optimize("Ofast")
#include <bits/stdc++.h>
using namespace std;

void abir()
{
  int n;
  cin >> n;
  string s;
  cin >> s;
  s.erase(unique(s.begin(), s.end()), s.end());
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