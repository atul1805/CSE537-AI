import sys
import itertools

class Variable(object):
    id_count = 0 # The first ID is 1
    
    def __init__(self):
        Variable.id_count += 1
        self.id = Variable.id_count


def parse_file(filepath):
    # Read the layout file to the board array
    board = []
    fin = open(filepath)
    header = fin.readline().strip().split(' ')
    rows = int(header[0])
    cols = int(header[1])
    
    for i in xrange(rows):
        row = fin.readline().strip().split(',')
        if len(row) != cols:
            print ('Row %d is not consistent with header: '
                   'expected %d columns.' % (i, cols) )
            exit(-1)
        board.append([parse_cell(cell) for cell in row])
    
    fin.close()
    return board


def parse_cell(char):
    if char == 'X':
        return Variable() # Construct a new Variable with a unique ID
    return int(char)


def convert2CNF(board, output):
    # Interpret the number constraints
    rows = len(board)
    cols = len(board[0])
    clauses = []
    # Introduced variables have IDs beginning after the normal ones
    combo_id = Variable.id_count
    
    for i in xrange(rows):
        for j in xrange(cols):
            cell = board[i][j]
            if isinstance(cell, int):
                # Get neighboring variables
                vars = []
                for n in xrange(max(0, i - 1), min(rows - 1, i + 1) + 1):
                    for m in xrange(max(0, j - 1), min(cols - 1, j + 1) + 1):
                        neigh = board[n][m]
                        if isinstance(neigh, Variable):
                            vars.append(neigh.id)
                # Sanity check
                num_vars = len(vars)
                if cell > num_vars:
                    print ('Inconsistent board: cell %d,%d has value %d, '
                           'but only %d neighbor(s)!' % (i, j, cell, num_vars))
                    exit(-1)
                if num_vars == 0: # No variables are constrained by this cell
                    continue
                # Generate combinations which satisfy this cell's value.
                # Note: the outer loop still runs even if 0 negatives are
                # selected (i.e. num_vars == cell).
                combo_clause = []
                for negatives in itertools.combinations(xrange(num_vars),
                                                        num_vars - cell):
                    combination = list(vars) # Clone the vars list
                    # Negate the values selected to not have mines, if any
                    for k in negatives:
                        combination[k] = -combination[k]
                    # Generate clauses corresponding to this combination.
                    # A new variable (combo_id) is introduced to implement the
                    # num_vars-ary AND formula. It corresponds to the AND's
                    # output: if it is true, then each variable must be
                    # assigned as it is in the combination in order to satisfy.
                    # If it is false, all of the clause's combinations are
                    # satisfied regardless of assignments on the variables.
                    combo_id += 1
                    for v in combination:
                        clauses.append([-combo_id, v])
                    combo_clause.append(combo_id)
                # This clause indicates that at least one of the combinations
                # must be true in order to satisfy the overall formula.
                # It is simply a list of the output variable corresponding to
                # each combination, effectively implementing OR(combinations...)
                clauses.append(combo_clause)
    # Note that because the clauses for each numeric cell are simply appended,
    # The result is effectively AND(cell_constraints...).
    # The overall structure of the underlying constraints is:
    # AND(
    #   [OR(
    #     [AND([var for var in combination]) for combination in cell]
    #   ) for cell in board if cell != 'X']
    # )
    # By introducing variables for each combination, this has been encoded as
    # an equisatisfiable CNF in space linear in the underlying constraints.
    
    # Save the constraints to the specified output file
    fout = open(output, 'w')
    # Write the number of variables and clauses
    fout.write('p cnf %d %d\n' % (combo_id, len(clauses)))
    # Write the actual clauses
    for clause in clauses:
        fout.write(' '.join([str(v) for v in clause]) + ' 0\n')
    fout.close()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Layout or output file not specified.'
        exit(-1)
    board = parse_file(sys.argv[1])
    convert2CNF(board, sys.argv[2])
