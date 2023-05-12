# Report

1. Implementation: On top level you have the constants.py file which houses all the constants used in the tasks. Then you have the make keys which makes k and k prime. Then the implmentation of the tasks is divided into folders task1, task2, task3 for each of the 3 tasks. Run the python script with the task algorithm and you will generate a data.json file with all the data. Then run the analyze script to generate the plots. 

2. Most difficult was to structure the experiments nicely so that it's easily reproducible and downloading the correct libraries.

3. Plots will show up in the final pdf in the plots section.

## Task 1
We generated tons of datasets with different proportions of the shared keys and the different ratios of sizes to support our conclusions. Generally we have a little bit of variance on the observed and target fp rates, though we suspect that could also be a product of the size of k'. 

We suppport the theoretical view that as k increases linearly, so does the size of the bloom filter for a fixed false positive rate. There also seems to be a logarithmic relationship between the size of k and the time is takes per query. 

All other conclusions are in our measurements and beyond the scope of this homework.

## Task 2
As with task 1 we generated the same number of datasets changing similar hyperparameters where applicable. 

Here we observed the same expected linear relationship between the size of the MPHF and the size of K. Though it seems that the size of the MPHF was smaller than the size of the Bloom filter given the same size of K. Why this could be the case would require further investigation into the implementation of the two libraries which is outside of the scope of the current report.

The great thing is that the query time per key seems fairly constant up to a certain point. This could be a matter of an outlier, but given the time and compute power it takes to run such experiments (more than initially expected), we make an educated guess based on the theory that the machine we were using had to be at fault here.

We also observed that query time increased as the FPR increased for |K|=1000, but the reverse happen for |K|=500000, which we don't have a clear expanaation for yet. Best of our knowledge this is simply due to luck.

## Task 3

We noticed a similar linear relationship here wrt to the number of bits used vs the size of the underlying data structure.
 
On the other hand we couldn't find the connection between the query time and the false positive rate to be anything other than constant across FPR. We tried reproducing this with the number of bits and query time per key but to no avail. We could not get the right number whatever we tried. 

With respect to the size of the bloom filter we found that there was a bijection between have a TFPR of 1/2^i in the bloom filter and have i bits. It seems that the bloom filter and this idea are really then doing the same thing fundamentally, but implementing it with different paradigms in mind.


## Attached are the plots
