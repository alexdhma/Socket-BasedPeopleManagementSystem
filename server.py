
# import socket
import socket

# read data.txt
print("\nLoading database...\n")
database = {}

with open("data.txt", "r") as file:
    for line in file:
        parts = line.strip().split("|")
        

        reason = ""

        # if missing fields
        if len(parts) != 4:
            reason = "[missing field(s)]"
        else:
            name, age_str, address, phone = [p.strip() for p in parts]

            # if there's no name
            if not name:
                reason = "[missing name field]"


            # if age is invalid
            elif not age_str.isdigit():
                reason = "[invalid age field]"
            else:
                age = int(age_str)
                if age < 0 or age > 120:
                    reason = "[invalid age field]"
        

            # if phone is invalid
            if reason == "" and phone != "":
                index = phone[:3]
                
                validIndex = False
                if index == "394" or index=="426" or index=="901" or index=="514":
                    validIndex = True

                if len(phone) != 8 or phone[3] != "-" or not validIndex:
                    reason = "[invalid phone field]"


            # if person already exist
            if reason=="" and name.capitalize() in database:
                reason = "[key/record already exists]"


        if reason != "":
            print("DB read error: Record skipped " + reason +  ": " + line)

        else:
            database[name.capitalize()] = (name, age, address, phone)

  


# create socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind socket to a host and port
host = socket.gethostname()
port = 1234
server_socket.bind((host, port))

# listen to client
server_socket.listen(1)
print("\nPython DB server is now running...\n")

# accept client connection
client_socket, addr = server_socket.accept()


# handle client commands
while True:
    # client's command
    data = client_socket.recv(1024).decode()
    print("Received command: " + data)

    # 1. find customer command
    if data.startswith("FIND "):
        name = data[5:].strip()
        if name in database:
            record = database[name.capitalize()]
            response = record[0] + "|" + str(record[1]) + "|" + record[2] + "|" + record[3]
        else:
            response = name + " not found in database"

        # send response to client
        client_socket.sendall(response.encode())


    # 2. add customer
    if data.startswith("ADD "):
        parts = data[4:].strip().split("|")
        reason = ""

        # if missing fields
        if len(parts) != 4:
            reason = "[missing field(s)]"
        else:
            name, age_str, address, phone = [p.strip() for p in parts]

            # if there's no name
            if not name:
                reason = "record contains invalid name [" + name + "]"

            # if age is invalid
            elif not age_str.isdigit():
                reason = "record contains invalid age [" + age_str + "]"
            else:
                age = int(age_str)
                if age < 0 or age > 120:
                    reason = "record contains invalid age [" + str(age) + "]"
        
            # if phone is invalid
            if reason == "" and phone != "":
                index = phone[:3]
                
                validIndex = False
                if index == "394" or index=="426" or index=="901" or index=="514":
                    validIndex = True

                if len(phone) != 8 or phone[3] != "-" or not validIndex:
                    reason = "record contains invalid phone [" + phone + "]"

            # if person already exist
            if reason=="" and name.capitalize() in database:
                reason = name.capitalize() + " already stored in database"

        if reason != "":
            response = "DB add error: " + reason

        else:
            database[name.capitalize()] = (name, age, address, phone)
            response = data[4:] + " added to database"

        # send response to client
        client_socket.sendall(response.encode())  

    # 3. delete customer
    if data.startswith("DELETE "):
        name = data[7:].strip()
        if name in database:
            del database[name]
            response = name + " deleted from database"
        else:
            response = name + " not found in database"

        # send response to client
        client_socket.sendall(response.encode())  

    # 4. update customer age
    if data.startswith("UPDATE AGE "):
        parts = data[11:].strip().split("|")

        name, newAge_str = [p.strip() for p in parts]

        # if person not in database
        if name not in database:
            response = name + " not found in database"

        # if age is invalid
        if not newAge_str.isdigit() or int(newAge_str) < 0 or int(newAge_str) > 120:
            response = "DB update error: attempt to update using invalid age [" + newAge_str + "]"
        else:
            old = database[name.capitalize()]
            database[name.capitalize()] = (old[0], newAge_str, old[2], old[3])
            response = "DB update sucessful: updated customer's age to [" + newAge_str + "]"

        # send response to client
        client_socket.sendall(response.encode())  

    # 5. update customer address
    if data.startswith("UPDATE ADDRESS "):
        parts = data[15:].strip().split("|")

        name, newAddress = [p.strip() for p in parts]

        # if person not in database
        if name not in database:
            response = name + " not found in database"

        # if address is empty
        if not newAddress:
            response = "DB update error: attempt to update using invalid address [" + newAddress + "]"
        else:
            old = database[name.capitalize()]
            database[name.capitalize()] = (old[0], old[1], newAddress, old[3])
            response = "DB update sucessful: updated customer's address to [" + newAddress + "]"

        # send response to client
        client_socket.sendall(response.encode()) 

    # 6. update customer phone
    if data.startswith("UPDATE PHONE "):
        parts = data[13:].strip().split("|")

        name, newPhone = [p.strip() for p in parts]

        # if person not in database
        if name not in database:
            response = name + " not found in database"

        # if phone is invalid
        if newPhone != "":
            index = newPhone[:3]
            validIndex = False
            if index == "394" or index=="426" or index=="901" or index=="514":
                validIndex = True

            if len(newPhone) != 8 or newPhone[3] != "-" or not validIndex:
                response = "DB update error: attempt to update using invalid phone number [" + newPhone + "]"
            
            else:
                old = database[name.capitalize()]
                database[name.capitalize()] = (old[0], old[1], old[2], newPhone)
                response = "DB update sucessful: updated customer's phone to [" + newPhone + "]"

        # send response to client
        client_socket.sendall(response.encode()) 


    # 7. print report
    if data.startswith("PRINT REPORT"):
        response = "\n\n++\n++ DB Report\n++\n\n"
        response += f"{'Name':<10} {'Age':<5} {'Address':<20} {'Phone':<12}\n"
        response += f"{'-'*10} {'-'*5} {'-'*20} {'-'*12}\n" 
        
        # sort alphabetically
        sorted_database = sorted(database.items())
        
        # print each entry
        for key, entry in sorted_database:
            name, age, address, phone = entry
            age_str = str(age)
            if not age_str:
                age_str = ""
            if not address:
                address = ""
            if not phone:
                phone = ""

            response += f"{name:<10} {age_str:<5} {address:<20} {phone:<12}\n"

        # send response to client
        client_socket.sendall(response.encode()) 


    # 8. exit command
    if data == "EXIT":
        response = "Goodbye!\n"
        client_socket.sendall(response.encode())
        break


# close sockets
client_socket.close()
server_socket.close()
      




