import math
from collections import deque, defaultdict

#THIS IS THE PROBLEM WE HAVE TO COVER ALL CROSS  PATH
print("Robot has 3 containers: Fox, Chicken, Chicken-feed, crossing the river")
print("Conditions:")
print("  - Fox eats Chicken if left alone")
print("  - Chicken eats Feed if left alone")
print("Robot must avoid these states by carrying items carefully.")
scenario = 4
cond = int(math.pow(2, scenario))
print("TOTAL NUMBER OF STATES:", cond)

states = []
for i in range(cond):
    binarycon = format(i, '04b')
    state = [1 if bit == '1' else 0 for bit in binarycon]
    states.append(state)
    display = ['F' if bit == 1 else 'N' for bit in state]
    print(f"{i:>2} |  {display[0]} | {display[1]} | {display[2]} | {display[3]} || {binarycon} | {''.join(display)}")

# Check if a state is safe
def is_safe(state):
    robot, fox, chicken, feed = state
    if fox == chicken and robot != fox:
        return False
    if chicken == feed and robot != chicken:
        return False
    return True

# Filter valid states
print("\nValid (Safe) States:")
safe_states = []
for state in states:
    if is_safe(state):
        binary = ''.join(str(bit) for bit in state)
        readable = ['F' if b == 1 else 'N' for b in state]
        print(f"State: {binary} | {' '.join(readable)}")
        safe_states.append(binary)

# Divide into Row_A and Row_B
def count_ones(binary):
    return binary.count('1')

row_A = safe_states[:len(safe_states)//2]
row_B = [s for s in safe_states[len(safe_states)//2:] if count_ones(s) in [2, 3] or s == "1111"]

print("\nRow_A First_Division")
print(row_A)
print("Row_B Second_Division")
print(row_B)

# Map letters to state binaries
dic = {
    "ROW_A": {
        'A': row_A[0],
        'B': row_A[1],
        'C': row_A[2],
        'D': row_A[3],
        'E': row_A[4],
    },
    "ROW_B": {
        'F': row_B[0],
        'G': row_B[1],
        'H': row_B[2],
        'I': row_B[3],
        'J': row_B[4],
    }
}

final_paths = [
    ['A', 'F', 'G', 'H', 'I'],
    ['B', 'G', 'H', 'J'],
    ['C', 'F', 'G', 'I', 'J'],
    ['D', 'H', 'I', 'J'],
    ['E', 'H', 'J']
]

# Print each path with binary state
print("\nEACH TRANSITIONS OF Row_A -> ROW_B:\n")
for path in final_paths:
    print(" -> ".join(path))
    binary = [dic["ROW_A"].get(p, dic["ROW_B"].get(p, '----')) for p in path]
    print("Binary: ", " -> ".join(binary))

paths = {}
for path in final_paths:
    start = path[0]
    links = path[1:]
    paths[start] = links

a_links = set(paths['A'])

print("\n--- Nodes Sharing Links with A (F → G → H → I) ---")
for node in ['B', 'C', 'D', 'E']:
    if node in paths:
        common = a_links.intersection(paths[node])
        print(f"{node} shares with A:", " → ".join(common) if common else "None")
    else:
        print(f"{node} not found in path dictionary")


graph = defaultdict(list)

edges = [
    ('A', 'F'), ('A', 'G'), ('A', 'H'), ('A', 'I'),
    ('B', 'G'), ('B', 'H'), ('B', 'J'),
    ('C', 'F'), ('C', 'G'), ('C', 'I'), ('C', 'J'),
    ('D', 'H'), ('D', 'I'), ('D', 'J'),
    ('E', 'H'), ('E', 'J')
]

for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)

# BFS to find all paths from A to J
def bfs_all_paths(start, goal):
    queue = deque([[start]])
    all_paths = []

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == goal:
            all_paths.append(path)
            continue

        for neighbor in graph[node]:
            if neighbor not in path:
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return all_paths

all_paths = bfs_all_paths('A', 'J')

print("\n*******************")
print("We have to go to our goal -----> It will have many paths to reach as we make a network")
print("FROM A -> (F, G, H, I)")
print("All correct paths from A to J:\n")

for i, path in enumerate(all_paths, 1):
    print(f"{i}. {' -> '.join(path)}")
    print("\nTotal Paths Found:", i)



