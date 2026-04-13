import json
import matplotlib.pyplot as plt

def plot_results():
    try:
        with open("experiment_data.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: experiment_data.json not found. Run run_experiments.py first.")
        return

    days = range(len(data["Baseline"]["active_count"]))

    plt.figure(figsize=(14, 6))

    # --- Plot 1: Active Memory Count ---
    plt.subplot(1, 2, 1)
    plt.plot(days, data["Baseline"]["active_count"], label="Baseline (No Fuzzy)", color="red", linestyle="--", linewidth=2)
    plt.plot(days, data["Hybrid"]["active_count"], label="Hybrid (Neural + Fuzzy)", color="green", linestyle="-", linewidth=2)
    plt.title("Memory Retention Over 30 Days")
    plt.xlabel("Simulation Days")
    plt.ylabel("Active Memory Count")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # --- Plot 2: Total System Strength ---
    plt.subplot(1, 2, 2)
    plt.plot(days, data["Baseline"]["total_strength"], label="Baseline (No Fuzzy)", color="salmon", linestyle="--", linewidth=2)
    plt.plot(days, data["Hybrid"]["total_strength"], label="Hybrid (Neural + Fuzzy)", color="lightgreen", linestyle="-", linewidth=2)
    plt.title("Total System Strength Comparison")
    plt.xlabel("Simulation Days")
    plt.ylabel("Total Strength (normalized)")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("experiment_results.png")
    print("\n[SUCCESS] Comparative analysis plot generated: experiment_results.png")

if __name__ == "__main__":
    plot_results()
