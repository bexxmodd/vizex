from dataclasses import dataclass

@dataclass(order=True)
class DecoratedData():
    """
    Custom class to compare numerical data for sorting
    which appears in the stylized representation of a string.
    """
    size: int
    to_string: str

    def __str__(self):
        """String representation of the class"""
        return self.to_string


if __name__ == '__main__':
    file1 = DecoratedData(55456, '54.2 kb')
    file2 = DecoratedData(123233419, '117.5 mb')
    print(f'{file1} is less than {file2} : {file1 < file2}')