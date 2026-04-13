import logging
import json
from agent import Agent
from importance_model import train_model

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

def run_comparative_experiment():
    print("="*60)
    print(" PHASE 5: COMPARATIVE EXPERIMENT (60 DAYS)")
    print(" Goal: Prove that Hybrid system protects 'Active' important memories")
    print("="*60)

    # 1. Shared Model
    logger.info("Step 1: Training shared Importance Model...")
    model = train_model()

    # 2. Experimental Setup
    duration = 60
    memories_to_seed = [
        ("Core Architecture", 0.95),  # High Importance (To be reinforced)
        ("Trivial Log", 0.2)           # Low Importance (To be ignored)
    ]

    results = {
        "Baseline": {"active_count": [], "total_strength": [], "final_memories": {}},
        "Hybrid": {"active_count": [], "total_strength": [] , "final_memories": {}}
    }

    for mode in ["Baseline", "Hybrid"]:
        logger.info(f"\nRunning {mode} Simulation...")
        agent = Agent()
        for content, emotion in memories_to_seed:
            agent.add_memory(content, emotion)
        
        use_fuzzy = (mode == "Hybrid")
        
        for day in range(duration):
            # REINFORCE 'Core Architecture' every 5 days
            if day % 5 == 0:
                agent.access_memory(0)
                
            agent.update_memories(model, use_fuzzy=use_fuzzy)
            results[mode]["active_count"].append(len(agent.memories))
            results[mode]["total_strength"].append(sum(m.strength for m in agent.memories))

        for m in agent.memories:
            results[mode]["final_memories"][m.content] = round(m.strength, 3)
            
        logger.info(f"{mode} Complete.")

    # 3. Save Results
    with open("experiment_data.json", "w") as f:
        json.dump(results, f, indent=4)
    
    # 4. Impact Analysis
    print("\n" + "-"*40)
    print(" FINAL SYSTEM RETENTION ANALYSIS")
    print("-" * 40)
    
    print(f"{'Memory Content':25} | {'Baseline':10} | {'Hybrid':10} | {'Status'}")
    print("-" * 65)
    
    for content in ["Core Architecture", "Trivial Log"]:
        b_s = results["Baseline"]["final_memories"].get(content, 0.0)
        h_s = results["Hybrid"]["final_memories"].get(content, 0.0)
        
        if h_s > b_s:
            status = "INTELLIGENT PROTECTION"
        elif h_s < b_s and h_s == 0:
            status = "SMART PRUNING"
        else:
            status = "NORMAL"
            
        print(f"{content:25} | {b_s:10.3f} | {h_s:10.3f} | {status}")

if __name__ == "__main__":
    run_comparative_experiment()
