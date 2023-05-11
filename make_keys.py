import random
import time
import numpy as np
import copy

from constants import MAX_INT, PROPORTIONS_OF_SAME, TEST_SETS, K_PRIME_FRACS
from constants import get_dir_name, get_k_file_name, get_k_prime_file_name
import os


def main():


    os.chdir("data")

    

    for k_size, k_prime_size in TEST_SETS:
        for PROPORTION_OF_SAME in PROPORTIONS_OF_SAME:
            # Define the name of the directory to be created
            directory = get_dir_name(k_size)

            # Save the current working directory
            prev_dir = os.getcwd()

            # Create the directory if it does not exist
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Change the current working directory to the newly created directory
            os.chdir(directory)
            
                
            # Generate intermediate set arr
            arr = np.array(random.sample(range(1, MAX_INT), k_prime_size + k_size))

            
            
            
            #  # Generate set K
            k = copy.deepcopy(arr[:k_size])



            # Save set K to a file
            k_file_name = get_k_file_name(k_size)
            np.save(k_file_name, k)


            for k_prime_frac in K_PRIME_FRACS: 
                k_prime_final_size = int( k_prime_size * k_prime_frac )

                k_prime = []
                number_of_same = int( PROPORTION_OF_SAME * k_prime_final_size)
                start = k_size- number_of_same
                end = start + k_prime_final_size
                k_prime = copy.deepcopy(arr[start:end])



                # Save set K' to a file
                k_prime_file_name = get_k_prime_file_name(k_prime_final_size, number_of_same)
                np.save(k_prime_file_name, k_prime)
            
             # Verify  the current working directory 
            print(os.getcwd())

            # Change the current working directory back to the previous directory
            os.chdir(prev_dir)

             # Verify that the current working directory has been changed back to the previous directory
            print(os.getcwd())

           
        
           

if __name__ == "__main__":
    main()
