# Leetcode Helper

### Leetcode solution organizer written in python3


# How to use
To creates question templates under `./solutions/`, including question readme, Python3 and C++ code snippet, and sample input.
<br>

```
# insice neovim
:!python3 ./src/create.py <number of question> <q id 1> <q id 2> ...
```

# for example, this create 3 dir under `./solutions/` for question 14, 88, 9
```
!python3 src/create.py 3 14 88 9
```

## Functionality (in progress)
1. Get/update leetcode questions database
    - question id
    - question description
    - starter code
    - sample testcase
2. Local dev environment
    - C++
    - Python3
    - Rust
    - etc
3. Auto test locally
4. Submit solution
5. Organize solution locally
6. Serialization of the helper object
