import logging
from agent import Agent
from importance_model import train_model
from config import SIMULATION_DAYS, REINFORCE_EVERY_N_DAYS

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

# --- Train the importance model ---
logger.info("=== Starting Neural Memory Agent ===")
model = train_model()

# --- Create agent and seed memories ---
agent = Agent()
agent.add_memory("User praised system", 0.8, tags=["feedback", "positive"])
agent.add_memory("Minor interaction", 0.2, tags=["neutral"])

# Consolidation test: adding a very similar memory
agent.add_memory("The system was praised by user", 0.9, tags=["positive"])

# --- Run simulation ---
logger.info(f"Running {SIMULATION_DAYS}-day simulation...")
for day in range(SIMULATION_DAYS):

    print(f"\n--- Day {day} ---")

    if day % REINFORCE_EVERY_N_DAYS == 0:
        agent.access_memory(0)

    agent.update_memories(model)
    agent.show_memories()

# --- Final Report ---
print("\n")
logger.info("=== Top 3 Important Memories ===")
top_3 = agent.get_top_memories(3)
agent.show_memories(top_3)

logger.info("=== Simulation Complete ===")