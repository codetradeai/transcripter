import json
import time
import os

# Simulate database with 1000 records
records = [{
    "origem": "youtube",
    "titulo": f"Video {i}",
    "texto": "Some long text " * 100,
    "data": "2023-10-27 12:00:00"
} for i in range(1000)]

db_file = "simulated_db.json"
with open(db_file, "w") as f:
    json.dump({"_default": {str(i): r for i, r in enumerate(records)}}, f)

def simulate_unoptimized(iterations):
    start = time.time()
    for _ in range(iterations):
        # Simulate db.all() which reads and parses the JSON
        with open(db_file, "r") as f:
            data = json.load(f)
            transcricoes = list(data["_default"].values())
    return time.time() - start

def simulate_optimized(iterations):
    start = time.time()
    # Initial load
    with open(db_file, "r") as f:
        data = json.load(f)
        transcricoes = list(data["_default"].values())

    for _ in range(iterations):
        # Use cached transcricoes
        pass
    return time.time() - start

iterations = 100
time_unoptimized = simulate_unoptimized(iterations)
time_optimized = simulate_optimized(iterations)

print(f"Benchmark results for {iterations} iterations with 1000 records:")
print(f"Unoptimized (repeated loads): {time_unoptimized:.4f}s")
print(f"Optimized (cached): {time_optimized:.4f}s")
print(f"Improvement: {(time_unoptimized - time_optimized) / time_unoptimized * 100:.2f}%")

os.remove(db_file)
