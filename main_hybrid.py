import logging
from agent import Agent
from importance_model import train_model

# --- Logging Setup ---
# Set to DEBUG to see the Fuzzy Reasoning and Spreading Activation logs
logging.basicConfig(
    level=logging.INFO, # Change to DEBUG to see decision-level details
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def run_hybrid_demo():
    print("="*60)
    print(" 🌌 AETHERMIND: FULL HYBRID INTEGRATION (NEURAL + FUZZY)")
    print("="*60)

    # 1. Neural Layer: Training
    logger.info("Step 1: Training Neural Network (The Learning Layer)...")
    model = train_model()

    # 2. Setup Agent
    agent = Agent()
    
    # 3. Associative Memory Setup (Spreading Activation)
    logger.info("Step 2: Seeding Associative Memories (Sharing 'project' tag)...")
    agent.add_memory("Research Phase 4", 0.9, tags=["project", "work"])
    agent.add_memory("Write implementation plan", 0.7, tags=["project", "planning"])
    agent.add_memory("Trivial task", 0.2, tags=["unrelated"])

    # 4. Simulation with Hybrid Pipeline
    days = 5
    logger.info(f"Step 3: Running {days}-day Hybrid Simulation...")
    for day in range(days):
        print(f"\n--- Day {day} ---")
        
        # Access only the first task
        if day == 2:
            logger.info("--> MANUALLY REINFORCING 'Research Phase 4'...")
            agent.access_memory(0)
            print("Note: Watch how 'Write implementation plan' also gains strength via Spreading Activation.")

        # Update memories calls:
        # NN (Importance) -> FIS (Decay Multiplier) -> Memory (Strength Update)
        agent.update_memories(model)
        agent.show_memories()

    print("\n" + "="*60)
    print(" HYBRID PIPELINE VERIFIED")
    print(" Neural Network -> Predicted Importance")
    print(" Fuzzy Logic    -> Reasoned Decay Multiplier")
    print(" Tag Network    -> Spreading Activation")
    print("="*60)

if __name__ == "__main__":
    run_hybrid_demo()
