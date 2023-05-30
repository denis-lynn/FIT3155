# Denis Lynn 30580390

import sys
import numpy as np


def readfile(filepath):
    f = open(filepath, 'r')

    # Read Number Decision Variables
    f.readline()
    curr_line = f.readline().strip()
    num_dv = int(curr_line)

    # Read Number Constraints
    f.readline()
    curr_line = f.readline().strip()
    num_constraints = int(curr_line)

    # Read Objectives (Cj)
    f.readline()
    curr_line = f.readline().strip()
    objective_lst = curr_line.split(', ')
    objective_lst = list(map(float, objective_lst))
    objective_lst += num_constraints * [0.0]

    # Read LHS
    f.readline()
    constraints_LHS = []
    for i in range(num_constraints):
        curr_line = f.readline().strip()
        matrix_val = curr_line.split(', ')
        matrix_val = list(map(float, matrix_val))
        matrix_val += num_constraints * [0.0]
        matrix_val[i+2] = 1.0
        constraints_LHS.append(matrix_val)

    # Read RHS
    f.readline()
    constraints_RHS = []
    for _ in range(num_constraints):
        curr_line = f.readline().strip()
        constraints_RHS.append(float(curr_line))
    return num_dv, num_constraints, objective_lst, constraints_LHS, constraints_RHS


def tableau_simplex(num_dv, constraints_no, cj, lhs, rhs):
    # Create Initial Tableau
    optimal_objective = 0

    # Create basis list containing index of basis vars in Cj
    basis = []
    for i in range(constraints_no):
        basis.append(i + num_dv)

    # Initialise Cj - Zj (Net gain table)
    net_gain = calculate_cj_zj(lhs, basis, cj)

    # Maximise while net gain has max > 0
    while max(net_gain) > 0:
        # find pivots
        pivot_col_index = np.argmax(net_gain)
        theta = []
        for row in range(len(lhs)):
            div_elem = lhs[row][pivot_col_index]
            if div_elem == 0:
                theta.append(float('inf'))
            else:
                theta.append(rhs[row]/div_elem)
        pivot_row_index = theta.index(min([i for i in theta if i > 0]))

        # updating basis row
        basis[pivot_row_index] = pivot_col_index
        lhs, rhs = update_basis_row(lhs, rhs, pivot_row_index, pivot_col_index)

        # Do row operations to turn column into 0s
        lhs, rhs = update_other_rows(lhs, rhs, pivot_row_index, pivot_col_index)

        # update cj-zj
        net_gain = calculate_cj_zj(lhs, basis, cj)

        # update objective
        optimal_objective = calculate_optimal(rhs, basis, cj)

    # find optimal decisions
    optimal_decisions = []
    for i in range(len(basis)):
        if basis[i] < num_dv:
            optimal_decisions.append(rhs[i])
    return optimal_decisions, optimal_objective


def calculate_optimal(rhs, basis, cj):
    optimal = 0
    for row in range(len(rhs)):
        optimal += cj[basis[row]] * rhs[row]
    return optimal


def update_basis_row(lhs_matrix, rhs, row_index, col_index):
    key_elem = lhs_matrix[row_index][col_index]
    for i in range(len(lhs_matrix[row_index])):
        lhs_matrix[row_index][i] /= key_elem
    rhs[row_index] /= key_elem
    return lhs_matrix, rhs


def update_other_rows(lhs_matrix, rhs, pivot_row, pivot_col):
    # Find Gaussian Factor for row operations
    # Row(old) - factor * key_row(new) = Row(new)
    # Gauss factor is lhs[row][pivot_col_index]
    key_elem = lhs_matrix[pivot_row][pivot_col]
    gauss_factor = 0
    for row in range(len(lhs_matrix)):
        if row != pivot_row:
            gauss_factor = lhs_matrix[row][pivot_col]
            for col in range(len(lhs_matrix[row])):
                lhs_matrix[row][col] -= gauss_factor * lhs_matrix[pivot_row][col]
            rhs[row] -= gauss_factor * rhs[pivot_row]
    return lhs_matrix, rhs


def calculate_cj_zj(lhs_matrix, basis_table, cj):
    cj_minus_zj = []
    for col in range(len(cj)):
        curr_zj = 0
        for row in range(len(lhs_matrix)):
            dot_prod = lhs_matrix[row][col] * cj[basis_table[row]]
            curr_zj += dot_prod
        cj_minus_zj.append(cj[col] - curr_zj)
    return cj_minus_zj


def writefile(optimal_decisions_lst, optimal_objective):
    with open('lpsolution.txt', 'w') as f:
        f.write('# optimalDecisions' + '\n')
        optimal_decisions_lst = list(map(str, optimal_decisions_lst))
        f.write(', '.join(optimal_decisions_lst) + '\n')
        f.write('# optimalObjective' + '\n')
        f.write(str(optimal_objective))


if __name__ == '__main__':
    _, filename = sys.argv
    decision_vars, num_cons, Cj, LHS, RHS = readfile(filename)
    opt_dec, opt_obj = tableau_simplex(decision_vars, num_cons, Cj, LHS, RHS)
    writefile(opt_dec, opt_obj)


