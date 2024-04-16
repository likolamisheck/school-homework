

import random


class CacheLine:
      
    def __init__(self, tag):
        self.tag = tag
        self.state = 'I'  # Initial state: Invalid



class CacheSet:
    def __init__(self, associativity):
        self.lines = [CacheLine(None) for _ in range(associativity)]
        self.associativity = associativity
        

class Cache:
    def __init__(self, num_sets, associativity):
        self.num_sets = num_sets
        self.sets = [CacheSet(associativity) for _ in range(num_sets)]
        

class Memory:
    def __init__(self, size):
        self.size = size
        self.data = [0] * size


class Processor:
    def __init__(self, pid, cache):
        self.pid = pid
        self.cache = cache
        

class CacheModel:
    def __init__(self, num_processors, memory_size, cache_size, num_sets, associativity):
        self.num_processors = num_processors
        self.memory = Memory(memory_size)
        self.processors = [Processor(pid, Cache(num_sets, associativity)) for pid in range(num_processors)]
        self.cache_size = cache_size

    def read(self, processor_id, address):
        processor = self.processors[processor_id]
        cache = processor.cache
        set_index = address % len(cache.sets)
        tag = address // len(cache.sets)
        cache_set = cache.sets[set_index]


        for line in cache_set.lines:
            if line.tag == tag:
                if line.state in ['M', 'O', 'E', 'S']:
                    return True  # Cache hit
                elif line.state == 'I':
                    line.state = 'S'  # Update state to Shared
                    return False  # Cache miss

        # Cache miss, randomly choose a line to replace
        replaced_line_index = random.randint(0, cache.sets[0].associativity - 1)
        replaced_line = cache_set.lines[replaced_line_index]
        replaced_line.tag = tag
        replaced_line.state = 'S'  # Set state to Shared
        return False

    def write(self, processor_id, address):
        processor = self.processors[processor_id]
        cache = processor.cache
        set_index = address % len(cache.sets)
        tag = address // len(cache.sets)
        cache_set = cache.sets[set_index]

        for line in cache_set.lines:
            if line.tag == tag:
                if line.state in ['M', 'O', 'E']:
                    return True  # Cache hit
                elif line.state in ['I', 'S']:
                    line.state = 'M'  # Set state to Modified
                    return False  # Cache miss

        # Cache miss, randomly choose a line to replace
        replaced_line_index = random.randint(0, cache.sets[0].associativity - 1)
        replaced_line = cache_set.lines[replaced_line_index]
        replaced_line.tag = tag
        replaced_line.state = 'M'  # Set state to Modified
        return False

# Example usage


cache_model = CacheModel(num_processors=4, memory_size=16, cache_size=4, num_sets=4, associativity=2)

# Perform some random read and write operations
for _ in range(20):
    processor_id = random.randint(0, 3)
    operation = random.choice(['read', 'write'])
    address = random.randint(0, 15)
    if operation == 'read':
        cache_hit = cache_model.read(processor_id, address)
    else:
        cache_hit = cache_model.write(processor_id, address)
    print(f"Processor {processor_id} performed a {'read' if operation == 'read' else 'write'} operation at address {address}. Cache hit: {cache_hit}")



# Output cache contents
print("\nCache Contents:")
for i, cache_set in enumerate(cache_model.processors[0].cache.sets):
    print(f"Set {i}: ", end="")
    for line in cache_set.lines:
        print(f"[{line.tag}, {line.state}] ", end="")
    print()
