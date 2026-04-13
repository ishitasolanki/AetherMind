import logging
import math
import json
from importance_model import predict_importance
from fuzzy_logic import get_fuzzy_decay_multiplier
from config import (
    INITIAL_STRENGTH, INITIAL_IMPORTANCE, REINFORCE_BOOST,
    MAX_STRENGTH, FORGET_THRESHOLD, BASE_DECAY_RATE, AGE_DECAY_FACTOR,
    RETRIEVABILITY_FACTOR, CONSOLIDATION_THRESHOLD, ACTIVATION_SPREAD_FACTOR
)

logger = logging.getLogger(__name__)


class Memory:
    def __init__(self, content, emotional_weight, tags=None):
        self.content = content
        self.age = 0
        self.usage_count = 1
        self.emotional_weight = emotional_weight
        self.importance = INITIAL_IMPORTANCE
        self.strength = INITIAL_STRENGTH
        self.tags = tags or []
        # History for visualization
        self.history = {
            "strength": [self.strength],
            "importance": [self.importance],
            "age": [self.age]
        }

    def reinforce(self, factor=1.0):
        self.usage_count += 1
        boost = REINFORCE_BOOST * factor
        self.strength = min(MAX_STRENGTH, self.strength + boost)
        logger.info(f"Reinforced: '{self.content}' (Factor: {factor:.2f}) -> strength={self.strength:.2f}")

    def age_memory(self):
        self.age += 1

    def apply_decay(self, importance_score, use_fuzzy=True):
        # 1. Base Ebbinghaus exponential decay
        decay_constant = BASE_DECAY_RATE + (AGE_DECAY_FACTOR * math.log1p(self.age))
        
        # 2. Hybrid Step: Fuzzy reasoning based on Neural Importance
        if use_fuzzy:
            fuzzy_multiplier = get_fuzzy_decay_multiplier(importance_score, self.age)
        else:
            fuzzy_multiplier = 1.0 # Baseline behavior
        
        # Apply combined decay
        effective_decay = decay_constant * RETRIEVABILITY_FACTOR * fuzzy_multiplier
        self.strength *= math.exp(-effective_decay)
        
        logger.debug(f"Decay: '{self.content}' | UseFuzzy: {use_fuzzy} | Multiplier: {fuzzy_multiplier:.2f} | Strength: {self.strength:.2f}")

    def update_importance(self, model):
        self.importance = predict_importance(
            model,
            self.usage_count,
            self.age,
            self.emotional_weight
        )
        self._record_history()

    def _record_history(self):
        self.history["strength"].append(self.strength)
        self.history["importance"].append(self.importance)
        self.history["age"].append(self.age)

    def to_dict(self):
        return {
            "content": self.content,
            "age": self.age,
            "usage_count": self.usage_count,
            "emotional_weight": self.emotional_weight,
            "importance": self.importance,
            "strength": self.strength,
            "tags": self.tags,
            "history": self.history
        }

    @classmethod
    def from_dict(cls, data):
        mem = cls(data["content"], data["emotional_weight"], data["tags"])
        mem.age = data["age"]
        mem.usage_count = data["usage_count"]
        mem.importance = data["importance"]
        mem.strength = data["strength"]
        mem.history = data.get("history", {
            "strength": [mem.strength],
            "importance": [mem.importance],
            "age": [mem.age]
        })
        return mem


class Agent:
    def __init__(self):
        self.memories = []

    def add_memory(self, content, emotional_weight, tags=None):
        # Consolidation check
        for existing in self.memories:
            similarity = self._calculate_similarity(content, existing.content)
            if similarity >= CONSOLIDATION_THRESHOLD:
                logger.info(f"Consolidating '{content}' into existing memory '{existing.content}' (Sim: {similarity:.2f})")
                existing.reinforce()
                existing.emotional_weight = max(existing.emotional_weight, emotional_weight)
                if tags:
                    existing.tags = list(set(existing.tags + tags))
                return

        memory = Memory(content, emotional_weight, tags)
        self.memories.append(memory)
        logger.info(f"Added memory: '{content}' (tags={tags})")

    def _calculate_similarity(self, text1, text2):
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        if not words1 or not words2:
            return 0.0
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        return len(intersection) / len(union)

    def access_memory(self, index):
        if 0 <= index < len(self.memories):
            target = self.memories[index]
            target.reinforce(factor=1.0)
            
            # --- Spreading Activation (Associative Memory) ---
            if target.tags:
                self._spread_activation(target)

    def _spread_activation(self, source_memory):
        source_tags = set(source_memory.tags)
        for memory in self.memories:
            if memory == source_memory:
                continue
            
            # If shared tags exist, spread activation
            shared = source_tags.intersection(set(memory.tags))
            if shared:
                logger.debug(f"Spreading activation: '{source_memory.content}' -> '{memory.content}' (shared tags: {shared})")
                memory.reinforce(factor=ACTIVATION_SPREAD_FACTOR)

    def get_top_memories(self, n=5):
        return sorted(self.memories, key=lambda m: m.importance, reverse=True)[:n]

    def update_memories(self, model, use_fuzzy=True):
        for memory in self.memories:
            memory.age_memory()
            memory.update_importance(model)
            memory.apply_decay(memory.importance, use_fuzzy=use_fuzzy)

        before_count = len(self.memories)
        self.memories = [m for m in self.memories if m.strength > FORGET_THRESHOLD]
        forgotten = before_count - len(self.memories)
        if forgotten > 0:
            logger.debug(f"Pruned {forgotten} forgotten memories (Fuzzy={use_fuzzy})")

    def show_memories(self, memories=None):
        target = memories if memories is not None else self.memories
        for i, m in enumerate(target):
            tags_str = f" [{', '.join(m.tags)}]" if m.tags else ""
            print(f"  {i}: {m.content}{tags_str} | Strength: {m.strength:.2f} | Age: {m.age} | Importance: {m.importance:.2f}")

    def save_to_json(self, filepath):
        data = [m.to_dict() for m in self.memories]
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(f"Saved {len(self.memories)} memories to {filepath}")

    def load_from_json(self, filepath):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            self.memories = [Memory.from_dict(d) for d in data]
            logger.info(f"Loaded {len(self.memories)} memories from {filepath}")
        except FileNotFoundError:
            logger.warning(f"No save file found at {filepath}. Starting fresh.")
        except Exception as e:
            logger.error(f"Error loading memories: {e}")