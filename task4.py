def CommonSum(n):
    return int(n * (n ** 2 + 1) / 2)


def pmsList(n, pairList):
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
        problem.addConstraint(ExactSumConstraint(pair[1]), [pair[0]])
    bd = []
    for x in range(1, n):
        tmp = [i * n + i + x for i in range(n)]
        for y in range(n - x, n):
            tmp[y] -= n
        bd.append(tmp)
    for x in range(1, n):
        tmp = [i*n+(n-i-1)-x for i in range(n)]
        for y in range(n-x, n):
            tmp[y] += n
        bd.append(tmp)
    print(bd)
    for list in bd:
        problem.addConstraint(ExactSumConstraint(CommonSum(n)), list)
    return problem.getSolutions()


result =pmsList(4,[[0, 13], [1, 12], [2, 7]])
for item in result:
    print(item)
