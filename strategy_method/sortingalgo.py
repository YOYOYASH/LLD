from abc import ABC,abstractmethod
from typing import List

class SortingStrategy(ABC):
    @abstractmethod
    def sort(self,nums:List[int]):
        pass


class BubbleSortStrategy(SortingStrategy):
    def sort(self,nums:List[int]) -> List[int]:
        n = len(nums)
        for i in range(n):
            for j in range(0,n-i-1):
                if nums[j] > nums[j+1]:
                    nums[j],nums[j+1] = nums[j+1],nums[j]
        
        return nums


class QuickSortStrategy(SortingStrategy):
    def sort(self, data: list) -> list:
        if len(data) <= 1:
            return data
        pivot = data[0]
        left = [x for x in data[1:] if x < pivot]
        right = [x for x in data[1:] if x >= pivot]
        return self.sort(left) + [pivot] + self.sort(right)

class PythonSortStrategy(SortingStrategy):
    def sort(self,data:List[int]) -> List[int]:
        return sorted(data)



class Sorter:

    def __init__(self,strategy:SortingStrategy):
        self._strategy = strategy

    def set_strategy(self,strategy:SortingStrategy):
        self._strategy = strategy
    
    def sort(self,data:List[int]) -> List[int]:
        return self._strategy.sort(data)



if __name__ == '__main__':
    numbers = [5, 2, 9, 1, 5, 6]
    sorter_obj = Sorter(BubbleSortStrategy())

    print("Sorted using bubblesort: ",sorter_obj.sort(numbers))

    sorter_obj.set_strategy(QuickSortStrategy())

    print("sorted using quicksort: ",sorter_obj.sort(numbers))