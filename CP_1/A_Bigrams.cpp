#pragma GCC optimize("Ofast")
#include <bits/stdc++.h>
using namespace std;

void abir()
{
  int n;
  cin >> n;
  int arr[n];
  int three = 0, two = 0, one = 0, four = 0;
  for (int i = 0; i < n; i++)
  {
    cin >> arr[i];
    if (arr[i] >= 3)
    {
      three++;
    }
    else if (arr[i] == 2)
      two++;

    else
      one++;
  }

  if (three > 0)
  {
    cout << "YES\n";
    return;
  }
  else if (two >= 2)
  {
    cout << "YES\n";
    return;
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