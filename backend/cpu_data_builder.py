import numpy as np
import pandas as pd
np.random.seed(42)

metric_ranges = {
    "cpu_usage": (0, 100),
    "cpu_freq_percent": (0, 100),
    "cpu_idle_time": (0, 100),
    "cpu_temperature": (20, 105),
    "cpu_percent_per_core": (0, 100),
    "num_cores": (2, 32),
    "num_threads": (2, 64),
    "load_avg_1m": (0, 8),
    "uptime": (0, 10**7),  # seconds
    "memory_usage": (0, 100),
    "swap_usage": (0, 100),
    "disk_read_bytes": (0, 2 * 10**9),   # 0 to 2 GB
    "disk_write_bytes": (0, 2 * 10**9),
    "network_sent_bytes": (0, 2 * 10**9),
    "network_recv_bytes": (0, 2 * 10**9),
    "context_switches": (0, 2 * 10**5),
    "interrupts": (0, 2 * 10**5),
    "num_running_apps": (0, 50)
}

# Create a balanced score range from 1 to 100, 100 samples per score (total 10,000)
scores = np.tile(np.arange(1, 101), 1000)

# Generate synthetic data uniformly within each score group
synthetic_data = []

for score in scores:
    row = {}
    for metric, (min_val, max_val) in metric_ranges.items():
        # Slightly bias the data based on score: higher scores get more "optimal" values
        bias = score / 100
        value = np.random.uniform(min_val + (1 - bias) * (max_val - min_val) * 0.8,
                                  min_val + (1 - bias) * (max_val - min_val) * 0.2 + bias * (max_val - min_val))
        row[metric] = value
    row["score"] = score
    synthetic_data.append(row)

# Create a DataFrame
df_synthetic = pd.DataFrame(synthetic_data)
df_synthetic.head()
df_synthetic.to_csv('synthetic_data.csv', index=False)