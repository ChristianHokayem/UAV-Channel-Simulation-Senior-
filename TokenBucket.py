class TokenBucket:
    def __init__(self, tokens):
        self.capacity = float(tokens)
        self.available_tokens = float(tokens)

    def consume(self, number_of_tokens):
        if number_of_tokens <= self.available_tokens:
            self.available_tokens -= number_of_tokens
            return True
        return False

    def return_resource(self, number_of_tokens):
        self.available_tokens += number_of_tokens
