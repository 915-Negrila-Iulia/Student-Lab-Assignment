### Student Lab Assignment
Application that manages student lab assignments for a discipline. The application stores:
- **Student**: `student_id`, `name`, `group`
- **Assignment**: `assignment_id`, `description`, `deadline`
- **Grade**: `assignment_id`, `student_id`, `grade_value`

Application allows to:
1. Manage students and assignments. The user can add, remove, update, and list both students and assignments.
2. Give assignments to a student or a group of students. In case an assignment is given to a group of students, every student in the group will receive it. In case there are students who were previously given that assignment, it will not be assigned again.
3. Grade student for a given assignment. When grading, the program allows the user to select the assignment that is graded, from the student’s list of ungraded assignments. A student’s grade for a given assignment cannot be changed. Deleting a student removes their assignments. Deleting an assignment also removes all grades at that assignment.
4. Statistics:
    - All students who received a given assignment, ordered by average grade for that assignment.
    - All students who are late in handing in at least one assignment. These are all the students who have an ungraded assignment for which the deadline has passed.
    - Students with the best school situation, sorted in descending order of the average grade received for all assignments.
5. Unlimited undo/redo functionality. Each step will undo/redo the previous operation performed by the user. Undo/redo operations cascade and have a memory-efficient implementation (no superfluous list copying)

Also implemented:\
1.Exception classes, PyUnit test cases for all non-UI classes and methods, Specifications.\
2. Persistent storage for all entities using file-based repositories. A `settings.properties` file to configure the application. The program works the same way using in-memory repositories, text-file repositories and binary file repositories. The decision of which repositories are employed, as well as the location of the repository input files are made in the program’s `settings.properties` file.\
3. Python module that contains an iterable data structure, a sort method(based on shell sort) and a filter method(contains 2 parameters: the list to be filtered, and an acceptance function that decided whether a given value passes the filter), together with complete PyUnit unit tests (100% coverage). The module is reusable in other projects. This data structure is used for storing objects in the repository and both functions are used in the repository and service layers.\
4. Implemented a graphical user interface, in addition to the menu-driven UI. Program can be started with either UI, without changes to source code. GUI is implemented in a declarative approach, using Qt Designer.

