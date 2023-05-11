

# K = [1000, 1000, 1000, 10000, 10000, 10000, 50000, 50000, 50000, 100000, 100000, 100000, 500000, 500000, 500000, 1000000, 1000000, 1000000]

# K_prime = [1000, 1000, 1000, 10000, 10000, 10000, 50000, 50000, 50000, 100000, 100000, 100000, 500000, 500000, 500000, 1000000, 1000000, 1000000]

# Target_FP_Rate = [0.00781, 0.00391, 0.00098, 0.00781, 0.00391, 0.00098, 0.00781, 0.00391, 0.00098, 0.00781, 0.00391, 0.00098, 0.00781, 0.00391, 0.00098, 0.00781, 0.00391, 0.00098]

# Observed_FP_Rate = [0.00400, 0.00200, 0.00000, 0.00330, 0.00220, 0.00060, 0.00352, 0.00234, 0.00056, 0.00414, 0.00201, 0.00051, 0.00378, 0.00195, 0.00049, 0.00387, 0.00192, 0.00048]

# Query_Time = [2.06, 2.52, 2.58, 150.74, 149.37, 148.70, 4147.42, 4028.00, 4389.02, 17848.00, 16897.65, 19000.60, 497072.23, 515839.26, 539221.80, 2112428.93, 2201349.47, 2067571.64]


import json
import matplotlib.pyplot as plt

# Load the data from the JSON file
with open("data.json", "r") as infile:
    data = json.load(infile)

# Extract the relevant data
sizes = [d["total_size"] for d in data]
query_times = [d["query_time"] for d in data]
observed_fp_rates = [d["observed_fp_rate"] for d in data]
target_fp_rates = [d["target_fp_rate"] for d in data]

# Plot the observed vs. target false positive rates
plt.figure()
plt.scatter(target_fp_rates, observed_fp_rates)
plt.xlabel("Target False Positive Rate")
plt.ylabel("Observed False Positive Rate")
plt.title("Observed vs. Target False Positive Rates")
plt.savefig("observed_vs_target_fp_rates.png")

# Plot the query time vs. target false positive rate
plt.figure()
plt.scatter(target_fp_rates, query_times)
plt.xlabel("Target False Positive Rate")
plt.ylabel("Query Time (ms)")
plt.title("Query Time vs. Target False Positive Rate")
plt.savefig("query_time_vs_target_fp_rate.png")

# Plot the total size of the Bloom filter vs. target false positive rate
plt.figure()
plt.scatter(target_fp_rates, sizes)
plt.xlabel("Target False Positive Rate")
plt.ylabel("Total Size of the Bloom Filter (bytes)")
plt.title("Total Size of the Bloom Filter vs. Target False Positive Rate")
plt.savefig("total_size_vs_target_fp_rate.png")

plt.close()
