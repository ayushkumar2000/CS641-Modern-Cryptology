#include <bits/stdc++.h>
using namespace std;
#define fo(i, n) for (int i = 0; i < n; i++)

void reverse_blocks() {
  string s;
  cin >> s;
  string p = "";
  for (int i = 0; i < s.length();) {
    for (int j = i + 4; j >= i; j--) {
      p += s[j];
    }
    i += 5;
  }
  cout << p;
}

int main() {
  reverse_blocks();
  return 0;
}