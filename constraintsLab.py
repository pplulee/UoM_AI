#!/usr/bin/env python3


# Task 1    
def Travellers(List):
    from constraint import Problem, AllDifferentConstraint

    problem = Problem()
    people = ["claude", "olga", "pablo", "scott"]
    times = ["2:30", "3:30", "4:30", "5:30"]
    destinations = ["peru", "romania", "taiwan", "yemen"]
    t_variables = list(map(lambda x: "t_" + x, people))
    d_variables = list(map(lambda x: "d_" + x, people))
    problem.addVariables(t_variables, times)
    problem.addVariables(d_variables, destinations)
    problem.addConstraint(AllDifferentConstraint(), t_variables)
    problem.addConstraint(AllDifferentConstraint(), d_variables)

    # # 1 | Olga is leaving 2 hours before the traveller from Yemen.
    for person in people:
        problem.addConstraint(
            (lambda x, y, z: (y != "yemen") or
                             ((x == "4:30") and (z == "2:30")) or
                             ((x == "5:30") and (z == "3:30"))),
            ["t_" + person, "d_" + person, "t_olga"])
    # 2 | Claude is either the person leaving at 2:30 pm or the traveller leaving at 3:30 pm.
    problem.addConstraint(lambda x: (x == "2:30") or (x == "3:30"), ["t_claude"])

    # 3 | The person leaving at 2:30 pm is flying from Peru.
    for person in people:
        problem.addConstraint(lambda x, y: (x != "2:30") or (y == "peru"), ["t_" + person, "d_" + person])

    # 4 | The person flying from Yemen is leaving earlier than the person flying from Taiwan.
    for person in people:
        for person2 in people:
            if person == person2:
                continue
            problem.addConstraint(lambda x, y, t1, t2: (x != "yemen") or (y != "taiwan") or (int(t1[0]) < int(t2[0])),
                                  ["d_" + person, "d_" + person2, "t_" + person, "t_" + person2])

    # 5 | The four travellers are Pablo, the traveller flying from Yemen, the person leaving at 2:30 pm and the person leaving at 3:30 pm.
    # Pablo is not flying from Yemen and is leaving at neither 2:30 nor 3:30.
    # whoever is flying from Yemen is likewise leaving at neither 2:30 nor 3:30.
    problem.addConstraint(lambda x, y: (x != "yemen") and (y not in ["2:30", "3:30"]), ["d_pablo", "t_pablo"])
    for person in people:
        if person == "pablo":
            continue
        problem.addConstraint(lambda x, y: (x != "2:30") or (x != "3:30") or (y == "yemen"),
                              ["t_" + person, "d_" + person])
    # extra constraint
    for constraint in List:
        problem.addConstraint(lambda x: x == constraint[1], ["t_" + constraint[0]])
    return problem.getSolutions()


# Task 2
def CommonSum(n):
    return int(n * (n ** 2 + 1) / 2)


# Task 3
def msqList(n, pairList):
    from constraint import Problem, AllDifferentConstraint, ExactSumConstraint
    problem = Problem()
    sum = CommonSum(n)
    problem.addVariables(range(0, n * n), range(1, n * n + 1))
    problem.addConstraint(AllDifferentConstraint(), range(0, n * n))
    for row in range(n):
        problem.addConstraint(ExactSumConstraint(sum),
                              [row * n + i for i in range(n)])
    for col in range(n):
        problem.addConstraint(ExactSumConstraint(sum),
                              [col + n * i for i in range(n)])
    problem.addConstraint(ExactSumConstraint(sum), [i * n + i for i in range(n)])  # diagonal
    problem.addConstraint(ExactSumConstraint(sum), [i * n + (n - i - 1) for i in range(n)])  # diagonal
    for pair in pairList:
        problem.addConstraint(ExactSumConstraint(pair[1]), [pair[0]])
    return problem.getSolutions()


# Task 4
def pmsList(n, pairList):
    from constraint import Problem, AllDifferentConstraint, ExactSumConstraint
    problem = Problem()
    sum = CommonSum(n)
    problem.addVariables(range(0, n * n), range(1, n * n + 1))
    problem.addConstraint(AllDifferentConstraint(), range(0, n * n))
    for row in range(n):
        problem.addConstraint(ExactSumConstraint(sum),
                              [row * n + i for i in range(n)])
    for col in range(n):
        problem.addConstraint(ExactSumConstraint(sum),
                              [col + n * i for i in range(n)])
    problem.addConstraint(ExactSumConstraint(sum), [i * n + i for i in range(n)])  # diagonal
    problem.addConstraint(ExactSumConstraint(sum), [i * n + (n - i - 1) for i in range(n)])  # diagonal
    for pair in pairList:
        problem.addConstraint(ExactSumConstraint(pair[1]), [pair[0]])
    bd = []
    for x in range(1, n):
        tmp = [i * n + i + x for i in range(n)]
        for y in range(n - x, n):
            tmp[y] -= n
        bd.append(tmp)
    for x in range(1, n):
        tmp = [i * n + (n - i - 1) - x for i in range(n)]
        for y in range(n - x, n):
            tmp[y] += n
        bd.append(tmp)
    for list in bd:
        problem.addConstraint(ExactSumConstraint(sum), list)
    return problem.getSolutions()


# Debug
if __name__ == '__main__':
    print("debug run...")
