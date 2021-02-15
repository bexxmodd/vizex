class DecoratedData():
    """
    Custom class to compare numerical data for sorting
    which appears in the stylized representation of a string.
    """

    def __init__(self, size: int, to_string: str) -> None:
        self.size = size
        self.to_string = to_string

    def __eq__(self, other) -> bool:
        """Equals"""
        return self.size == other.size

    def __ne__(self, other) -> bool:
        """Not equals"""
        return self.size != other.size

    def __gt__(self, other) -> bool:
        """Greater than"""
        return self.size > other.size
    
    def __ge__(self, other) -> bool:
        """Greater than or equals to"""
        return self.size >= other.size
    
    def __lt__(self, other) -> bool:
        """Less than"""
        return self.size < other.size

    def __le__(self, other) -> bool:
        """Less than or equals to"""
        return self.size <= other.size

    def __str__(self):
        """String representation of the class"""
        return self.to_string


if __name__ == '__main__':
    file1 = DecoratedData(55456, '54.2 kb')
    file2 = DecoratedData(123233419, '117.5 mb')
    print(f'{file1} is less than {file2} : {file1 < file2}')