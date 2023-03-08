import os

import mysql.connector

# Creating the connecting with MySQL

sqldb = mysql.connector.connect(
    host='localhost', user='root', password='0000', database='boutique')

mycur = sqldb.cursor()


class Boutique:

    def space(self):
        for i in range(1):
            print()

    # Check if customer exist in database or not

    def check(self):
        qry = "Select cust_id from customer"
        mycur.execute(qry)
        d = mycur.fetchall()
        list_of_ids = []
        for ids in d:
            list_of_ids.append(ids[0])
        return list_of_ids

    # Creating new account

    def customer_acoount(self):
        ask = 'Y'
        list_of_ids = self.check()
        while ask in 'yY':
            custid = int(input('Enter your customer id...   '))
            if custid in list_of_ids:
                print('This Customer Id already exists....\Try creating a new one')
            else:
                c_det = ()
                cnam = input('First Name : ')
                clnam = input('Last Name : ')
                cphno = input('Phone Number : ')
                cadrs = input('Your Address : ')
                c_det = (custid, cnam, clnam, cphno, cadrs)

                qry = 'insert into customer values(%s,%s,%s,%s,%s,NULL);'
                val = c_det

                mycur.execute(qry, val)
                sqldb.commit()
                print('Customer details entered')
                ask = input('Do you want to continue (Y/N) ')
                if ask not in ('Yy'):
                    self.space()
                    break

    # Get booked product

    def get_bkd_pro(self, cust_id):
        qry = 'select bkd_pro from customer where cust_id=%s;'
        mycur.execute(qry, (cust_id,))
        bp = mycur.fetchone()
        bkd_pro = bp[0]
        print(bkd_pro)
        return bkd_pro

    # Cutomer Sign-In

    def sign_in(self):
        try:
            ask = int(input('Enter customer ID to sign in : '))
            list_of_ids = self.check()
            if ask in list_of_ids:
                while True:
                    print(''' Do you want to :                                                                
                         1) View Bookings
                         2)  Book a product
                         3)  Update Self Details
                         4)  Cancel booked product
                            enter 'back' to exit ''')
                    ccc = input('enter choice -  ')
                    if ccc == '1':
                        s = self.get_bkd_pro(ask)
                        if s is None or s == '':
                            print('you have not booked product yet')
                        else:
                            ''' If more than one product are booked,
                            their IDs are stored as a single value
                            separated by '_' so we have to split the
                            string to print each product ID.'''
                            d = s.split('_')
                            print('Booked product')

                            for bkditems in d:
                                print(bkditems)
                    if ccc == '2':
                        qry = 'select pro_id from product;'
                        mycur.execute(qry)
                        pro_list = mycur.fetchall()

                        list_of_product = []
                        for i in pro_list:
                            list_of_product.append(i[0])
                        pro_id = input(
                            'Enter the product id to book product :')
                        if pro_id in list_of_product:
                            qry = 'select bkd_pro from customer where cust_id=%s;'
                            mycur.execute(qry, (ask,))
                            pr = mycur.fetchone()
                            prl = pr[0]
                            if prl is None or prl == ' ':
                                qry = 'update customer set bkd_pro=%s where cust_id=%s;'
                                val = (pro_id+'_', ask)
                                mycur.execute(qry, val)
                                sqldb.commit()
                                print('Your Product is booked !!')
                            else:
                                prl1 = prl+pro_id
                                qry2 = 'update customer set bkd_pro=%s where cust_id=%s;'
                   # val2 is the new value containing all booked product
                   # to be stored in the column
                                val2 = (prl1+'_', ask)
                                mycur.execute(qry2, val2)
                                sqldb.commit()
                                print('Your Product is booked !!')

                        else:
                            print('This product does not exists.\
                                    Please write the correct product id!')

                    if ccc == '3':
                        try:
                            qry = 'select cust_id,c_nam,c_lnam,c_phno,c_adrs\
                                      from customer where cust_id =%s'
                            mycur.execute(qry, (ask,))

                            clist = mycur.fetchone()

                            flds = ['Name', 'Last Name', 'Ph.No', 'Address']
                            dic = {}
                            print("Your existing record is :")

                            for i in range(4):
                                dic[flds[i]] = clist[i+1]
                                print(i+1, '    ',
                                      flds[i], '  :  ', clist[i+1])
                            for i in range(len(clist)):
                                updtc = int(input('enter choice to update '))
                                upval = input('enter'+flds[updtc-1]+'   ')
                                dic[flds[updtc-1]] = upval
                                yn = input(
                                    'Do you want to update other details? y or n ')
                                if yn in 'Nn':
                                    break
                            qry = 'update customer set c_nam=%s,c_lnam=%s,c_phno=%s,c_adrs=%s where cust_id=%s;'
                            updtl = tuple(dic.values())+(ask,)
                            val = (updtl)
                            mycur.execute(qry, val)
                            sqldb.commit()
                            print('Your details are updated ')
                        except Exception as e:
                            print("Error occured is :", e)

                    if ccc == '4':
                        try:
                            bkd_pro = self.get_bkd_pro(ask)
                            print('Your Booking(s)  : \n  ', bkd_pro)
                            if bkd_pro is None or bkd_pro == ' ':
                                print('you have no bookings to cancel')
                            else:
                                cw = input(
                                    "To cancel all product; enter A \nOR \enter the product code to cancel :  ")
                                if cw in 'Aa':
                                    qry = 'update customer set bkd_pro=NULL where cust_id=%s'
                                    mycur.execute(qry, (ask,))
                                    sqldb.commit()
                                    print('All bookings deleted')

                                elif cw in bkd_pro:
                                    x = (bkd_pro[0:-1]).split('_')
                                    x.remove(cw)
                                    updt_pro = ''
                                    for item in x:
                                        updt_pro = updt_pro+item+'_'
                                    qry = 'update customer set bkd_pro=%s where cust_id=%s'
                                    val = (updt_pro, ask)
                                    mycur.execute(qry, val)
                                    sqldb.commit()
                                    print('Booking Cancelled !')
                        except Exception:
                            print('Some problem in updating details.Try again')
                    if ccc.lower() == 'back':
                        print("Successfully logged out")
                        self.space()
                        break
            else:
                print('This Account does not exist. ')
        except Exception:
            print('Some error occurred. Try Again')

