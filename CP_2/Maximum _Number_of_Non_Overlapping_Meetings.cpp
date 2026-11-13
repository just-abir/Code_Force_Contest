#pragma GCC optimize("Ofast")
#include <bits/stdc++.h>
using namespace std;

void abir()
{
}

int32_t main()
{
  ios_base::sync_with_stdio(0), cin.tie(0), cout.tie(0);

  int n;
  cin >> n;

  vector<pair<int, int>> vec;

  for (int i = 0; i < n; i++)
  {
    int s, e;
    cin >> s >> e;
    vec.push_back({e, s});
  }

  sort(vec.begin(), vec.end());

  int count = 0, last_time = -1;
  for (int i = 0; i < n; i++)
  {
    int end = vec[i].first;
    int start = vec[i].second;

    if (start >= last_time)
    {
      count++;
      last_time = end;
    }
  }
  cout << count << "\n";
  return 0;
}