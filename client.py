
import socket

host = socket.gethostname()
port = 1234

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))

    print("""
        Python DB Menu
            
        1. Find customer
        2. Add customer
        3. Delete customer
        4. Update customer age
        5. Update customer address
        6. Update customer phone
        7. Print report
        8. Exit 
        """)
    
    while True: 
        try:
            user_input = input("\nSelect: ").strip()
        except ValueError:
            print("Invalid input. Enter number from 1 to 8.")
            continue


        # 1. find customer 
        if user_input == "1":
            name = input("Customer Name: ").strip().capitalize()
            command = "FIND " + name

        # 2. add customer
        if user_input == "2":
            name = input("Customer Name: ").strip().capitalize()
            age = input("Customer age: ").strip()
            address = input("Customer address: ").strip()
            phone = input("Customer phone: ").strip()
            command = "ADD " + name + "|" + age + "|" + address + "|" + phone

        # 3. delete customer
        if user_input == "3":
            name = input("Customer Name: ").strip().capitalize()
            command = "DELETE " + name

        # 4. update customer age
        if user_input == "4":
            name = input("Customer Name: ").strip().capitalize()
            age = input("Customer age: ").strip()
            command = "UPDATE AGE " + name + "|" + age

        # 5. update customer address
        if user_input == "5":
            name = input("Customer Name: ").strip().capitalize()
            address = input("Customer address: ").strip()
            command = "UPDATE ADDRESS " + name + "|" + address

        # 6. update customer phone
        if user_input == "6":
            name = input("Customer Name: ").strip().capitalize()
            phone = input("Customer phone: ").strip()
            command = "UPDATE PHONE " + name + "|" + phone

        # 7. print report
        if user_input == "7":
            command = "PRINT REPORT"

        # 8. exit
        elif user_input == "8":
            command = "EXIT"
            

        # send command to server
        s.sendall(command.encode())
        data = s.recv(1024).decode()
        print("Server response: " + data)

