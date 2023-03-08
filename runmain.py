from main import Boutique

print('WELCOME !')

obj = Boutique()


while True:
    print('''Are you a :                                                  
   (A). Customer
   (B). Employee
   (C). Employer
   enter e to exit ''')
    ch = input('Enter -  ')
    try:
        if ch in 'aA':
            print(" 1. Create Account\n 2.Sign In into existing account")
            choice = input('enter-   ')
            if choice == '1':
                 obj.customer_acoount()
            elif choice == '2':
                 obj.sign_in()     
            else:
                print('Enter correct choice')

        elif ch in 'bB':
              obj.emp_sign_in()  
        elif ch in 'cC':
              obj.employer()
        elif ch.lower() == "e":
            print("Thankyou for visiting !")    
            break
    except Exception:
         print('Give the right input')
    obj.space()



