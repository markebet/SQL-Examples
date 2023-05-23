### Part 4 Midterm ###

import sqlite3

'''Creating the tables'''
Student = '''
CREATE TABLE Student
(
 StudentID NUMBER(20) NOT NULL,
 Name VARCHAR2(25),
 Address VARCHAR2(25),
 GradYear NUMBER(4),

     PRIMARY KEY(StudentID)
);
'''

Course = '''
CREATE TABLE Course
(
 CName VARCHAR2(20) NOT NULL,
 Department VARCHAR2(25),
 Credits NUMBER(2),

     PRIMARY KEY(CName)
);
'''

Grade = '''
CREATE TABLE Grade
(
    CName VARCHAR2(20) NOT NULL,
    StudentID NUMBER(20) NOT NULL,
    CGrade NUMBER(5,2),

    PRIMARY KEY(CName, StudentID),

    FOREIGN KEY(StudentID)
     REFERENCES Student(StudentID),
    FOREIGN KEY(CName)
     REFERENCES Course(CName)
);
'''


'''Setting the connection'''
conn = sqlite3.connect('dsc450_midterm.db')
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS Student')
cursor.execute('DROP TABLE IF EXISTS Course')
cursor.execute('DROP TABLE IF EXISTS Grade')

'''Creating the table'''
cursor.execute(Student)
cursor.execute(Course)
cursor.execute(Grade)


''' Inersting the data to tables'''
insert1 = [
    "INSERT INTO Student VALUES(123, 'Chandler Muriel Bing','New York, NY',2010);",
    "INSERT INTO Student VALUES(124, 'Monica Muriel Geller','New York, NY',2011);",
    "INSERT INTO Student VALUES(125, 'Rosse Lee Geller','New York, NY',2012);",
    "INSERT INTO Student VALUES(126, 'Phoebe Ann Buffay','Jersey City, NJ',2011);",
    "INSERT INTO Student VALUES(127,'Joey Alexander Trbbiani','Millan, Italy',2013);",
    "INSERT INTO Student VALUES(128, 'Nora Grace Lu','Chicago, IL',2015);"
    ]

insert2 = [
    "INSERT INTO Course VALUES('Machine Learning', 'Computer Science',4);",
    "INSERT INTO Course VALUES('Database Management', 'Data Science',4);",
    "INSERT INTO Course VALUES('Calculus I', 'Mathematics',3);",        
    ]


insert3 = [
    "INSERT INTO Grade VALUES('Database Management',128,4.0);",
    "INSERT INTO Grade VALUES('Database Management', 125,3.7);",
    "INSERT INTO Grade VALUES('Calculus I', 126,3.0);",
    "INSERT INTO Grade VALUES('Calculus I', 127,2.7);",
    "INSERT INTO Grade VALUES('Calculus I', 123,3.1);",
    "INSERT INTO Grade VALUES('Calculus I', 125,3.8);",
    "INSERT INTO Grade VALUES('Database Management',126,3.0);"
    ]

for item in insert1:
    cursor.execute(item)
for item in insert2:
    cursor.execute(item)
for item in insert3:
    cursor.execute(item)

'''Setting the join'''
join_query = '''
SELECT temp1.SID AS SID, temp1.Name, temp1.Address, temp1.GradYear, course.CName, TEMP1.CGrade, Course.Department, Course.Credits
FROM(
    SELECT s.StudentID AS SID, s.Name AS Name, s.Address AS Address, s.GradYear AS GradYear, g.CName AS CName, g.CGrade AS CGrade
    FROM Student s
    LEFT OUTER JOIN Grade g ON s.StudentID = g.StudentID)
    temp1 LEFT OUTER JOIN Course ON TEMP1.CName = Course.CName
UNION
SELECT temp2.SID AS SID, Student.Name, Student.Address, Student.GradYear, temp2.CName, temp2.CGrade, temp2.Department, temp2.Credits
FROM(
    SELECT c.CName AS CName, c.Department AS Department, c.Credits AS Credits, g.StudentID AS SID, g.CGrade AS CGrade
    FROM Course c
    LEFT OUTER JOIN Grade g ON c.cname = g.cname) temp2 LEFT OUTER JOIN
Student ON temp2.SID = student.StudentID;
'''

res = cursor.execute(join_query)

conn.commit()
r1 = res.fetchall()
print(str(r1))


### Question B ###

with open('midterm_part4.txt', 'wb') as outfile:
    cursor = conn.cursor()
    for rows in cursor.execute(join_query):
        each_row = ','.join([str(i) for i in rows]) + '\n'
        outfile.write(each_row.encode())

outfile.close()


#### Question E.1 ###
cursor.execute('DROP VIEW allinfo')

view_query = cursor.execute('CREATE VIEW [allinfo] AS SELECT GradYear, CName, Department FROM Student, Course;')
view_query = cursor.execute('SELECT * FROM [allinfo]')

res1 = cursor.execute(
'SELECT Department, MAX(GradYear)FROM [allinfo] GROUP BY Department;'
    )

res2 = cursor.execute(
'SELECT Department, MIN(GradYear)FROM [allinfo] GROUP BY Department;'
    )

print(res1.fetchall())
print(res2.fetchall())

