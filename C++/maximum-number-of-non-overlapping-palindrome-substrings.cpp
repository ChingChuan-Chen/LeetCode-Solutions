// Time:  O(n * k)
// Space: O(1)

// greedy
class Solution {
public:
    int maxPalindromes(string s, int k) {
        int result = 0;
        for (int mid = 0, prev = 0; mid < 2 * size(s) - 1; ++mid) {
            int left = mid / 2, right = mid / 2 + mid % 2;
            while (left >= prev && right < size(s) && s[left] == s[right]) {
                if (right - left + 1 >= k) {
                    prev = right + 1;
                    ++result;
                    break;
                }
                --left, ++right;
            }
        }
        return result;
    }
};
