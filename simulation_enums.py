from enum import Enum


class QueueingModel(Enum):
  FCFS_QUEUING = 'fcfs'
  PRIORITY_QUEUING = 'priority'
  MODIFIED_PRIORITY_QUEUING = 'modified priority'
  EDF_QUEUING = 'edf'


class Fading(Enum):
  RICIAN = 'rice'
  RAYLEIGH = 'rayleigh'
