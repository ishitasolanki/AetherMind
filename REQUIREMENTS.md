# Requirements — Soft Computing Neural Memory Agent

## V1 — Existing (Implemented)
- [x] Memory class with strength, age, usage_count, emotional_weight, importance
- [x] Decay mechanic: `decay_rate = 0.02 + (0.01 * age)`
- [x] Reinforcement: usage increases strength (capped at 1.0)
- [x] Forgetting: memories with strength ≤ 0.1 are pruned
- [x] ImportanceNet: 3→8→1 neural network (usage, age, emotion → importance)
- [x] Synthetic training data generation (1000 samples)
- [x] Training loop (500 epochs, Adam optimizer, MSE loss)
- [x] Agent: add, access, update, show memories
- [x] 10-day simulation with periodic memory access

## Phase 5 — Experiments & Analysis (Completed)
- [x] Comparative Simulation (Baseline vs Hybrid)
- [x] Memory Retention Metrics (97% strength for High-Imp)
- [x] Smart Pruning verification (Clutter removed)
- [x] Graphical Analysis (`experiment_results.png`)
