#include <bits/stdc++.h>
using namespace std;

int main()
{
  int n, mark;
  string name;
  cin >> n;
  vector<pair<int, string>> val;

  for (int i = 0; i < n; i++)
  {
    cin >> name >> mark;
    val.push_back({mark, name});
  }

  sort(val.begin(), val.end());
  reverse(val.begin(), val.end());
  cout << "The sorted result is: \n";

  for (auto p : val)
  {
    cout << p.second << " " << p.first << "\n";
  }

  return 0;
}