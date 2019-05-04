class PacketQCI:
  def __init__(self, qci, priority, delay_budget, proportional_lambda, description):
    self.priority = priority
    self.delay_budget = delay_budget
    self.qci = qci
    self.proportional_lambda = proportional_lambda
    self.description = description


PACKET_QCI_DICT = {1: PacketQCI(1, 1, 0.075 / 2, proportional_lambda=0.8, description="Real-Time Services"),
                   2: PacketQCI(2, 2, 0.125 / 2, proportional_lambda=0.1, description="Conversational Services"),
                   3: PacketQCI(3, 3, 0.300 / 2, proportional_lambda=0.1, description="Background Services")
                   }