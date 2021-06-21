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

        if OS == 'Linux': # only compatible with Linux OS
            os.system("cd Omar")
            self.filebase = "Omar"
            
            # changes package requirements depending on Linux OS version
            version = float((platform.linux_distribution()[1]))
            if version >= 7:
                self.packagefile = self.filebase+"/os-linux7-packages.txt"
                self.confcsv = self.filebase+"/sysreadiness-linux7.csv"
            elif version < 7 and version >= 6:
                self.packagefile = self.filebase+"/os-linux6-packages.txt"
                self.confcsv = self.filebase+"/sysreadiness-linux6.csv"

        # closes program if OS does not meet requirements
        else:
            print("OS does not meet requirements")
            quit()

        # creates file paths for log directory, system readiness log and err files
        self.logdir = self.filebase+"/log"
        self.sysconfirmlog = self.filebase+"/sysreadiness.log"
        self.sysconferr = self.filebase+"/sysreadiness.err"
        self.packagefile = self.filebase+"/os-linux-requiredpackages.txt"

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

                os.system('''rpm -qa --qf "%{n}-%{v}-%{arch}\n" '''+str(self.NewPackageName)+'''> "'''+self.logdir+"/"+str(self.NewPackageName)+'''-tmp.log"''')
                os.system('''cat "'''+self.logdir+"/"+str(self.NewPackageName)+'''-tmp.log"|grep '''+str(self.NewPackageName)+'''|wc -l > "'''+
                          self.logdir+"/"+str(self.NewPackageName)+'''-countercheck.txt"''')

                # gets version and architecture
                #os.system('''cat "'''+self.logdir+"/"+str(self.NewPackageName)+"""-tmp.log"|awk -F '"""+str(self.NewPackageName)+"""'{print$2}'""")    

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

                os.system('rm '+self.logdir+"/"+str(self.NewPackageName)+'-tmp.log')
                os.system('rm '+self.logdir+"/"+str(self.NewPackageName)+'-countercheck.txt')
            
                # sets the truncated package name back to empty string for iteration
                self.NewPackageName=''

    # OS dependent limit checks
    def limits_check(self):
        
        # prepares confirmation file    
        confirmationfile = open(self.sysconfirmlog,"a")
        hdrmessage = str("\nLimit Checks:\n")
        confirmationfile.write(hdrmessage)
        position = 0
        
        # Linux commands to store limits in temporary files
        os.system('ulimit -n -H > '+self.logdir+'/openfiles.txt')
        os.system('ulimit -u -H > '+self.logdir+'/maxuserprocesses.txt')

        # if any limits are not met it writes correct text into confirmation log file
        openfiles = open(str(self.logdir)+"/openfiles.txt")
        nofile = int(openfiles.read())
        maxuserprocesses = open(str(self.logdir)+"/maxuserprocesses.txt")
        nproc = int(maxuserprocesses.read())
        if nofile < 65536:
            self.message = 'nofile limit not met\n'
            package_query.error_message(self)
            self.limit_name[position] = 'nofile'
            self.limit_value[position] = nofile
            position += 1
        if nproc < 32768:
            self.message = 'nproc limit not met\n'
            package_query.error_message(self)
            self.limit_name[position] = 'nofile'
            self.limit_value[position] = nofile
            position += 1
        if nofile >= 65536 and nproc >= 32768:
            confirmationfile.write('all limits met\n')
            self.limit_name[position] = 'nofile'
            self.limit_value[position] = nofile
            self.limit_name[position+1] = 'nproc'
            self.limit_value[position+1] = nproc              
        else:
            confirmationfile.write('review system readiness error file '+self.sysconferr+'\n')

        # removes temporary text files
        os.system('rm '+self.logdir+'/*.txt')

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

        # sets up values for iteration loop
        systemchecks = ['net.core.rmem_max','net.core.wmem_max','kernel.shmall',
                        'kernel.shmmax','kernel.msgmax','kernel.msgmnb','vm.swappiness']
        systemrequirementvalues = []
        minvalues = ['4192608', '4192608', '4294967295', '68719476736', '65536', '65536', '10']
        temparray = []
        x = 0
        confirmvalue = 0

        # creates values for systemrequirementvalues array
        for i in range(7):
            systemrequirement = systemchecks[x].replace(".","")
            systemrequirement = systemrequirement.replace("_","")
            os.system("sysctl "+systemchecks[x]+" | awk -F '=' '{print$2}' > "+self.logdir+'/'+systemrequirement+'.txt')
            systemrequirementfile = open(str(self.logdir)+"/"+systemrequirement+".txt")
            systemrequirementvalues.append((int(systemrequirementfile.read())))
            temparray.append(systemrequirementvalues[x]-int(minvalues[x]))
            x+=1
            
        # writes error message for any failed system requirements checks
        # loops through each item in the list conifrming if any values are false
        x = 0
        for i in range(7):
            if temparray[x]<0:
                self.message = str(systemchecks[x])+'value is too low\n'
                package_query.error_message(self)
                self.comp_value[x] = systemrequirementvalues[x]
                self.comp_name[x] = systemchecks[x]
            else:
                confirmvalue += 1
                self.comp_value[x] = systemrequirementvalues[x]
                self.comp_name[x] = systemchecks[x]
            x += 1
        
        # if all system requirements are met
        if confirmvalue == 7:
            confirmationfile.write('all limits met\n')
        else:
            confirmationfile.write('review system readiness error file: '+self.sysconferr+'\n')

        # removes temporary text files
        os.system("rm "+self.logdir+'/*.txt')

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

        # deletes sysreadiness.err file and removes contents of sysreadiness csv file if exists
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
        os.system('rm -r '+self.logdir)

    # function that tries to reach the sysreadiness.err file
    def confirmreadiness(self):
        
        try: # error handling to output appropriate message
            
            open(self.sysconferr) # attempts to open system readiness error file

            print("Error! One or more system readiness check failed\n"+
                  "Review system readiness error file : "+self.sysconferr)
            
        except FileNotFoundError: # no error file
            
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
    app.create_csv()
    app.confirmreadiness()
