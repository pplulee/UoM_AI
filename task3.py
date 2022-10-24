def CommonSum(n):
    return int(n * (n ** 2 + 1) / 2)


def msqList(n, pairList):
    from constraint import Problem, AllDifferentConstraint, ExactSumConstraint
    problem = Problem()
    problem.addVariables(range(0, n * n), range(1, n * n + 1))
    problem.addConstraint(AllDifferentConstraint(), range(0, n * n))
    for row in range(n):
        problem.addConstraint(ExactSumConstraint(CommonSum(n)),
                              [row * n + i for i in range(n)])
    for col in range(n):
        problem.addConstraint(ExactSumConstraint(CommonSum(n)),
                              [col + n * i for i in range(n)])
    problem.addConstraint(ExactSumConstraint(CommonSum(n)), [i * n + i for i in range(n)])  # diagonal
    problem.addConstraint(ExactSumConstraint(CommonSum(n)), [i * n + (n - i - 1) for i in range(n)])  # diagonal
    for pair in pairList:
        problem.addConstraint(ExactSumConstraint(pair[1]),[pair[0]])
    return problem.getSolutions()



print(msqList(4, [[0, 13], [1, 12], [2, 7]]))
