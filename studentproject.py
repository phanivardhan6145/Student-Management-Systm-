#Features: Add, update, delete, and search student records.
import mysql.connector as db
con=db.connect(user='root',password='root',host='localhost',database='phani')
cursor=con.cursor(buffered=True)
admin='admin'
password=1234


def student_pre(stu_id):
    query='select count(*) from student where stu_id=%s'
    value=[stu_id]
    cursor.execute(query,value)
    count=cursor.fetchone()[0]
    
    return count

def user1_pre(stu_id):
    query='select count(*) from user1 where stu_id=%s'
    value=[stu_id]
    cursor.execute(query,value)
    count=cursor.fetchone()[0]
    
    return count

    
def add_student(stu_id,name,marks,phno):
    if not student_pre(stu_id):
        query='insert into student values(%s,%s,%s,%s)'
        values=[stu_id,name,marks,phno]
        cursor.execute(query,values)
        con.commit()
        
        print('student details added successfully')
        if student_pre(stu_id):
            if not user1_pre(stu_id):
                a=input('enter password:') 
                query='insert into user1 values(%s,%s)'
                
                values=[stu_id,a]
                cursor.execute(query,values)
                con.commit()
                
                print('password added successfully')
            else:
                print('password already created for this user')
        else:
            print('invalid user id')
   
      
    
        

def update_student(stu_id,marks):
    if student_pre(stu_id):
        if marks>0 and marks<101:
            query='update student set marks=%s where stu_id=%s'
            values=[marks,stu_id]
            cursor.execute(query,values)
            con.commit()
            print('marks updated successfully')
            
        else:
            print('enter valid marks')
    else:
        print('there is no student with that id')

def delete_student(stu_id):
    if user1_pre(stu_id):
        query='delete from user1 where stu_id=%s'
        value=[stu_id]
        cursor.execute(query,value)
        con.commit()
        if student_pre(stu_id):
            query='delete from student where stu_id=%s'
            value=[stu_id]
            cursor.execute(query,value)
            con.commit()
            print('student details deleted successfully')

            
    else:
        print('there is no student with that id')
    

def view_student(stu_id):
    if student_pre(stu_id):
        query='select *from student where stu_id=%s'
        value=[stu_id]
        cursor.execute(query,value)
        
        row=cursor.fetchone()
        print(row)
        
    else:
        print('there is no student with that id')

def view_allstudents():
    cursor.execute('select *from student')
    rows=cursor.fetchall()
    
    print(rows)
    

def create_pass(stu_id,password):
    if student_pre(stu_id):
        if user1_pre(stu_id):
            query='update user1 set password=%s where stu_id=%s'
            values=[password,stu_id]
            cursor.execute(query,values)
            con.commit()
            
            print('password reseted successfully')
        else:
            query='insert into user1 values(%s,%s)'
            values=[stu_id,password]
            cursor.execute(query,values)
            con.commit()
            print('password created successfully')
            
    else:
        print('invalid user id')

def check_password(stu_id):
    if student_pre(stu_id):
        if user1_pre(stu_id):
            a=input('enter password:')
            query='select password from user1 where stu_id=%s'
            value=[stu_id]
            cursor.execute(query,value)
            row=cursor.fetchone()
            
            if row and a==row[0]:
                return True
            else:
                print('wrong password')
                return False
        else:
            print('you want to create password first')
            return False
            
    return False
def see_grade(stu_id):
    if student_pre(stu_id):
        if check_password(stu_id):
            query='''select case when marks>90 then 'A'
                                when marks>75 then 'B'
                                when marks>65 then 'C'
                                when marks>55 then 'D'
                                else 'f' end as grade from student where stu_id=%s'''
            value=[stu_id]
            cursor.execute(query,value)
            row=cursor.fetchone()
            if row:
                print('Grade:',row[0])
            else:
                print('no marks for this student')
        else:
            pass
            #print('grade check failed due to wrong password')
    else:
        print('no data for that student id')

while True:
    print('*'*15,'STUDENT MANAGEMENT SYSTEM','*'*15)
    print('1.admin login')
    print('2.student login')
    print('3.exit')

    login_type=int(input('chose login type:'))
    if login_type==1:
        a=input('enter admin name:')
        b=int(input('enter password:'))
        if a==admin and b==password:
            while True:
                
                
                print('1.update_student')
                print('2.delete_student')
                print('3.view_student')
                print('4.view_allstudents')
                print('5.exit')

                choise=int(input('enter a number:'))

                

                if choise==1:
                    a=int(input('enter student id:'))
                    b=int(input('enter the updated marks of that student:'))
                    update_student(a,b)

                elif choise==2:
                    a=int(input('enter the student id you want to delete:'))
                    delete_student(a)

                elif choise==3:
                    a=int(input('enter student id:'))
                    view_student(a)

                elif choise==4:
                    print('student details')
                    view_allstudents()
                    
                elif choise==5:
                    print('exit')
                    break

                else:
                    print('invalid choise')
        else:
            print('invalid admin name or password')

    elif login_type==2:
        while True:
            print('1.add_student')
            print('2.reset password')
            print('3.check grade')
            print('4.exit')
            choise=int(input('select an option:'))

            if choise==1:
                    a=int(input('enter student id:'))
                    if student_pre(a):
                         print('student already present with that id')
                         continue
                    else:
                        b=input('enter student name:')
                        c=(int(input('enter student marks:')))
                        d=input('enter phno:')
                        if len(d)==10 and d.isdigit():
                            add_student(a,b,c,d)
                            continue
                        else:
                            print('enter valid phno')
                            break

            if choise==2:
                a=int(input('enter student id:'))
                b=input('enter password:')
                create_pass(a,b)

            elif choise==3:
                a=int(input('enter student id:'))
                see_grade(a)
            elif choise==4:
                print('exit')
                break
            else:
                print('choose correct option')
            
         
    elif login_type==3:
        print('exit')
        break
    else:
        print('choose correct login type')


con.close()
