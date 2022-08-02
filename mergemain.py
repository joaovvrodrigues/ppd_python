import random
import time
from celery import group
from mergesort import sort, merge

# Create a list of 1,000,000 elements in random order.
sequence = list(range(1000000))
random.shuffle(sequence)
start_time = time.time()

# Split the sequence (considering 16 processes)
# A works start a process per core
parts = 16
sub_size = len(sequence) // parts
subseqs = [sequence[i * sub_size:(i + 1) * sub_size] for i in range(parts - 1)]
subseqs.append(sequence[(parts - 1) * sub_size:])

# Ask the Celery workers to sort each sub-sequence.
# Use a group to run the individual independent tasks as a unit of work.
partials = group(sort.s(seq) for seq in subseqs)().get()

# Merge all the individual sorted sub-lists into our final result.
result = partials[0]
for partial in partials[1:]:
    result = merge(result, partial)
distrib_time = time.time() - start_time
print('Distributed mergesort took %.02fs' % (distrib_time))

# Do the same thing locally and compare the times.
start_time = time.time()
result = sort(sequence)
local_time = time.time() - start_time
print('Local mergesort took %.02fs' % (local_time))