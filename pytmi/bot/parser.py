class StringParser:
    "Represents a simple forward only string parser"

    def __init__(self, string : str):
        self.str = string
        self.position = 0
    
    @property
    def complete(self) -> bool:
        "Returns true if the parser is exhausted, false otherwise"
        return self.position >= len(self.str)

    def skip_whitespace(self):
        "Skip over space characters. Currently there is no support for tab characters and the like"
        while not self.complete and self.str[self.position] == ' ':
            self.position += 1

    def skip_value(self, *values):
        """Skips over a value in the list, and returns the value it skipped over.
        If none were skipped, returns None."""

        # sort from biggest to smallest so that the most precise value matches
        values = sorted(values, reverse=True, key=lambda v: len(v))
        
        for value in values:
            test_value = self.str[self.position : self.position + len(value)]
            if test_value == value:
                self.position += len(value)
                return value

        return None

    def consume_word(self) -> str:
        "Skips over a word and returns it."
        self.skip_whitespace()

        whitespace_idx = self.str.find(' ', self.position)
        if whitespace_idx == -1:
            whitespace_idx = len(self.str)

        word = self.str[self.position : whitespace_idx]
        self.position = whitespace_idx

        return word    

    def consume_rest_as_words(self):
        "Consume every word split by a delimeter (space, comma, semicolon), and return them as a list"
        rest = self.consume_rest().replace(',', ' ').replace(';', ' ').strip()
        items = rest.split(' ')
        items = list(filter(lambda i: i != '', items))

        return items
    
    def consume_rest(self) -> str:
        rest = self.str[self.position:]
        self.position = len(self.str)
        return rest
    