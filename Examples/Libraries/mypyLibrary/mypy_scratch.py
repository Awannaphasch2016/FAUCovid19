from typing import List

x_type  = List[List[str]]

if __name__ == '__main__':
    y = ['a', 'b', 'c']
    x: x_type = [y, y, y]
