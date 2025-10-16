# Python Implementation of NQueens Recursive Backtracking Solver
## nqueens.py
Python script which has two processes: basic backtracking and forward-checking backtracking solvers on the nqueens CSP.  
To run the basic solver for n queens >> python3 nqueens.py basic n  
To run the forward-checking solver for n queens >> python3 nqueens.py forward n  
If the inproper arguments are supplied to the program it will terminate.  
## Implemenation
The solver is instantiated as a `NQueen` object. The object stores the current state of the backtracking algorithm:  
- **variables assignments**: Each queen's assignment is represented as a binary integer of size n. Each queen is given its own row. Its binary int will have a 1 in the row it is assigned. So Q<sub>0</sub> = 1000 will respresent Q<sub>0</sub> placed at row 0. <u>The MSB is row 0.</u> 
- **variable domains**: Each queen's domain is represented by a binary mask, with 1s represented rows the queen is able to be placed at. The domains are used for the forward checking pruning.
- **number of backtracks**: I counted a backtrack as an occurrence where the current queen was unable to make a legal assignment from its domain, so the solver backtracks and reassigns the previously assigned queen. At that moment I increment the backtrack counter
- `forward_checking` method: runs the forward checking procedure, parsing the unassigned queens domains. Given the current queens assignment, we prune the unassigned queens domains. Done via bitwise operation. Compute the rows and diagonals affected by the current assignment and remove those affected squares from each queen's domain. If a queen's domain becomes empty (0), we reassign the current queen to the next row. I did not count this is a backtrack because we are not changing a previous assignment. Instead we are changing the current assignment because we detected error early.- `check_contraints` method: ensures the current assignments this far do not break any constraints. DOne via bitwise operation similar to that in forward checking. 
- `basic_backtrack` and `forward_backtrack` methods: Run the respected solver. Both assign queens in order from (0, 1, ..., n). Basic assigns each queen starting at row 0 to row n. Forward only progresses on a queen assignment if it is in that queen's domain. 
#### Note:
Untested runtimes for for large n.
