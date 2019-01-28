class Event:
    num_to_type = {1: 'arrival', 3: 'service end'}
    type_to_num = {v: k for k, v in num_to_type.items()}

    def __init__(self, time, type, reference_packet=None):
        self.type = type
        self.time = time
        self.reference_packet = reference_packet

    def __lt__(self, comparable):
        return self.time < comparable.time
