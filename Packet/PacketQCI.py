class PacketQCI:
  def __init__(self, qci, priority, delay_budget, proportional_lambda, description):
    self.priority = priority
    self.delay_budget = delay_budget
    self.qci = qci
    self.proportional_lambda = proportional_lambda
    self.description = description
