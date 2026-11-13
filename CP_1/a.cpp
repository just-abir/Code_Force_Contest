#pragma GCC optimize("Ofast")
#include <bits/stdc++.h>
using namespace std;

void abir()
{
  long long int a;
  cin >> a;
  long long int temp = a;
  long long int final = a;

  while (a > 0)
  {
    temp = temp / 10;
    a = a * 10;
  }

  cout << final + a << endl;
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