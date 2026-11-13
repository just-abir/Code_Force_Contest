#include <bits/stdc++.h>
using namespace std;

int main()
{
    // your code goes here
    int test;
    cin >> test;
    while (test--)
    {
        int n, budget;
        cin >> n >> budget;

        int itemList[n];
        for (int i = 0; i < n; i++)
            cin >> itemList[i];

        int budgetList[n];
        for (int i = 0; i < n; i++)
            cin >> budgetList[i];

        int mxTest = 0, mxCost = 0;

        for (int i = 0; i < n; i++)
        {
            for (int j = 0; i < n; j++)
            {
                int expesive = max(itemList[i], itemList[j]);
                int discount = min(expesive / 2, 100);
                int totalCost = itemList[i] + itemList[j] - discount;

                if (totalCost <= budget)
                {
                    mxTest = max(mxTest, budgetList[i] + budgetList[j]);
                }
            }
        }

        cout << mxTest << "\n";
    }
}
