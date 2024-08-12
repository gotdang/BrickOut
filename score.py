from dataclasses import dataclass


@dataclass
class Score():
    score: int = 0
    def __init__(self, initial_score: int = 0):
        self.score = initial_score
    def __str__(self):
        return str(self.score)
    def reset(self):
        self.score = 0
    def increment(self, n: int = 1):
        self.score += n
    def decrement(self, n: int = 1):
        self.score -= n
