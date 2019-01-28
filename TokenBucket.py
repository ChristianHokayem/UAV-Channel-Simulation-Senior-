class TokenBucket:
    def __init__(self, tokens):
        self.capacity = float(tokens)
        self.available_tokens = float(tokens)

    def consume(self, number_of_tokens):
        if number_of_tokens <= self.available_tokens:
            self.available_tokens -= number_of_tokens
        else:
            return False
        return True

    def return_resource(self, number_of_tokens):
        self.available_tokens += number_of_tokens
