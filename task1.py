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

# 1 | Olga is leaving 2 hours before the traveller from Yemen.
for person in people:
    problem.addConstraint(
        (lambda x, y, z: (y != "yemen") or
                         ((x == "4:30") and (z == "2:30")) or
                         ((x == "5:30") and (z == "3:30"))),
        ["t_" + person, "d_" + person, "t_olga"])
#
# 2 | Claude is either the person leaving at 2:30 pm or the traveller leaving at 3:30 pm.
problem.addConstraint(lambda x: (x == "2:30") or (x == "3:30"), ["t_claude"])

# 3 | The person leaving at 2:30 pm is flying from Peru.
for person in people:
    problem.addConstraint(lambda x, y: (x != "2:30") or (y == "peru"), ["t_" + person, "d_" + person])

# 4 | The person flying from Yemen is leaving earlier than the person flying from Taiwan.
for person in people:
    for person2 in people:
        problem.addConstraint(lambda x, y, t1, t2: (x != "yemen") or (y != "taiwan") or (int(t1[0]) < int(t2[0])),
                              ["d_" + person, "d_" + person2, "t_" + person, "t_" + person2])
#
# 5 | The four travellers are Pablo, the traveller flying from Yemen, the person leaving at 2:30 pm and the person leaving at 3:30 pm.
# Pablo is not flying from Yemen and is leaving at neither 2:30 nor 3:30.
# whoever is flying from Yemen is likewise leaving at neither 2:30 nor 3:30.
problem.addConstraint(lambda x, y: (x != "yemen") and (y not in ["2:30", "3:30"]), ["d_pablo", "t_pablo"])
for person in people:
    if person == "pablo":
        continue
    problem.addConstraint(lambda x, y: (x != "2:30") or (x != "3:30") or (y == "yemen"), ["t_" + person, "d_" + person])
solns = problem.getSolutions()
for item in solns:
    print(item)
