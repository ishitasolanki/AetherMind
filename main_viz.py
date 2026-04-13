import logging
import matplotlib.pyplot as plt
from agent import Agent
from importance_model import train_model
from config import SIMULATION_DAYS, REINFORCE_EVERY_N_DAYS

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

def run_viz_simulation():
    # 1. Train model
    logger.info("Training importance model...")
    model = train_model()

    # 2. Setup Agent
    agent = Agent()
    agent.add_memory("System Launch Success", 0.9, tags=["milestone", "positive"])
    agent.add_memory("Minor UI Glitch", 0.3, tags=["bug", "neutral"])
    agent.add_memory("User Feature Request", 0.6, tags=["feedback"])

    # 3. Simulation loop
    logger.info(f"Running {SIMULATION_DAYS}-day simulation with tracking...")
    for day in range(SIMULATION_DAYS):
        # Reinforce launch success every 4 days
        if day % 4 == 0:
            agent.access_memory(0)
        
        agent.update_memories(model)

    # 4. Plotting
    logger.info("Generating visualization...")
    plt.figure(figsize=(12, 6))

    for memory in agent.memories:
        days = range(len(memory.history["strength"]))
        plt.plot(days, memory.history["strength"], label=f"{memory.content} (Strength)", linestyle='-')
        plt.plot(days, memory.history["importance"], label=f"{memory.content} (Importance)", linestyle='--')

    plt.title("Memory Evolution Over Time")
    plt.xlabel("Days")
    plt.ylabel("Value (0.0 - 1.0)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output_file = "memory_trends.png"
    plt.savefig(output_file)
    logger.info(f"Visualization saved to {output_file}")
    print(f"\n[SUCCESS] Memory trends plot generated: {output_file}")

if __name__ == "__main__":
    run_viz_simulation()
    plt.show() # Attempt to show if graphical env exists, otherwise just saving is fine