# View Product Function

    def view_pro(self):
        qry = 'select * from product;'
        mycur.execute(qry)
        d = mycur.fetchall()

        dic = {}

        for i in d:
            dic[i[0]] = i[1:]
        print('_'*80)

        print("{:<17} {:<22} {:<23} {:<19}".format(
            'Product id', 'Product name', 'Price', 'Stock'))
        print('_'*80)
        for k, v in dic.items():
            a, b, c = v
            print("{:<17} {:<22} {:<23} {:<19}".format(k, a, b, c))
        print('_'*80)

# Add Product

    def addpro(self):
        self.view_pro()
        n = int(input('Enter no of items to insert  '))
        for j in range(n):
            t = ()
            pronum = input("Product No.  ")
            proid = input('Product ID :  ')
            pprice = int(input('Price : '))
            pstk = int(input('Stock : '))
            t = (pronum, proid, pprice, pstk)

            qry = 'insert into product values(%s,%s,%s,%s);'
            val = t
            mycur.execute(qry, val)
            sqldb.commit()
            print("Product Added")


# Deleting a Product


    def delpro(self):
        self.view_pro()
        delt = input("Enter ID of product to be deleted")
        qry = 'delete from product where pro_id=%s;'
        mycur.execute(qry, (delt,))
        sqldb.commit()
        print("Product is deleted")

# Employee Login
    def emp_sign_in(self):
        try:
            ask = input('Enter id to sign in to the account :   ')
            qry = 'select emp_id from employee;'
            mycur.execute(qry)
            d = mycur.fetchall()
            lis = []
            for i in d:
                lis.append(i[0])
            if ask not in lis:
                print('Enter the correct id')
            else:
                while True:
                    self.space()
                    ccc = input(
                        "1. Update delivered records\n2. Add a New Product \n3. Delete a product \nEnter  'Back' to logout:  ")

                    if ccc == '1':
                        cust_id = input('Enter customer id : ')
                        bkd_pro = self.get_bkd_pro(cust_id)
                        if bkd_pro is None or bkd_pro == '':
                            print('This customer has no bookings ')
                        else:
                            print('All booking(s):  ', bkd_pro)
                            pro_id = input(
                                'Enter product code to remove the delivered product   ')
                            if pro_id in bkd_pro:
                                x = (bkd_pro[0:-1]).split('_')
                                x.remove(pro_id)
                                updt_pro = ''
                                for i in x:
                                    updt_pro = updt_pro+i+'_'
                                qry = 'update customer set bkd_pro=%s where cust_id=%s;'
                                val = (updt_pro, cust_id)
                                mycur.execute(qry, val)
                                sqldb.commit()
                                print(
                                    'Delivered product is removed from the database. ')
                            else:
                                print('enter the correct code')

                    elif ccc == '2':
                        self.addpro()
                    elif ccc == '3':
                        self.delpro()
                    elif ccc.lower() == 'back':
                        print("Successfully logged out ")
                        break
        except Exception:
            print('Give the correct input')


# Adding an Employee

    def addemp(self):
        qry = "select * from employee;"
        mycur.execute(qry)
        emp_list = mycur.fetchall()
        print("List of Employees ")
        for emp in emp_list:
            print("Emp Id : ", emp[0], "  Name :   ", emp[1],
                  "  Last Name : ", emp[2], "  Phone No :  ", emp[3])
        ne = []
        n = int(input('enter the no. of employees to add  '))
        for i in range(1, n+1):
            t = ()
            # print()
            idd = int(input('enter employee id :'))
            # print()
            nam = input('Enter the EMP Name: ')
            # print('Last name  ')
            lnam = input('Enter the EMP Last Name: ')
            # print('Contact no.  ')
            conno = int(input('Enter the EMP Contact number: '))

            adrs = input('Enter the EMP Address:')

            t = (idd, nam, lnam, conno, adrs)
        
        ne = ne+[t, ]
        print(ne)
        qry = 'insert into employee values(%s,%s,%s,%s,%s);'

        for i in range(len(ne)):
            val = ne[i]
            mycur.execute(qry, val)
            sqldb.commit()
        print('All Employee details added. ')
        self.space()

# Employee Login

    def employer(self):
        while True:
            print()
            print('''Enter Your Choice:                                                    
                    1)View Product Details
                    2)Add  a New Employee
                      enter back to exit''')
            ccc = input('Enter _____  ')
            if ccc == '1':
                self.view_pro()
            if ccc == '2':
                self.addemp()
            if ccc.lower() == "back":
                break
