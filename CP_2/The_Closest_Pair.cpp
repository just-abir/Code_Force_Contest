#pragma GCC optimize("Ofast")
#include <bits/stdc++.h>
using namespace std;

int32_t main()
{
  ios_base::sync_with_stdio(0), cin.tie(0), cout.tie(0);

  int num, targetVal;
  cin >> num >> targetVal;

  vector<int> vec;

  int X;

  for (int i = 0; i < num; i++)
  {
    cin >> X;
    vec.push_back(X);
  }

  sort(vec.begin(), vec.end());
  cout << "\n Sorted value: \n";
  for (auto p : vec)
  {
    cout << p << " ";
  }
  cout << endl;

  int left = 0, right = num - 1;
  int dif, sum1, difVal = INT_MAX;
  vector<pair<int, int>> p;

  while (left < right)
  {
    sum1 = vec[left] + vec[right];

    dif = abs(targetVal - sum1);

    if (dif < difVal)
    {
      difVal = dif;

      p.clear();
      p.push_back({vec[left], vec[right]});
    }
    else if (dif == difVal)
    {
      p.push_back({vec[left], vec[right]});
    }

    if (sum1 < targetVal)
    {
      left++;
    }
    else if (sum1 > targetVal)
    {
      right--;
    }
    else
    {
      left++;
      right--;
    }
  }

  sort(p.begin(), p.end());

  cout << p[0].first << " " << p[0].second << endl;

  return 0;
}