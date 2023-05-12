

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



k_1000_res = []
ps_1 = []
for d in data:
    if d["k_size"] == 500000:
        k_1000_res.append(d)
for d in data:
    if d["proportion_of_same"] == 0.1:
        ps_1.append(d)
data = k_1000_res
# data = ps_1

# Extract the relevant data
sizes = [d["total_size"] for d in data]
query_times = [d["query_time"] for d in data]
observed_fp_rates = [d["observed_fp_rate"] for d in data]
# target_fp_rates = [d["target_fp_rate"] for d in data]
query_time_per_key = [d["query_time_per_key"] for d in data]
k_prime_sizes = [d["k_prime_size"] for d in data]
proportion_of_same = [d["proportion_of_same"] for d in data]
k_size = [d["k_size"] for d in data]

title1 = "Observed vs. Target False Positive Rates"
title2 = "Query Time per key vs. Observed Positive Rate"
title3 = "Total Size of the MPHF vs. Target False Positive Rate"
title4 = "Observed FPR vs |k'|"
title5 = "Observed FPR vs proportion of same between K' and K"
title6 = "|K| size vs Total Size"
title7 = "|K| size vs query time per key"
title8 = "|K'| size vs query time per key"

titles = [title1, title2, title3, title4, title5, title6, title7, title8]
for i in range(len(titles)):
    # titles[i] += " for fixed prop of same"
    titles[i] += " for |K| = 500000"
    
print(titles)

# # Plot the observed vs. target false positive rates
# plt.figure()
# plt.scatter(target_fp_rates, observed_fp_rates)
# plt.xlabel("Target False Positive Rate")
# plt.ylabel("Observed False Positive Rate")
# plt.title(titles[0])
# plt.savefig("observed_vs_target_fp_rates.png")

# Plot the query time vs. target false positive rate
plt.figure()
plt.scatter(observed_fp_rates, query_time_per_key)
plt.xlabel("Observed False Positive Rate")
plt.ylabel("Query Time (ms) per key")
plt.title(titles[1])
plt.savefig("query_time_vs_observed_fp_rate.png")

# # Plot the total size of the Bloom filter vs. target false positive rate
# plt.figure()
# plt.scatter(target_fp_rates, sizes)
# plt.xlabel("Target False Positive Rate")
# plt.ylabel("Total Size of the MPHF (bytes)")
# plt.yscale("log")
# plt.title(titles[2])
# plt.savefig("total_size_vs_target_fp_rate.png")

# Plot the observed vs. target false positive rates
plt.figure()
plt.scatter(k_prime_sizes, observed_fp_rates)
plt.xlabel("K Prime sizes")
plt.xscale("log")
plt.ylabel("Observed False Positive Rate")
plt.title(titles[3])
plt.savefig("observed_fp_rate_vs_k_prime_size.png")


# Plot the observed vs. target false positive rates
plt.figure()
plt.scatter(proportion_of_same, observed_fp_rates)
plt.xlabel("K Prime proportion of same")
plt.ylabel("Observed False Positive Rate")
plt.title(titles[4])
plt.savefig("observed_fp_rate_vs_k_prime_prop_of_same.png", dpi=1000)



# Plot the total size of the Bloom filter vs. target false positive rate
plt.figure()
plt.scatter(k_size, sizes)
plt.xlabel("K Size")
plt.xscale("log")
plt.yscale("log")
plt.ylabel("Total Size of the MPHF (bytes)")
plt.title(titles[5])
plt.savefig("total_size_vs_k_size.png")



# Plot the |K| size vs query time per key
plt.figure()
plt.scatter(k_size, query_time_per_key)
plt.xlabel("K Size")
plt.xscale("log")
plt.ylabel("Query time per key")
plt.title(titles[6])
plt.savefig("k_size_vs_query_per_key.png")


# title8
plt.figure()
plt.scatter(k_prime_sizes, query_time_per_key)
plt.xlabel("K prime Size")
plt.ylabel("Query time per key")
plt.xscale("log")
plt.title(titles[7])
plt.savefig("k_prime_size_vs_query_per_key.png")
plt.close()
