# import socket
# import struct
# import time

# HOST = "192.168.0.2" # The remote host
# PORT = 30002 # The same port as used by the server

# print("Starting Program")

# # Modify this value to control how many times the loop will execute
# loop_count = 1

# for count in range(loop_count):
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect((HOST, PORT))
#     time.sleep(0.5)
#     print("Getting encoder data...")
#     cmd = "encoder_get_tick_count()\n"
#     cmd = "movel([-0.7, -0.7, 0.6, 0.3, 0.1, 0], a=1.0, v=0.1)" + "\n"
#     cmd = ()
#     s.send(cmd)
#     #s.send("powerdown()\n".encode())
#     time.sleep(0.1)
#     data = s.recv(4)  # Expecting 4 bytes for an integer
#     encoder_data = struct.unpack("!i", data)[0]  # Unpack as a signed integer
#     print("Encoder data:", encoder_data)
#     s.close()

# print("Program finish")

# # Connect to the robot
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((HOST, PORT))

# # Send a URScript command to shut down the robot
# cmd = "shutdown()\n"
# #s.send(cmd.encode())

# # Close the connection
# s.close()

# Echo client program
# import socket


# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((HOST, PORT))

# s.send ("set_digital_out(2,True)" + "\n")

# data = s.recv(1024)

# s.close()

# print ("Received", repr(data))




# # Echo client program
# import socket

# HOST = "192.168.0.2" # The remote host
# PORT = 50000 # The same port as used by the server

# while True:

#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect((HOST, PORT))



#     s.send("True".encode())

#     data = s.recv(1024).decode('ascii')

#     message_recieved = data

#     print("Received", repr(message_recieved))


# s.close()




# # Echo client program
# import socket
# HOST = "192.168.0.2" # The remote host
# PORT = 30002 # The same port as used by the server

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((HOST, PORT))

# s.send(("set_digital_out(3,True)" + "\n").encode())





    # import time
    # from urx import Robot

    # # UR robot's IP address
    # ROBOT_IP = '192.168.0.2'  # Replace with the actual IP address of your UR10 robot

    # # Connect to the UR robot
    # robot = Robot(ROBOT_IP)

    # # Send the 'set_digital_out' command
    # digital_output_pin = 3
    # output_value = True
    # robot.set_digital_out(digital_output_pin, output_value)

    # # Sleep for a while to make sure the command is sent
    # time.sleep(1)





# import socket

# # establish a TCP/IP connection to the robot controller
# robot_ip = '192.168.0.2'  # replace with the IP address of your robot
# robot_port = 30002
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect((robot_ip, robot_port))

# # send the secondary program to the robot controller
# secondary_program = 'sec secondaryProgram():\n  set_digital_out(3, True)\nend\n'
# sock.send(secondary_program.encode())

# # close the TCP/IP connection
# sock.close()





# def send_variable_to_pc(variable_name):
#     # Open a socket to your PC
#     import socket
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.connect(("YOUR_PC_IP_ADDRESS", YOUR_TCP_PORT))

#     # Send the variable value to your PC
#     var_value = eval(variable_name)  # Get the value of the variable by its name
#     s.send(str(var_value).encode())

#     # Close the socket
#     s.close()

# # Example usage: send the value of a variable named "my_var" to your PC
# send_variable_to_pc("my_var")







import socket

# Set the IP address to listen on to all available interfaces
robot_ip = ''
robot_port = 50002

# Create a TCP socket and bind it to the IP address and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((robot_ip, robot_port))

# Listen for incoming connections
server_socket.listen()

print(f"Server socket listening on port {robot_port}...")

while True:
    # Wait for a client to connect
    client_socket, client_address = server_socket.accept()
    print(f"Received connection from {client_address}")
    
    while True:
        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            # No more data, so break out of the loop
            break
    
        print(f"Received data: {data.decode()}")  # assuming data is a string
        
    

    







# import socket

