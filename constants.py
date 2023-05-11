import numpy as np

MAX_INT = 10**10

PROPORTIONS_OF_SAME = [0.1, 0.25, 0.5]
TEST_SETS = [
    (1000, 1000),
    (10000, 10000),
    (50000, 50000),
    (100000, 100000),
    (500000, 500000),
    (1000000, 1000000)
]
K_PRIME_FRACS = [1, .5, .1]

FALSE_POSITIVE_RATES = [1.0 / (2 ** 7), 1.0 / (2 ** 8), 1.0 / (2 ** 10)]
FINGERPRINT_BITS = [7, 8, 10]

def get_dir_name(k_size):
    return  f"data_for_k{k_size}"

def get_k_file_name(k_size):
    return f"k_{k_size}"

def get_k_prime_file_name(k_prime_final_size, number_of_same):
    return f"k_prime_final_{k_prime_final_size}_num_same_{number_of_same}"

DATA_ROOT = "/home/zlagumdz/UMD_Classes/2023_Spring_Classes/CMSC_701_Comp_Genomics/HW03/data/"

def get_k_nparray(k_size):
    file_path = DATA_ROOT + get_dir_name(k_size) +"/" + get_k_file_name(k_size) + ".npy"
    return np.load(file_path)

def get_k_prime_nparray(k_size, k_prime_final_size, number_of_same):
    file_path = DATA_ROOT + get_dir_name(k_size) +"/" + get_k_prime_file_name(k_prime_final_size, number_of_same) + ".npy"
    return np.load(file_path)


def get_all_k_prime_arrays_with_prop(k_size, PROPORTION_OF_SAME):
    all_k_prime = []
    for k_prime_frac in K_PRIME_FRACS: 
        k_prime_final_size = int( k_size * k_prime_frac )
        number_of_same = int( PROPORTION_OF_SAME * k_prime_final_size)




        # Save set K' to a file
        all_k_prime.append(get_k_prime_nparray(k_size, k_prime_final_size, number_of_same))
    return all_k_prime