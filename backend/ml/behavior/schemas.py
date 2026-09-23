from dataclasses import dataclass


@dataclass
class BehaviorPrediction:
    sleep_disturbance: bool
    appetite_change: bool
    crying: bool
    hopelessness: bool
    bonding_issue: bool
    social_withdrawal: bool
    anxiety: bool
    self_harm_risk: bool