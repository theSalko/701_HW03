import bbhash
import hashlib
import bitarray
from bitarray.util import ba2int
import time
import json
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from constants import get_k_nparray, get_all_k_prime_arrays_with_prop
from constants import FINGERPRINT_BITS, PROPORTIONS_OF_SAME, TEST_SETS


# Function to generate a hash for an input value
def uint_hash(value):
    return int(hashlib.sha1(str(value).encode()).hexdigest(), 16)

# Function to create an MPHF using the bbhash library
def get_mphf(numbers_to_hash, num_threads=1, gamma=3):
    return bbhash.PyMPHF(numbers_to_hash, len(numbers_to_hash), num_threads, gamma)

# Function to create a fingerprint array for the given MPHF and number of bits per element
def create_fingerprint_array(uint_hashes, mphf, num_bits):
    # Initialize a bitarray with enough space for all fingerprints
    fingerprint_array = bitarray.bitarray(len(uint_hashes) * num_bits)
    fingerprint_array.setall(0)

    # For each hash value, calculate its fingerprint and store it in the fingerprint array
    for hash_value in uint_hashes:
        index = mphf.lookup(hash_value)
        fingerprint = uint_hash(hash_value) & ((1 << num_bits) - 1)
        fingerprint_array[index * num_bits:(index + 1) * num_bits] = bitarray.bitarray(bin(fingerprint)[2:].zfill(num_bits))

    return fingerprint_array

# Function to query the fingerprint array for a given value
def query_fingerprint_array(mphf, fingerprint_array, query, num_bits):
    index = mphf.lookup(query)
    if index is None:
        return False
    fingerprint = uint_hash(query) & ((1 << num_bits) - 1)
    stored_fingerprint = fingerprint_array[index * num_bits:(index + 1) * num_bits]
    stored_fingerprint = ba2int(stored_fingerprint) 
    

    # Returns True if the query's fingerprint matches the stored fingerprint, False otherwise
    return fingerprint == stored_fingerprint


# Runs experiment on bloom, k, and k_prime
# Returns All results of experiment
def run_experiment(mphf, fingerprint_array, k, k_prime, PROPORTION_OF_SAME, num_bits):

    k_prime_size = len(k_prime)

    # Query K' and measure the performance
    false_positives = 0
    start_time = time.perf_counter()
    for key in k_prime:
        if query_fingerprint_array(mphf, fingerprint_array, key, num_bits) and key not in k:
            false_positives += 1
    query_time = (time.perf_counter() - start_time) * 1000
    observed_fp_rate = false_positives / k_prime_size
    query_time_per_key = query_time / k_prime_size
    results = {}
    k_size = len(k)
    filename1 = f"fingerprint_{len(k)}_bits_{num_bits}"
    filename2 = f"mphf_{k_size}"
    results["total_size"] = os.path.getsize(filename1) + os.path.getsize(filename2)
    results["k_size"] = k_size
    results["k_prime_size"] = k_prime_size
    results["query_time"] = query_time
    results["observed_fp_rate"] = observed_fp_rate
    results["num_bits"] = num_bits
    results["proportion_of_same"] = PROPORTION_OF_SAME
    results["query_time_per_key"] = query_time_per_key
    return results


def save_fingerprint_array_to_filename(fingerprint_array, filename):
    # Save the Bloom filter to a file named filename
    with open(filename, "wb") as f:
        fingerprint_array.tofile(f) 

def run_tests_with_all_k_prime(k_size):
    
    all_results = []
    # get the k with the size
    k = list( get_k_nparray(k_size) )

     # Build the MPHF
    mphf = get_mphf(k)

    # Save mphf 
    file_name = f"mphf_{k_size}"
    mphf.save(file_name)
    # Go over all FINGERPRINT BITS:
    for num_bits in FINGERPRINT_BITS:
        


        # Create the fingerprint array using the MPHF
        fingerprint_array = create_fingerprint_array(k, mphf, num_bits)

        file_name_fingerprint = f"fingerprint_{k_size}_bits_{num_bits}"
        save_fingerprint_array_to_filename(fingerprint_array, file_name_fingerprint)
        # Go over all FINGERPRIN


        
        # For each propotion of identical elements
        for PROPORTION_OF_SAME in PROPORTIONS_OF_SAME:
            # For each Fraction of size
            for k_prime in get_all_k_prime_arrays_with_prop(k_size, PROPORTION_OF_SAME):
                results = run_experiment(mphf, fingerprint_array, k, k_prime, PROPORTION_OF_SAME, num_bits)
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

    return 0


    uint_hashes = list(range(100000))  # Replace with your list of uint_hashes
    num_bits = 4  # Set the desired number of bits per fingerprint
    num_threads = 1  # Number of threads for MPHF
    gamma = 3  # Set gamma value for MPHF
    not_hashes = range(100000, 200000)
    # Create the MPHF
    mphf = get_mphf(uint_hashes, num_threads, gamma)
    # Create the fingerprint array using the MPHF
    fingerprint_array = create_fingerprint_array(uint_hashes, mphf, num_bits)
    print(type(fingerprint_array))

    for query in uint_hashes:
        res = query_fingerprint_array(mphf, fingerprint_array, query, num_bits)
        if not res:
            print("PROBLEM")
            print(res, query)
    return 0
    for query in not_hashes:
        res = query_fingerprint_array(mphf, fingerprint_array, query, num_bits)
        if res:
            print(res, query)
    # Perform queries using `query_fingerprint_array(mphf, fingerprint_array, query, num_bits)`
    # Compare false positive rate, query speed, and size against the bloom filter

if __name__ == "__main__":
    main()
