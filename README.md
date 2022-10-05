# COMP24011 Labs

This is the base repo for COMP24011 labs in the academic session 2022-23.

There is a branch for each of the 4 lab assignments.
These are called: `lab1`, `lab2`, `lab3`, `lab4`.
To access the files for a lab you need to switch to the corresponding branch.
For example, you can use the command
```
git checkout lab1
```

Every branch has a refresh script to fetch the lab materials when they become available.
You **must** run this script before you start working on the assignment.
This can be done with the command
```
./refresh.sh
```

To submit your work you need to follow the coursework instructions in the [CS Handbook](https://wiki.cs.manchester.ac.uk/index.php/UGHandbook22:Coursework#Developing_and_submitting_with_Gitlab).
You **must** use the correct git tag which you can find in the manual for the lab.
This usually involves the following sequence of commands
```
git add -A .
git commit -m <A_COMMIT_MESSAGE>
git tag <CORRECT_TAG_FROM_MANUAL>
git push origin
git push --tags origin
```

Please ask for support in the lab sessions if you're unsure about lab instructions.
