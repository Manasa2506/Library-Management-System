import mysql.connector
mydb=mysql.connector.connect(host="localhost",user="root",passwd="adnan",database="LMS")
crsr=mydb.cursor()
crsr.execute("""create table if not exists student (
                id int(3) primary key,
                name varchar(30),
                grade int(3),
                sec char(2),
                bk_brwed varchar(50),
                date_brwed date,
                expctd_ret varchar(12),
                bk_condtn varchar(80),
                Fine int)""")
crsr.execute("""create table if not exists library (
                id int(3) primary key,
                bK_name varchar(30),
                genre varchar(10),
                author varchar(30),
                publsher varchar(30))""")
def studentadd():
    n=int(input("Enter the number of student you want to add: "))
    for i in range(n):
        try:
            d_id=int(input("Enter the id of the student"))
            name=input("Please enter the name of the student: ")
            grd=input("Enter the grade of the student: ")
            sec=input("Enter the sec of the student: ")
        except:
            studentadd()
        sql="insert into student(id,name,grade,sec) values(%s,%s,%s,%s)"
        val=(d_id,name,grd,sec)
        crsr.execute(sql,val)
def studentrem():
    crsr.execute("select* from student")
    d_id=int(input("Enter the id of the student you wish to remove"))
    try:
        crsr.execute("delete from student where id=%s",d_id)
        print("Done!")
    except:
        print("Error!")
def booksadd():
    try:
        n=int(input("Enter the number of books you want to add: "))
        for i in range(n):
            d_id=int(input("Enter the id of the books"))
            name=input("Please enter the name of the books: ")
            gen=input("Enter the genre of the books: ")
            auth=input("Enter the author of the books: ")
            pb=input("Enter the publisher of the books: ")
            sql="insert into library values(%s,%s,%s,%s,%s)"
            val=(d_id,name,gen,auth,pb)
            crsr.execute(sql,val)
    except:
        booksadd()
def bk_rq():
    dnr=int(input("Enter id of student: "))
    dnt=int(input("Enter the id of the books: "))
    crsr.execute("SELECT * FROM library")
    bkd = crsr.fetchall()
    bnm=""
    for i in bkd:
        if dnt==i[0]:
            bnm=i[1]
            break
        else:
            pass
    try:
        sql="""UPDATE student
               SET bk_brwed=%s,date_brwed=curdate(),expctd_ret=curdate()+10
               WHERE id=%s"""
        val=(bnm,dnr)
        crsr.execute(sql,val)
        print("Success")
        
    except:
        print("Invalid entry")
        bk_rq()
def alldet():
    print("student's Table")
    crsr.execute("SELECT * FROM student")
    myresult = crsr.fetchall()
    print()
    print()
    for x in myresult:
      print(x)
    print("books's table")
    crsr.execute("SELECT * FROM library")

    myresult = crsr.fetchall()
    crsr.execute("DESCRIBE student")
    colnm=crsr.fetchall()
    print(colnm)
    
    for x in myresult:
      print(x)
def main():
    mydb.commit()
    
    print("Choose one of the following functions by thier number")
    print("""
             1. Add student
             
             2. Remove student

             3. Add books

             4. all details

             5. Borrow books""")
    a=int(input(""))
    if a==1:
        studentadd()
        main()
    elif a==2:
        studentrem()
        main()
    elif a==3:
        booksadd()
        main()
    elif a==4:
        alldet()
        main()
    elif a==5:
        bk_rq()
        main()
    else:
        exit()
main()

