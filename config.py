# ============================================================
# config.py — Centralized configuration for the Memory Agent
# ============================================================

# --- Memory Parameters ---
INITIAL_STRENGTH = 1.0          # Starting strength of a new memory
INITIAL_IMPORTANCE = 0.5        # Default importance before model prediction
REINFORCE_BOOST = 0.5           # Strength added when a memory is accessed
MAX_STRENGTH = 1.0              # Strength cap
FORGET_THRESHOLD = 0.1          # Memories below this strength are pruned

# --- Decay Parameters ---
BASE_DECAY_RATE = 0.02          # Minimum decay per time step
AGE_DECAY_FACTOR = 0.01         # Additional decay per unit of age
RETRIEVABILITY_FACTOR = 0.5     # Used for exponential Ebbinghaus decay

# --- Neural Network (ImportanceNet) ---
INPUT_SIZE = 3                  # Features: usage, age, emotion
HIDDEN_SIZE = 8                 # Hidden layer neurons
OUTPUT_SIZE = 1                 # Single importance score

# --- Training ---
TRAINING_DATA_SIZE = 1000       # Number of synthetic samples
TRAINING_EPOCHS = 500           # Training iterations
LEARNING_RATE = 0.01            # Adam optimizer learning rate
LOG_EVERY_N_EPOCHS = 100        # Print loss every N epochs

# --- Synthetic Data Ranges ---
MAX_USAGE = 10                  # Max usage count in training data
MAX_AGE = 20                    # Max age in training data

# --- Importance Formula Weights (ground truth for synthetic data) ---
EMOTION_WEIGHT = 0.4
USAGE_WEIGHT = 0.4
RECENCY_WEIGHT = 0.2

# --- Simulation ---
SIMULATION_DAYS = 10            # Number of days to simulate
REINFORCE_EVERY_N_DAYS = 3      # Access memory[0] every N days
CONSOLIDATION_THRESHOLD = 0.8   # Minimum similarity (0.0 to 1.0) to merge
ACTIVATION_SPREAD_FACTOR = 0.2  # % of reinforcement that spreads to linked memories