# # create a socket object
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # bind the socket to a specific IP address and port
# # host = "192.168.0.2"  # listen on all available interfaces
# # port = 50000  # choose a port number
# # server_socket.bind((host, port))
# server_socket.bind(("0.0.0.0", 50000)) 

# # listen for incoming connections
# server_socket.listen(1)  # allow up to 1 connection

# while True:
#     # accept incoming connections
#     client_socket, client_address = server_socket.accept()

#     # receive data from the client
#     data = client_socket.recv(1024)  # receive up to 1024 bytes of data

#     # process the data
#     if data:
#         # send a response back to the client
#         response = 'Thank you for connecting'
#         client_socket.send(response.encode())

#     # close the client socket
#     client_socket.close()

# # close the server socket
# siserver_socket.close()


# import socket

# def server_program():
#     # get the hostname
#     host = ""
#     port = 50000  # initiate port no above 1024

#     server_socket = socket.socket()  # get instance
#     # look closely. The bind() function takes tuple as argument
#     server_socket.bind((host, port))  # bind host address and port together

#     # configure how many client the server can listen simultaneously
#     server_socket.listen(1)
#     conn, address = server_socket.accept()  # accept new connection
#     #print("Connection from: " + str(address))

#     while True:
#         # receive data stream. it won't accept data packet greater than 1024 bytes
#         data = conn.recv(1024).decode()
#         if not data:
#             # if data is not received break
#             break
#         print(str(data))
#         # data = input(' -> ')
#         # conn.send(data.encode())  # send data to the client

#     conn.close()  # close the connection


# if __name__ == '__main__':
#     server_program()


# import socket

# def server_program():
#     # get the hostname
#     host = "192.168.0.2"
#     port = 50000  # initiate port no above 1024

#     server_socket = socket.socket()  # get instance
#     # look closely. The bind() function takes tuple as argument
#     server_socket.bind((host, port))  # bind host address and port together

#     # configure how many client the server can listen simultaneously
#     server_socket.listen(1)
#     conn, address = server_socket.accept()  # accept new connection
#     #print("Connection from: " + str(address))

#     conn.send("movel([-0.7, -0.7, 0.6, 0.3, 0.1, 0], a=1.0, v=0.1)" + "\n")
#     # while True:
#     #     # receive data stream. it won't accept data packet greater than 1024 bytes
#     #     data = conn.recv(1024).decode()
#     #     print(str(data))
#     #     conn.send("movel([-0.7, -0.7, 0.6, 0.3, 0.1, 0], a=1.0, v=0.1)" + "\n")

# # # Python code
# import socket

# # Set the IP address and port of the robot
# HOST = '192.168.0.2'  # Replace with the IP address of your robot
# PORT = 30002  # Default port for UR robots

# # Create the socket object
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Connect to the robot
# s.connect((HOST, PORT))

# # set 'ready' to True
# ready = True
# # send command to client to update 'ready' variable
# s.send(("ready " + str(ready == True).lower() + "\n").encode())


# Python code
# Send the command to set the boolean variable to True
# command = "ready = True\n"
# s.send(command.encode())
# # Python code
# Close the socket connection



# # Python code

# import socket

# # set up socket connection
# HOST = "192.168.0.134"  # IP address of UR10 robot
# PORT = 3020  # port number for socket communication
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect((HOST, PORT))


# message = "backward".encode()
# sock.send(message)
# sock.close()

# host = ""
# port = 30002  # initiate port no above 1024

# UR10_Target_Location_socket = socket.socket()  # get instance
# # look closely. The bind() function takes tuple as argument
# UR10_Target_Location_socket.bind((host, port))  # bind host address and port together

# # configure how many client the server can listen simultaneously
# UR10_Target_Location_socket.listen(1)
# UR10_Target_Location, address = UR10_Target_Location_socket.accept()  # accept new connection




    


# UR10_Target_Location.send("set_digital_out(2,True)" + "\n").encode()



# /////