from pybloom_live import BloomFilter
import random
import string
import time
import sys
import os
import json


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from constants import get_k_nparray, get_all_k_prime_arrays_with_prop
from constants import FALSE_POSITIVE_RATES, PROPORTIONS_OF_SAME, TEST_SETS



def build_bloom_filter(k, k_size, target_fp_rate):
    assert(len(k) == k_size)
    bloom = BloomFilter(capacity=k_size, error_rate=target_fp_rate)

    for key in k:
        bloom.add(key)
    return bloom

# Runs experiment on bloom, k, and k_prime
# Returns the query time and observed_fp_rate
def run_experiment(bloom, k, k_prime, PROPORTION_OF_SAME, target_fp_rate):

    k_prime_size = len(k_prime)

    # Query K' and measure the performance
    false_positives = 0
    start_time = time.perf_counter()
    for key in k_prime:
        if key in bloom and key not in k:
            false_positives += 1
    query_time = (time.perf_counter() - start_time) * 1000
    observed_fp_rate = false_positives / k_prime_size
    query_time_per_key = query_time / k_prime_size
    results = {}

    k_size = len(k)
    filename1 = f"bloom_{k_size}_fp_{target_fp_rate}"
    results["total_size"] = os.path.getsize(filename1)
    results["k_size"] = len(k)
    results["k_prime_size"] = k_prime_size
    results["query_time"] = query_time
    results["observed_fp_rate"] = observed_fp_rate
    results["target_fp_rate"] = target_fp_rate
    results["proportion_of_same"] = PROPORTION_OF_SAME
    results["query_time_per_key"] = query_time_per_key
    return results

def save_bloom_filter_to_filename(bloom, filename):
    # Save the Bloom filter to a file named filename
    with open(filename, "wb") as f:
        bloom.tofile(f) 

def run_tests_with_all_k_prime(k_size):
    
    all_results = []
    # get the k with the size
    k = get_k_nparray(k_size)
    # Go over all false positive rates:
    for target_fp_rate in FALSE_POSITIVE_RATES:
        
        # Build the bloom filter
        bloom = build_bloom_filter(k, k_size, target_fp_rate)

        file_name = f"bloom_{k_size}_fp_{target_fp_rate}"
        save_bloom_filter_to_filename(bloom, file_name)
        
        # For each propotion of identical elements
        for PROPORTION_OF_SAME in PROPORTIONS_OF_SAME:
            # For each Fraction of size
            for k_prime in get_all_k_prime_arrays_with_prop(k_size, PROPORTION_OF_SAME):
                results = run_experiment(bloom, k, k_prime, PROPORTION_OF_SAME, target_fp_rate)
                all_results.append(results)
    return all_results
def main():

    all_results = []
    i= 0
    for k_size, k_prime_size in TEST_SETS:
        i+= 1
        results =  run_tests_with_all_k_prime(k_size)
        all_results += results
        if i > 4:
            break
    # Save the array of dictionaries to a JSON file
    with open("data.json", "w") as outfile:
        json.dump(all_results, outfile)
        

if __name__ == "__main__":
    main()
