class WindowedList:

    def __init__(self, size: int):
        self.size = size
        self.windowed_list = [0] * size
        self.readings = 0

    def push(self, value: int):
        self.windowed_list.append(value)
        self.windowed_list.pop(0)
        self.readings += 1

    def mean(self) -> float:
        return sum(self.windowed_list) / self.size

    def all_same(self) -> bool:
        return self.windowed_list.count(self.windowed_list[0]) == self.size

    def stalled(self):
        return ( self.readings >= self.size and self.all_same() and self.mean() == 0.0 )
    
    def moving(self):
        return ( self.readings >= self.size and self.mean() != 0.0 )
