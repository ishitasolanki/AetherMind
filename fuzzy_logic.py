# ============================================================
# fuzzy_logic.py — Reasoning Layer (Fuzzy Inference System)
# ============================================================

import logging

logger = logging.getLogger(__name__)

class FuzzyInferenceSystem:
    def __init__(self):
        # We define simple triangular membership functions
        # Lower, Peak, Upper
        self.importance_sets = {
            "low": (0.0, 0.0, 0.4),
            "medium": (0.2, 0.5, 0.8),
            "high": (0.6, 1.0, 1.0)
        }
        
        self.age_sets = {
            "young": (0, 0, 10),
            "old": (5, 20, 100)
        }
        
        # Output: Decay Multiplier
        self.decay_sets = {
            "protected": 0.2,   # 80% reduction in decay
            "normal": 1.0,      # No change
            "aggressive": 2.5   # 2.5x faster decay
        }

    def _get_membership(self, value, triangle):
        low, peak, high = triangle
        if value <= low or value >= high:
            return 0.0
        if value == peak:
            return 1.0
        if value < peak:
            return (value - low) / (peak - low)
        return (high - value) / (high - peak)

    def calculate_decay_multiplier(self, importance, age):
        """
        Reasons about how fast a memory should decay based on 
        the Neural Importance and the chronological Age.
        """
        
        # 1. Fuzzification
        m_imp_high = self._get_membership(importance, self.importance_sets["high"])
        m_imp_low = self._get_membership(importance, self.importance_sets["low"])
        m_imp_med = self._get_membership(importance, self.importance_sets["medium"])
        
        m_age_old = self._get_membership(age, self.age_sets["old"])
        m_age_young = self._get_membership(age, self.age_sets["young"])

        # 2. Rule Evaluation (Mamdani Inference - MIN for AND, MAX for OR)
        # Rule 1: IF Importance is High THEN Decay is Protected
        rule1 = m_imp_high
        
        # Rule 2: IF Importance is Low AND Age is Old THEN Decay is Aggressive
        rule2 = min(m_imp_low, m_age_old)
        
        # Rule 3: IF Importance is Medium THEN Decay is Normal
        rule3 = m_imp_med
        
        # Rule 4: IF Age is Young THEN Decay is Protected (give new memories a chance)
        rule4 = m_age_young

        # 3. Defuzzification (Weighted Average / Centroid approximation)
        # Combine rules and outputs
        # We'll use clipping and a simple weighted average for performance
        
        weights = {
            "protected": max(rule1, rule4),
            "normal": rule3,
            "aggressive": rule2
        }
        
        numerator = 0.0
        denominator = 0.0
        
        for state, weight in weights.items():
            numerator += weight * self.decay_sets[state]
            denominator += weight
            
        if denominator == 0:
            return 1.0 # Default to normal if no rules fire
            
        multiplier = numerator / denominator
        
        logger.debug(f"Fuzzy Reasoning: Imp={importance:.2f}, Age={age} -> Multiplier={multiplier:.2f}")
        return multiplier

# Global instance
fis = FuzzyInferenceSystem()

def get_fuzzy_decay_multiplier(importance, age):
    return fis.calculate_decay_multiplier(importance, age)
