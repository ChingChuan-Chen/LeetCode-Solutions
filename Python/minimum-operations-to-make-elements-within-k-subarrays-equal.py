# Time:  O(nlogx + k * n)
# Space: O(n)

from sortedcontainers import SortedList


# two sorted lists, dp
class Solution(object):
    def minOperations(self, nums, x, k):
        """
        :type nums: List[int]
        :type x: int
        :type k: int
        :rtype: int
        """
        class TwoSortedLists(object):
            def __init__(self):
                self.left = SortedList()
                self.right = SortedList()
                self.total1 = self.total2 = 0

            def add(self, val):
                if not self.left or val <= self.left[-1]:
                    self.left.add(val)
                    self.total1 += val
                else:
                    self.right.add(val)
                    self.total2 += val
                self.rebalance()

            def remove(self, val):
                if val <= self.left[-1]:
                    self.left.remove(val)
                    self.total1 -= val
                else:
                    self.right.remove(val)
                    self.total2 -= val
                self.rebalance()

            def rebalance(self):
                if len(self.left) < len(self.right):
                    self.total2 -= self.right[0]
                    self.total1 += self.right[0]
                    self.left.add(self.right[0])
                    self.right.pop(0)
                elif len(self.left) > len(self.right)+1:
                    self.total1 -= self.left[-1]
                    self.total2 += self.left[-1]
                    self.right.add(self.left[-1])
                    self.left.pop()

            def median(self):
                return self.left[-1]


        INF = float("inf")
        two_sls = TwoSortedLists()
        cost = [INF]*(len(nums)+1)
        for i in xrange(len(nums)):
            if i-x >= 0:
                two_sls.remove(nums[i-x])
            two_sls.add(nums[i])
            if i >= x-1:
                cost[i+1] = (two_sls.median()*len(two_sls.left)-two_sls.total1) + (two_sls.total2-two_sls.median()*len(two_sls.right))
        dp = [0]*(len(nums)+1)
        for i in xrange(k):
            new_dp = [INF]*(len(nums)+1)
            for j in xrange((i+1)*x, len(nums)+1):
                new_dp[j] = min(new_dp[j-1], dp[j-x]+cost[j])
            dp = new_dp
        return dp[-1]


# Time:  O(nlogn + k * n)
# Space: O(n)
import heapq
import collections


# two heaps, dp
class Solution2(object):
    def minOperations(self, nums, x, k):
        """
        :type nums: List[int]
        :type x: int
        :type k: int
        :rtype: int
        """
        class LazyHeap(object):
            def __init__(self, sign):
                self.heap = []
                self.to_del = collections.defaultdict(int)
                self.cnt = 0
                self.sign = sign

            def push(self, val):
                heapq.heappush(self.heap, self.sign*val)

            def remove(self, val):
                self.to_del[self.sign*val] += 1
                self.cnt += 1

            def pop(self):
                self.remove(self.top())

            def top(self):
                while self.heap and self.heap[0] in self.to_del:
                    self.to_del[self.heap[0]] -= 1
                    self.cnt -= 1
                    if self.to_del[self.heap[0]] == 0:
                        del self.to_del[self.heap[0]]
                    heapq.heappop(self.heap)
                return self.sign*self.heap[0]

            def __len__(self):
                return len(self.heap)-self.cnt


        class TwoHeaps(object):
            def __init__(self):
                self.left = LazyHeap(-1)   # max heap
                self.right = LazyHeap(+1)  # min heap
                self.total1 = self.total2 = 0

            def add(self, val):
                if not self.left or val <= self.left.top():
                    self.left.push(val)
                    self.total1 += val
                else:
                    self.right.push(val)
                    self.total2 += val
                self.rebalance()

            def remove(self, val):
                if val <= self.left.top():
                    self.left.remove(val)
                    self.total1 -= val
                else:
                    self.right.remove(val)
                    self.total2 -= val
                self.rebalance()

            def rebalance(self):
                if len(self.left) < len(self.right):
                    self.total2 -= self.right.top()
                    self.total1 += self.right.top()
                    self.left.push(self.right.top())
                    self.right.pop()
                elif len(self.left) > len(self.right)+1:
                    self.total1 -= self.left.top()
                    self.total2 += self.left.top()
                    self.right.push(self.left.top())
                    self.left.pop()

            def median(self):
                return self.left.top()


        INF = float("inf")
        two_heaps = TwoHeaps()
        cost = [INF]*(len(nums)+1)
        for i in xrange(len(nums)):
            if i-x >= 0:
                two_heaps.remove(nums[i-x])
            two_heaps.add(nums[i])
            if i >= x-1:
                cost[i+1] = (two_heaps.median()*len(two_heaps.left)-two_heaps.total1) + (two_heaps.total2-two_heaps.median()*len(two_heaps.right))
        dp = [0]*(len(nums)+1)
        for i in xrange(k):
            new_dp = [INF]*(len(nums)+1)
            for j in xrange((i+1)*x, len(nums)+1):
                new_dp[j] = min(new_dp[j-1], dp[j-x]+cost[j])
            dp = new_dp
        return dp[-1]
