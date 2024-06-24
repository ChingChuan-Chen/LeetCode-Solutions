// Time:  O(n + max(end) * max(cnt)) <= O(n^3)
// Space: O(n + max(cnt)) <= O(n^2)

// dp, combinatorics, sliding window, two pointers
class Solution {
public:
    int numberOfPermutations(int n, vector<vector<int>>& requirements) {
        static const int MOD = 1e9 + 7;

        const auto& addmod = [&](const auto& a, const auto& b) {
            return (a + b) % MOD;
        };
        const auto& submod = [&](const auto& a, const auto& b) {
            return ((a - b) % MOD + MOD) % MOD;
        };

        vector<int> lookup(n, -1);
        for (const auto& r : requirements) {
            lookup[r[0]] = r[1];
        }
        const int max_e = (*max_element(cbegin(requirements), cend(requirements), [](const auto& a, const auto&b) {
            return a[0] < b[0];
        }))[0];
        const int max_c = (*max_element(cbegin(requirements), cend(requirements), [](const auto& a, const auto&b) {
            return a[1] < b[1];
        }))[1];
        vector<int> dp(max_c + 1);
        dp[0] = 1;
        for (int i = 0; i <= max_e; ++i) {
            vector<int> new_dp(size(dp));
            if (lookup[i] != -1) {  // optimized
                new_dp[lookup[i]] = accumulate(cbegin(dp) + max(lookup[i] - i, 0), cbegin(dp) + (lookup[i] + 1), 0, addmod);
            } else {
                for (int j = 0, curr = 0; j < size(dp); ++j) {
                    curr = addmod(curr, dp[j]);
                    if (j - (i + 1) >= 0) {
                        curr = submod(curr, dp[j - (i + 1)]);
                    }
                    new_dp[j] = curr;
                }
            }
            dp = move(new_dp);
        }
        int result = accumulate(cbegin(dp), cend(dp), 0, addmod);
        for (int i = max_e + 1; i < n; ++i) {
            result = (result * (i + 1ll)) % MOD;
        }
        return result;
    }
};

// Time:  O(n + max(end) * max(cnt)) <= O(n^3)
// Space: O(n + max(cnt)) <= O(n^2)
// dp, combinatorics, sliding window, two pointers
class Solution2 {
public:
    int numberOfPermutations(int n, vector<vector<int>>& requirements) {
        static const int MOD = 1e9 + 7;

        const auto& addmod = [&](const auto& a, const auto& b) {
            return (a + b) % MOD;
        };
        const auto& submod = [&](const auto& a, const auto& b) {
            return ((a - b) % MOD + MOD) % MOD;
        };

        vector<int> lookup(n, -1);
        for (const auto& r : requirements) {
            lookup[r[0]] = r[1];
        }
        const int max_c = (*max_element(cbegin(requirements), cend(requirements), [](const auto& a, const auto&b) {
            return a[1] < b[1];
        }))[1];
        vector<int> dp(max_c + 1);
        dp[0] = 1;
        for (int i = 0; i < n; ++i) {
            vector<int> new_dp(size(dp));
            for (int j = 0, curr = 0; j < size(dp); ++j) {
                curr = addmod(curr, dp[j]);
                if (j - (i + 1) >= 0) {
                    curr = submod(curr, dp[j - (i + 1)]);
                }
                new_dp[j] = lookup[i] == -1 || lookup[i] == j ? curr : 0;
            }
            dp = move(new_dp);
        }
        return accumulate(cbegin(dp), cend(dp), 0, addmod);
    }
};