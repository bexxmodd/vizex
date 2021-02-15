'''
 # Gives yellow color to the string
entry_name = stylize("» " + entry_name, fg(226))

# Gives orange color to the string
entry_name = stylize("■ " + entry_name + "/", fg(202))

# Convert last modified time (which is in nanoseconds)
                    #  in to a human readable format
                    dt = time.strftime(
                            '%h %d %Y %H:%M',
                            time.localtime(os.stat(entry).st_mtime))
'''
class DecoratedData():
    """
    Custom class to compare numerical data for sorting which is stylized
    and appears to the end user in the form of a decorated string.
    """

    def __init__(self, size: int, to_string: str) -> None:
        self.size = size
        self.to_string = to_string

    def __eq__(self, other) -> bool:
        return self.size == other.size

    def __ne__(self, other) -> bool:
        return self.size != other.size

    def __gt__(self, other) -> bool:
        return self.size > other.size
    
    def __gt__(self, other) -> bool:
        return self.size >= other.size
    
    def __lt__(self, other) -> bool:
        return self.size < other.size

    def __le__(self, other) -> bool:
        return self.size <= other.size

    def __repr__(self):
        return self.to_string + " :: " + str(self.size)


if __name__ == '__main__':
    file1 = DecoratedData(55456, '54.2 kb')
    file2 = DecoratedData(123233419, '117.5 mb')
    print(f'{file1} is less than {file2} : {file1 < file2}')