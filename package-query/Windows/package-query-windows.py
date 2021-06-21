#############################################################
#                                                           #
#   PURPOSE OF PROGRAM:                                     #
#                                                           #
#   --> verify package installations                        #
#   --> confirm which package versions are installed        #
#   --> checks limits (nofile & nproc)                      #
#   --> checks system requirements                          #
#   --> creates sysreadiness log files                      #
#   --> creates sysreadiness err file if error(s)           #
#       are encountered                                     #
#   --> confirms readiness for system for installation      #
#   --> to set up basis for a fusion middleware             #
#       environment                                         #
#                                                           #
#############################################################

# import required modules
import os, subprocess, time, platform, csv, socket

# sets OS
OS = platform.system()

#main class
class package_query():

    # constructor
    def __init__(self):

        # sets correct file base and file paths, OS dependent
        if OS == 'Windows': # Windows
            self.filebase = "G:/UNICC/Fusion Middleware"
            self.packagefile = self.filebase+"/os-linux-requiredpackages.txt"
            self.limitsfile = self.filebase+"/limits.conf"
            self.sysfile = self.filebase+"/sysctl.conf"
            
            # setting initial system requirements to not ready
            self.netcorermemmax = 0
            self.netcorewmemmax = 0
            self.kernelshmall = 0
            self.kernelshmmax = 0
            self.kernelmsgmax = 0
            self.kernelmsgmnb = 0
            self.vmswappiness = 0
            
        # closes program if OS does not meet requirements
        else:
            print("OS does not meet requirements")
            time.sleep(1)
            quit()

        # creates file paths for log directory, system readiness log and err files
        self.logdir = self.filebase+"/log"
        self.sysconfirmlog = self.filebase+"/sysreadiness.log"
        self.sysconferr = self.filebase+"/sysreadiness.err"
        self.confcsv = self.filebase+"/sysreadiness.csv"

        # declaring variables
        self.NewPackageName = ''
        self.NewComponentName=''
        self.message=''
        self.package_name = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
        self.package_versions = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
        self.package_architecture = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
        self.limit_name = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
        self.limit_value = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
        self.comp_name = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
        self.comp_value = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
        self.position = 0

    # function to output message to error file
    def error_message(self):
        errorfile = open(self.sysconferr,"a")
        errorfile.write(self.message)
        errorfile.close()

    # function to verify package if OS is Linux
    def verify_package(self):

        # opens file which contains package and writes header message
        with open(self.packagefile) as packages:
            package = packages.readline()
            confirmationfile = open(self.sysconfirmlog,"a")
            hdrmessage = str("Package Checks:\n")
            confirmationfile.write(hdrmessage)
            confirmationfile.close()
            position = 0

            # truncates package name to just the package name minus version and other details      
            while package:
                packagename = package.strip()
                for x in range(len(packagename)):
                    if packagename[x] == '-' and packagename[x+1].isdigit():
                            break
                    else:
                            self.NewPackageName += str(packagename[x])
                package = packages.readline()

                if OS == 'Windows': #  Windows OS commands for testing
                    os.system('''dir > "'''+str(self.logdir)+"/"+str(self.NewPackageName)+'''-tmp.log"''')
                    os.system('''find /i /c "UNICC" < "'''+str(self.logdir)+"/"+str(self.NewPackageName)+'''-tmp.log" > "'''+
                              str(self.logdir)+"/"+str(self.NewPackageName)+'''-countercheck.txt"''')                

                # prepares confirmation log
                check_exist = open(str(self.logdir)+"/"+str(self.NewPackageName)+'''-countercheck.txt''')
                checkcount = int(check_exist.read())
                confirmationfile = open(self.sysconfirmlog,"a")
                version = 'X.Y.Z'
                version2 = 'W.X.Y.Z'
                architecture = '64-bit'
                architecture2 = '32-bit'

                # determines which X-bit versions are installed
                if checkcount == 1:
                    message = str(self.NewPackageName)+' 64-bit version installed'+'\n'
                    confirmationfile.write(message)
                    self.package_name[position] = self.NewPackageName
                    self.package_versions[position] = version
                    self.package_architecture[position] = architecture
                    position += 1
                elif checkcount == 2:
                    message = str(self.NewPackageName)+' 64-bit & 32-bit versions installed'+'\n'
                    confirmationfile.write(message)
                    self.package_name[position] = self.NewPackageName
                    self.package_versions[position] = version
                    self.package_architecture[position] = architecture
                    position += 1
                    self.package_name[position] = self.NewPackageName
                    self.package_versions[position] = version2
                    self.package_architecture[position] = architecture2
                    position += 1
                else:
                    self.message = str(self.NewPackageName)+' not installed'+'\n'
                    package_query.error_message(self)
                    confirmationfile.write('review system readiness error file '+self.sysconferr+'\n')
                confirmationfile.close()

                try: # Linux os commands to remove temporary log files
                    os.system('rm '+self.logdir+"/"+str(self.NewPackageName)+'-tmp.log')
                    os.system('rm '+self.logdir+"/"+str(self.NewPackageName)+'-countercheck.txt')
                finally:                
                    # sets the truncated package name back to empty string for iteration
                    self.NewPackageName=''

    # OS dependent limit checks
    def limits_check(self):
        
        # prepares confirmation file    
        confirmationfile = open(self.sysconfirmlog,"a")
        hdrmessage = str("\nLimit Checks:\n")
        confirmationfile.write(hdrmessage)
        position = 0
        limitsfile = open(self.limitsfile,"r")

        # sets initial Windows limits to not ready
        a = b= c = d = 0

        # iterates through each line and confirms values for each individual limit when met
        for line in limitsfile:
            fields = line.split()
            field1 = str(fields[0])
            field2 = str(fields[1])
            field3 = str(fields[2])
            field4 = int(fields[3])
            limits = [field1, field2, field3]

            # minimum requirements for each limit
            if limits == ['*', 'soft', 'nofile'] and field4 >= 65536:
                a=1
                self.limit_name[position] = field2+field3
                self.limit_value[position] = field4
                position += 1
            elif limits == ['*', 'hard', 'nofile'] and field4 >= 65536:
                b=1
                self.limit_name[position] = field2+field3
                self.limit_value[position] = field4
                position += 1
            elif limits == ['*', 'soft', 'nproc'] and field4 >= 32768:
                c=1
                self.limit_name[position] = field2+field3
                self.limit_value[position] = field4
                position += 1
            elif limits == ['*', 'hard', 'nproc'] and field4 >= 32768:
                d=1
                self.limit_name[position] = field2+field3
                self.limit_value[position] = field4
                position += 1

        # if any limits are not met it writes correct text into confirmation log file       
        if a == 0:
            self.message = 'soft nofile limit not met\n'
            package_query.error_message(self)
        if b == 0:
            self.message = 'hard nofile limit not met\n'
            package_query.error_message(self)
        if c == 0:
            self.message = 'soft nproc limit not met\n'
            package_query.error_message(self)
        if d == 0:
            self.message = 'hard nproc limit not met\n'
            package_query.error_message(self)

        # if all limits are met
        if (a and b and c and d) == 1:
            confirmationfile.write('all limits met\n')
        else:
            confirmationfile.write('review system readiness error file '+self.sysconferr+'\n')

        confirmationfile.close()

    # function for checking system component values with required values 
    def comp_check(self, name, value):

        # minimum requirements for each limit
        if name == 'net.core.rmem_max' and value >= '4192608':
            self.netcorermemmax = 1
        elif name == 'net.core.wmem_max' and value >= '4192608':
            self.netcorewmemmax = 1   
        elif name == 'kernel.shmall' and value >= '4294967295':
            self.kernelshmall = 1
        elif name == 'kernel.shmmax' and value >= '68719476736':
            self.kernelshmmax = 1
        elif name == 'kernel.msgmax' and value >= '65536':
            self.kernelmsgmax = 1  
        elif name == 'kernel.msgmnb' and value >= '65536':
            self.kernelmsgmnb = 1
        elif name == 'vm.swappiness' and value >= '10':
            self.vmswappiness = 1
        
    # OS dependent system requirements checks
    def sys_check(self):
        
        # prepares confirmation file
        confirmationfile = open(self.sysconfirmlog,"a")
        hdrmessage = str("\nSystem Checks:\n")
        confirmationfile.write(hdrmessage)
       
        # opens file which contains system component information
        with open(self.sysfile) as components:
            component = components.readline()

            # truncates package name to just the component name minus extra characters and value      
            while component:
                componentname=component.strip()
                for x in range(len(componentname)):
                    if componentname[x] == '=' and componentname[x+1].isdigit():
                        componentvalue = componentname[x+1:]
                        package_query.comp_check(self, self.NewComponentName, componentvalue)
                    elif componentname[x] == ' ' and componentname[x+1] == '=':
                        componentvalue = componentname[x+3:]
                        package_query.comp_check(self, self.NewComponentName, componentvalue)
                    else:
                        self.NewComponentName += str(componentname[x])
                component = components.readline()

                # sets the truncated component name back to empty string for iteration
                self.NewComponentName=''

        # if any system requiremnts are not met it writes correct text into confirmation log file  
        if self.netcorermemmax == 0:
            self.message = 'net.core.rmem_max not met\n'
            package_query.error_message(self)
        if self.netcorewmemmax == 0:
            self.message = 'net.core.wmem_max not met\n'
            package_query.error_message(self)
        if self.kernelshmall == 0:
            self.message = 'kernel.shmall not met\n'
            package_query.error_message(self)
        if self.kernelshmmax == 0:
            self.message = 'kernel.shmmax not met\n'
            package_query.error_message(self)
        if self.kernelmsgmax == 0:
            self.message = 'kernel.msgmax not met\n'
            package_query.error_message(self)
        if self.kernelmsgmnb == 0:
            self.message = 'kernel.msgmnb not met\n'
            package_query.error_message(self)
        if self.vmswappiness == 0:
            self.message = 'vm.swappiness not met\n'
            package_query.error_message(self)
    
        # if all limits are met
        if (self.netcorermemmax and self.netcorewmemmax and self.kernelshmall and self.kernelshmmax and
            self.kernelmsgmax and self.kernelmsgmnb and self.vmswappiness) == 1:
            confirmationfile.write('all system components met\n')
        else:
            confirmationfile.write('review system readiness error file '+self.sysconferr+'\n')

        confirmationfile.close()            

    # checks if files/directories/file systems exists, OS indepdendent
    def check_file(self):

        # checks if log directory exists
        if os.path.exists(self.logdir) == 0:
            try:
                os.mkdir(self.logdir)
            except OSError:
                self.message = "Creation of the directory failed: " + self.logdir,"\n"
                package_query.error_message(self)
                confirmationfile.write('review system readiness error file:\n"'+self.sysconferr+'"\n')

        # deletes and recreates confirmation log file if exists    
        if os.path.isfile(self.sysconfirmlog):
            os.remove(self.sysconfirmlog)
            confirmationfile = open(self.sysconfirmlog,"w")
            confirmationfile.close()
        else:
            confirmationfile = open(self.sysconfirmlog,"w")
            confirmationfile.close()

        # deletes sysreadiness.err file and removes contents of sysreadiness.csv file if exists
        if os.path.exists(self.sysconferr) == 1:
            os.remove(self.sysconferr)
            
    # creates a system readiness csv file and inital headings
    def create_csv(self):
        
        # headings for csv file
        csvData = [['hostname','packagechecks','','','limitchecks','','systemchecks'],
                   [socket.gethostname(),'name','version','architecture','name','value','name','value']]

        emptyarray = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']

        # writes values retreived by other programs and stored in lists in he csv file
        with open(self.confcsv,'wb+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(csvData)
            rcount = 0
            for row in self.package_name:
                writer.writerow((emptyarray[rcount],
                                 self.package_name[rcount],
                                 self.package_versions[rcount],
                                 self.package_architecture[rcount],
                                 self.limit_name[rcount],
                                 self.limit_value[rcount],
                                 self.comp_name[rcount],
                                 self.comp_value[rcount]))
                rcount += 1
                
        csvFile.close()
            
    # program to delete log directory
    def del_logdir(self):
        os.system('RD /S /Q "'+self.logdir+'"')

    # function that tries to reach the sysreadiness.err file
    def confirmreadiness(self):
        
        try: # error handling to output appropriate message
            
            open(self.sysconferr) # attempts to open system readiness error file
            print("Error! One or more system readiness check failed\n" +
                  "Review system readiness error file : "+self.sysconferr)
            
        except: # no error file

            print("All packages installed\n"+
                  "All limits met\n"+
                  "All system requirements met\n"+
                  "System ready for installation")
            
# runs program    
if __name__ == "__main__":
    app = package_query()
    app.check_file()
    app.verify_package()
    app.limits_check()
    app.sys_check()
    app.del_logdir()
    #app.create_csv()
    app.confirmreadiness()
