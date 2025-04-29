# Assignment: Design Patterns Implementation
This repository contains two Python scripts demonstrating the Singleton and Decorator design patterns:

**1. `single_redis.py`:** Implements a Singleton pattern for a Redis service.
**`decorator_pat.py`:** Implements a Decorator pattern for text output formatting with execution time logging.

## Files
### 1. `single_redis.py`
**Purpose:** Demonstrates the Singleton pattern by ensuring only one instance of a Redis service is created, verified by logging the instance's memory address.
#### Key Features:

- **Singleton Pattern:** Uses `__new__` to enforce a single RedisService instance.
- Connects to a Redis server at `localhost:6381`.
- Provides methods to `set` (set_value) and `get` (get_value) key-value pairs in `Redis`.
- Logs instance creation/reuse and memory addresses to confirm singleton behavior.

#### Usage:
1. Download redis-server from [official redis page](https://redis.io/downloads/)
2. Ensure Redis is installed and running on `localhost:6381`:
```
redis-server --port 6381
```

3. Install the Python Redis client:
```
pip install redis
```

4. Run the script:
```
python single_redis.py
```

**Expected output:**
```
$ python single_redis.py
INFO:__main__:Created new RedisService instance at 125817542852928
INFO:__main__:Set test_key = test_value
INFO:__main__:Returning existing RedisService instance at 125817542852928
INFO:__main__:Got test_key = test_value
INFO:__main__:Instance 1 ID: 125817542852928
INFO:__main__:Instance 2 ID: 125817542852928
INFO:__main__:Are instances same? True
```

### 2. decorator_pat.py
**Purpose:** Demonstrates the `Decorator pattern` by wrapping a text output class to produce bold HTML text, with a `timing decorator` to measure method execution time.

#### Key Features:

- **Decorator Pattern:**
**TextOutput:** Base class with a get_output method returning plain text.
**BoldTextDecorator:** Wraps TextOutput to add <b> tags, with an additional get_output_bold method for direct bold output.


**- Timing Decorator:** log_time measures and logs execution time for methods, using functools.wraps for proper function metadata preservation.
Long for loops (10M and 5M iterations) simulate heavy computation to make timing measurable.

#### Usage:
No external dependencies required (uses standard Python libraries).
**Run the script:**
```
python decorator_pat.py
```

**Expected output:**
```
$ python decorator_pat.py
INFO:__main__:Function 'get_output' took 1.1773 seconds to execute
INFO:__main__:Plain output: Hello, World!
INFO:__main__:Function 'get_output' took 0.7467 seconds to execute
INFO:__main__:Function 'get_output' took 1.1510 seconds to execute
INFO:__main__:Decorated output (get_output): <b>Hello, World!</b>
INFO:__main__:Function 'get_output_bold' took 0.3718 seconds to execute
INFO:__main__:Decorated output (get_output_bold): <b>Hello, World!</b>
```