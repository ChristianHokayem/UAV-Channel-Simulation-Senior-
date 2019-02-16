class PacketQCI:
  def __init__(self, qci, is_gbr, priority, budget, proportional_lambda, description):
    self.isGBR = is_gbr
    self.priority = priority
    self.budget = budget
    self.qci = qci
    self.proportional_lambda = proportional_lambda
    self.description = description
