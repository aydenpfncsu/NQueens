import sys

class NQueen:
    def __init__(self, num_queens):
        # each queen has its own column, and can be placed in row 0,...,n-1
        # store the location of each queen as a bit string, with a 1 where Qi is located
        # list to store bit string of Qi for i=0,...,n-1. Initially all rows are empty; no assignments
        self.queens = [0] * num_queens
        # list to store the domains of Qi, with a 1 indicating Qi can be placed at that position in its column
        self.domains = [(1 << num_queens)-1] * num_queens
        # store n
        self.n = num_queens
        # store number of backtracks
        self.backtracks = 0

    def forward_checking(self, q):
        """Performs forward checking."""

        # get current queens assignment
        q_mask = self.queens[q]

        # update domains of all future queens
        for j in range(q+1, self.n):
            # calculate all rows and diagonals affected by the current queens row
            # current row must be removed from future queens domains
            attack_rows = q_mask
            # standardize diagonals with respect to current queen and jth queen
            attack_main_diag = q_mask >> (j - q)
            attack_anti_diag = q_mask << (j - q)
            # calculate mask of all rows that are unavailable
            attack_mask = attack_rows | attack_main_diag | attack_anti_diag
            # update jth queen's domain by masking out the rows that are unavailable
            self.domains[j] &= ~attack_mask

            # if new domain is empty, we can backtrack early
            if self.domains[j] == 0:
                return False

        return True

    def check_constraints(self, assigned):
        """Ensures the current assignment does not break the constraints"""
        # store mask for assigned row locations; if two variables are assigned to the same row (both are 1) then invalid.
        row_mask = 0
        # store masks for main and anti diagonals; 1 indicates that diagonal is already occupied
        main_diag_mask = 0
        anti_diag_mask = 0

        # iterate over the queens that have been assigned
        for q in assigned:
            # get assignment mask of the given queen
            q_mask = self.queens[q]
            # check if a queen has already been assigned to the current queens row
            if row_mask & q_mask: 
                # row has multiple queens
                return False
            # add current queen row to the total queens mask
            row_mask |= q_mask

            # check the main diagonals for conflicts
            # shift current queen mask to standardize its main diagonal
            standard_main = q_mask << q
            if main_diag_mask & standard_main:
                # diagonal has multiple queens
                return False
            main_diag_mask |= standard_main

            # check anti diagonals for confilcts
            standard_anti = q_mask << self.n - 1 - q 
            if anti_diag_mask & standard_anti:
                # diagonal has multiple queens
                return False
            anti_diag_mask |= standard_anti

        # no conflicts detected
        return True
    
    def basic_backtrack(self, q, assigned):
        """Runs the basic recursive backtracking algorithm."""
        # base case - all queens have been assigned and valid
        if q == self.n:
            return assigned
        # n total assignments for a given queen, right shift by 1 for each dif assn 
        for row in range(self.n):
            # assign queen to current row
            self.queens[q] = 1 << (self.n - 1 - row)
            assigned.add(q)

            # check if assignment breaks constraints
            if self.check_constraints(assigned): # assignment valid
                # assign next queen
                result = self.basic_backtrack(q+1, assigned)
                if result:
                    return result
         
            # pop queen from assigned list and reset its assignment
            self.queens[q] = 0
            assigned.remove(q)

        # no assignment works for this queen, must backtrack
        self.backtracks += 1
        return None

    def forward_backtrack(self, q):
        """Runs the recursive backtracking algorithm with forward checking."""
        # base case - all queens have been assigned and valid
        if q == self.n:
            return self.queens
        
        # instantiate a copy of the current domains if forward checking finds failure
        copy_domains = self.domains.copy()

        # iterate over the rows
        for row in range(self.n):
            # assign queen to current row
            q_mask = 1 << (self.n - 1 - row)
            # check if current assignment is in the queen's domain
            if q_mask & self.domains[q]:
                self.queens[q] = q_mask

                # perform forward checking given the assignment
                if self.forward_checking(q):
                    result = self.forward_backtrack(q+1)
                    if result: 
                        return result
                # forward check failed, restore original domains
                self.domains = copy_domains

        # no assignments work, backtrack
        self.queens[q] = 0
        self.backtracks += 1
        return None


    def solve(self, basic):
        """Solve N Queens with the given bracktracking strategy."""
        if basic:
            assigned = self.basic_backtrack(0, set())
            if assigned:
                return self.queens
        else:
            return self.forward_backtrack(0)


def main():
    """Main entrypoint of the program."""
    # ensure correct number of arguments passed in (2)
    if len(sys.argv) != 3:
        sys.stdout.write("Incorrect Args; prgm exit\n")
        sys.exit()

    # parse which type of search user is requesting; basic or forward
    search = sys.argv[1]
    if search not in ["basic", "forward"]:
        sys,stdout.write("Incorrect backtracking prompt; either basic or forward; prgm exit\n")
        sys.exit()
    
    # build CSP for the n queens
    num_queens = int(sys.argv[2])
    csp = NQueen(num_queens)

    # solve the N Queens problem
    result = csp.solve(search == "basic")

    sys.stdout.write("Solution: ")
    for q, mask in enumerate(result):
        row = (mask.bit_length()-1)
        sys.stdout.write(f"Q{q} = {num_queens - 1 - row}, ")
    
    sys.stdout.write(f"\nBacktrack count: {csp.backtracks}\n")

if __name__ == "__main__":
    main()
