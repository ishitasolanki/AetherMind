import logging
import sys
from agent import Agent
from importance_model import train_model

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

SAVE_FILE = "agent_state.json"

def interactive_session():
    print("="*60)
    print(" 🌌 AETHERMIND: NEURAL-FUZZY COGNITIVE AGENT")
    print("="*60)
    
    print("Training neural network...")
    model = train_model()
    
    agent = Agent()
    agent.load_from_json(SAVE_FILE)
    
    while True:
        print("\n--- MENU ---")
        print("1. Add Memory")
        print("2. Access/Reinforce Memory")
        print("3. Show Top Memories")
        print("4. Advance Time (1 Day)")
        print("5. Save and Exit")
        
        choice = input("\nSelect an option: ")
        
        if choice == '1':
            content = input("Memory content: ")
            try:
                emotion = float(input("Emotional weight (0.0 - 1.0): "))
                tags_raw = input("Tags (comma separated): ")
                tags = [t.strip() for t in tags_raw.split(',')] if tags_raw.strip() else []
                agent.add_memory(content, emotion, tags)
            except ValueError:
                print("Invalid input. Emotion must be a number.")
                
        elif choice == '2':
            agent.show_memories()
            try:
                idx = int(input("Index to reinforce: "))
                agent.access_memory(idx)
            except (ValueError, IndexError):
                print("Invalid index.")
                
        elif choice == '3':
            try:
                n = int(input("Number of memories to show: "))
                top = agent.get_top_memories(n)
                agent.show_memories(top)
            except ValueError:
                print("Invalid number.")
                
        elif choice == '4':
            print("Advancing system time by 1 day...")
            agent.update_memories(model)
            agent.show_memories()
            
        elif choice == '5':
            agent.save_to_json(SAVE_FILE)
            print("Goodbye!")
            break
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    interactive_session()
