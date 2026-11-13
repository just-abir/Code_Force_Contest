#include <bits/stdc++.h>
using namespace std;

int main()
{

  int num;
  cin >> num;
  vector<int> vec;
  int x;
  for (int i = 0; i < num; i++)
  {
    cin >> x;
    vec.push_back(x);
  }

  sort(vec.begin(), vec.end());

  int countX = 1;
  vector<pair<int, int>> Freq;
  for (int i = 0; i + 1 < num; i++)
  {
    if (vec[i] == vec[i + 1])
    {
      countX++;
    }
    else
    {

      Freq.push_back({vec[i], countX});

      countX = 1;
    }
  }

  Freq.push_back({vec[num - 1], countX});

  for (auto x : Freq)
  {

    cout << x.first << " " << x.second << endl;
  }

  sort(Freq.begin(), Freq.end());

  cout << Freq[0].first << " " << Freq[0].second << endl;
}