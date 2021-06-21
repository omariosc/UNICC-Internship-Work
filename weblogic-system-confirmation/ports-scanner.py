#############################################################
#                                                           #               
#   PURPOSE OF PROGRAM:                                     #
#                                                           #
#   --> verify listening ports                              #
#   --> verify established ports                            #
#                                                           #
#############################################################

# importing required modules
import socket, threading, csv, os, time, platform, subprocess

# sets OS
OS = platform.system()

# main class
class ports_scanner():

    # constructor
    def __init__(self):

        if OS != 'Linux': # only compatible with Linux OS
            print("OS does not meet requirements")
            quit()

        # declaring variables and lists
        self.state = {}
        self.port_number = {}
        self.threads = []
        self.host = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host)
        self.port_count = 28002
        self.current_count = 1
        self.position = 0

    # creates csv file to store all port information
    def create_csv(self):

        # csv file path
        csvpath = str(self.host) + ".csv"
        
        # headings for csv file
        headings = [['hostname', 'port'],
                    [self.host, 'number', 'ip', 'program']]

        infoarray = ['']

        ports = self.port_number.values()

        # writes values retreive by other functions and stored in lists in csv file
        with open(csvpath, 'wb+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(headings)
            rcount = 0
            for row in range(0,self.position):
                writer.writerow((infoarray[rcount], ports[rcount]))
                infoarray.append('')
                rcount += 1

        csvFile.close()

    # function to try and connect to port and output listening, established or null
    def TCP_connect(self):
        TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        TCPsock.settimeout(10)
        try:
            TCPsock.connect((self.host_ip, self.current_count))
            self.state[self.current_count] = 'Active'
            self.port_number[self.position] = self.current_count
            self.position += 1
        except:
            self.state[self.current_count] = 'Inactive'

    # function which iterates through a range of ports and runs TCP_connect function on them
    def scan_ports(self):

        # spawning threads to scan ports
        for self.current_count in range(self.port_count):
            t = threading.Thread(target=app.TCP_connect())
            self.threads.append(t)
        self.current_count = 1

        # starting threads
        for self.current_count in range(self.port_count):
            self.threads[self.current_count].start()
        self.current_count = 1
    
        # locking the main thread until all threads complete
        for self.current_count in range(self.port_count):
            self.threads[self.current_count].join()
        self.current_count = 1

# runs program
if __name__ == "__main__":
    app = ports_scanner()
    app.scan_ports()
    app.create_csv()
