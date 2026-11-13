#pragma GCC optimize("Ofast")
#include <bits/stdc++.h>
using namespace std;

void abir()
{
  int n;
  cin >> n;
  vector<int> v1;
  vector<int> v2;
  map<int, int> mp;
  for (int i = 0; i < n; i++)
  {
    int x;
    cin >> x;
    mp[x]++;
  }
  int cnt = 0;

  for (auto x : mp)
  {
    v1.push_back(x.first);

    int time = x.second - 1;

    if (time > 0)
      cnt++;
    for (int i = 0; i < time; i++)
    {

      v2.push_back(x.first);
    }
  }

  reverse(v2.begin(), v2.end());

  cout << mp.size() + cnt << endl;

  for (auto x : v1)
  {
    cout << x << " ";
  }
  for (auto x : v2)
  {
    if (v2.size() == mp.size())
    {
      cout << x << endl;
    }
    else
      cout << x << " ";
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