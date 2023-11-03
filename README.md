# MealMe Code inteview

## Instructions

[**45 minutes**] Create a function that determines whether a store is currently open, given a dictionary representing it’s open hours for days of the week. Note that the closing time is exclusive, so if a store closes at 2100, then it is no longer open starting at 2100.

**Notes**:

- is_open(current_time: int, day: int, hours: dict) -> bool
- Input Arguments
  - **current_time**: range = [0, 2400)
  - **day**
    - range = [0, 6]
    - 0 is Sunday
  - **hours**
    - weekday keys
      - range = [0, 6]
      - 0 is Sunday, 6 is Saturday
    - **open**: range = [0, 2400)
    - **close**: range = [0, 2400)
    - **open != close**
    - The following can be true: **close < open**

Sample **hours** input:

```
// 0 is sunday
hours = {
0: [{"open": 800, "close": 1500}, {"open": 1700, "close": 200}],
2: [{"open": 800, "close": 1200}, {"open": 1500, "close": 2100}],
3: [{"open": 800, "close": 2100}],
4: [{"open": 800, "close": 0}],
5: [{"open": 800, "close": 2100}],
6: [{"open": 800, "close": 1300}, {"open": 1700, "close": 200}]
}
```

### Test cases

1. is_open(current_time=800, day=0)
   Should return: True
   Returns: True

2. is_open(current_time=1800, day=0)
   Should return: True
   Returns: True

3. is_open(current_time=1600, day=0)
   Should return: False
   Returns: False

4. is_open(current_time=100, day=1)
   Should return: True
   Returns: False

# Run & Test

```
python is_open.py
```
