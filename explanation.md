## simulate()

### 1. Loop through each package
```python
for pkg in self.packages:
```


---

### 2. Loop through each train
```python
for train in self.trains:
```
Try to assign a train to carry the current package.

---

### 3. Check if the train has enough capacity
```python
if pkg.weight > train.capacity:
    continue
```
Skip this train if it cannot carry the package due to weight limits.

---

### 4. Find a path from the train to the package's current location
```python
path_to_pkg = self.find_path(train.current_node, pkg.current_node)
```
Use a simple DFS-style recursive function to find any valid path.

---

### 5. Find a path from the package's current location to its destination
```python
path_to_dest = self.find_path(pkg.current_node, pkg.dest_node)
```
Again, use the same brute-force search method to find any path.

---

---

### 6. Move the train to the package's location
```python
for next_node in path_to_pkg[1:]:
```
- Iterate over each node in the path from the train current position to the packag location (excluding the first node since its the train's current position).
- This loop moves the train step by step

```python
    edge = self.find_edge(train.current_node, next_node)
```
- Look up the edge between the train's current node and the next node using `find_edge()`.
- This returns an `Edge` object which contains the travel time between the two nodes.

```python
    travel_time = edge.time_sec
```
- Retrieve the journey time in seconds from the edge.

```python
    self.moves.append(Move(time, train.name, train.current_node, [], next_node, []))
```
- Create a `Move` object representing this leg of the trip:
  - `time`: the current simulation time
  - `train.name`: the name of the train making the move
  - `train.current_node`: the starting station of this move
  - `[]`: the train picks up **no packages** on the way to the package
  - `next_node`: the station the train is traveling to
  - `[]`: the train drops off **no packages** on this leg
- Append this move to the `moves` list.

```python
    time += travel_time
```
- Update the current simulation clock to reflect the travel duration.

```python
    train.current_node = next_node
```
- Update the train's location to the node it just arrived at.

---

### Class: Move

```python
class Move:
    def __init__(self, time, train_name, from_node, picked, to_node, dropped):
        self.time = time
        self.train_name = train_name
        self.from_node = from_node
        self.picked = picked  
        self.to_node = to_node
        self.dropped = dropped

    def __repr__(self):
        return f"W={self.time}, T={self.train_name}, N1={self.from_node}, P1={self.picked}, N2={self.to_node}, P2={self.dropped}"
```

**Explanation**:
- `time`: the exact second when this move begins
- `train_name`: the name of the train making this move
- `from_node`: station the train starts from
- `picked`: list of package names picked up at `from_node`
- `to_node`: station the train is traveling to
- `dropped`: list of package names dropped off at `to_node`

The `__repr__()` method produces a clear, formatted line like:
```
W=1800, T=Q1, N1=A, P1=[K1], N2=B, P2=[]
```
This makes it easy to log and verify what each train is doing at every point in time.
```python
for next_node in path_to_pkg[1:]:
    edge = self.find_edge(train.current_node, next_node)
    travel_time = edge.time_sec
    self.moves.append(Move(time, train.name, train.current_node, [], next_node, []))
    time += travel_time
    train.current_node = next_node
```
Move step-by-step along the path. Record each movement, update the train’s location and current simulation time.

---

### 7. Pick up the package
```python
train.carrying.append(pkg)
pkg.current_node = train.current_node
```
Once the train is at the package’s node, it picks it up.

---

### 8. Move the train to the package’s destination
```python
for next_node in path_to_dest[1:]:
    edge = self.find_edge(train.current_node, next_node)
    travel_time = edge.time_sec
    self.moves.append(Move(time, train.name, train.current_node, [pkg.name], next_node, []))
    time += travel_time
    train.current_node = next_node
```
Transport the package to its destination node step-by-step, logging each leg of the journey.

---

### 9. Drop off the package
```python
self.moves.append(Move(time, train.name, train.current_node, [], train.current_node, [pkg.name]))
pkg.delivered = True
```
Drop off the package at the destination node. Mark it as delivered.

---

### Notes:
- current approach is  not optimized for shortest path 
- will use the first available train and first valid path.
- simple but works correctly as long as the network is connected.

### Improvement: 
- use djitskra to move the trains
- implementation need more time for rnd