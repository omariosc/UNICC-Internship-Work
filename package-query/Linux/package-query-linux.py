#############################################################
#                                                           #
#   PURPOSE OF PROGRAM:                                     #
#                                                           #
#   --> verify package installations                        #
#   --> confirm which package versions are installed        #
#   --> checks limits (nofile & nproc)                      #
#   --> checks system requirements                          #
#   --> creates sysreadiness csv files                      #
#   --> confirms readiness for system for installation      #
#   --> to set up basis for a fusion middleware             #
#       environment                                         #
#                                                           #
#############################################################

# import required modules
import os, subprocess, time, platform, csv, socket

# sets OS
OS = platform.system()

# main class
class package_query():

    # constructor
    def __init__(self):

        if OS == 'Linux': # only compatible with Linux OS
            #os.system("cd package-query")
            self.filebase = "Linux"

        # closes program if OS does not meet requirements
        else:
            print("OS does not meet requirements")
            quit()

        # creates file paths for log directory, system readiness log and err files
        self.logdir = self.filebase+"/log"
        self.packagefile = self.filebase+"/os-linux-requiredpackages.text"
        self.confcsv = self.filebase+"/"+socket.gethostname()+".csv"

        # declaring variables
        self.NewPackageName = ''
        self.NewComponentName=''
        self.message=''
        self.package_name = []
        self.package_versions = []
        self.package_architecture = []
        self.package_comment = []
        self.limit_name = []
        self.limit_value = []
        self.limit_comment = []
        self.comp_name = []
        self.comp_value = []
        self.comp_comment = []
        self.position = 0

    # function to verify package if OS is Linux
    def verify_package(self):

        # opens file which contains package and writes header message
        with open(self.packagefile) as packages:
            package = packages.readline()
            position = 0

            # truncates package name to just the package name minus version and other details      
            while package:
                packagename = package.strip()
                for x in range(len(packagename)):
                    if ((packagename[x] == '-' and packagename[x+1].isdigit())
                         or packagename[x] == ' '):
                            break
                    else:
                            self.NewPackageName += str(packagename[x])
                package = packages.readline()

                # rpm command to call package name(s), version(s) and architecure(s) and store in the appropriate lists
                os.system('''rpm -q --qf "_%{n}_\n" '''+self.NewPackageName+
                          ''' | grep '_'''+self.NewPackageName+"_' | wc -l > "+
                          self.logdir+'/'+self.NewPackageName+'-nametmp.log')
                os.system('cat '+self.logdir+'/'+self.NewPackageName+'-nametmp.log > '+
                          self.logdir+'/'+self.NewPackageName+'-countercheck.log')
                countertext = open(self.logdir+'/'+self.NewPackageName+'-countercheck.log')
                checkcount = int(countertext.read())
                
                if checkcount >= 1:
                    os.system('''rpm -qa --qf "%{n}_%{v}\n" '''+self.NewPackageName+' > '+
                              self.logdir+'/'+self.NewPackageName+'-verstmp.log')
                    os.system("awk -F '_' '{print$2}' < "+
                              self.logdir+'/'+self.NewPackageName+'-verstmp.log > '+
                              self.logdir+'/'+self.NewPackageName+'-vers.log')    
                    versionnumber = open(self.logdir+'/'+self.NewPackageName+'-vers.log')
                    version = str(versionnumber.read())  
                    if version == '': # if there is no version recorded on system
                        version = 'N/A'              
                    os.system('''rpm -qa --qf "%{n}_%{arch}\n" '''+self.NewPackageName+' > '+
                              self.logdir+'/'+self.NewPackageName+'-archtmp.log')
                    os.system("awk -F '_' '{print$2}' < "+
                              self.logdir+'/'+self.NewPackageName+'-archtmp.log > '+
                              self.logdir+'/'+self.NewPackageName+'-arch.log') 
                    arch = open(self.logdir+'/'+self.NewPackageName+'-arch.log')
                    architecture = str(arch.read())
                    if architecture == '': # if there is no architecture recorded on system
                        architecture = 'N/A'
                    self.package_name.append('')
                    self.package_versions.append('')
                    self.package_architecture.append('')
                    self.package_comment.append('')
                    self.package_name[position] = self.NewPackageName
                    self.package_versions[position] = version
                    self.package_architecture[position] = architecture
                    self.package_comment[position] = 'Y'
                    position += 1
                    
                elif checkcount == 0: 
                    self.package_name.append('')
                    self.package_versions.append('')
                    self.package_architecture.append('')
                    self.package_comment.append('')
                    self.package_name[position] = self.NewPackageName
                    self.package_versions[position] = 'N/A'
                    self.package_architecture[position] = 'N/A'
                    self.package_comment[position] = 'N'
                    position += 1
                                
                # sets the truncated package name back to empty string for iteration
                self.NewPackageName=''

        # removes temporary text files
        os.system('rm '+self.logdir+'/*.log')

    # OS dependent limit checks
    def limits_check(self):
        
        # Linux commands to store limits in temporary files
        os.system('ulimit -n -H > '+self.logdir+'/openfiles.txt')
        os.system('ulimit -u -H > '+self.logdir+'/maxuserprocesses.txt')

        position = 0

        # if any limits are not met it writes correct text into csv file
        openfiles = open(str(self.logdir)+"/openfiles.txt")
        nofile = int(openfiles.read())
        maxuserprocesses = open(str(self.logdir)+"/maxuserprocesses.txt")
        nproc = int(maxuserprocesses.read())   
        self.limit_name.append('')
        self.limit_value.append('')
        self.limit_name[position] = 'nofile'
        self.limit_value[position] = nofile
        self.limit_name.append('')
        self.limit_value.append('')
        self.limit_name[position+1] = 'nproc'
        self.limit_value[position+1] = nproc
        if nofile < 65536:
            self.limit_comment.append('') 
            self.limit_comment[position] = 'FAIL'
        else:
            self.limit_comment.append('') 
            self.limit_comment[position] = 'PASS'
        if nproc < 32768:
            self.limit_comment.append('') 
            self.limit_comment[position+1] = 'FAIL'
        else:
            self.limit_comment.append('') 
            self.limit_comment[position+1] = 'PASS'

        # removes temporary text files
        os.system('rm '+self.logdir+'/*.txt')
       
    # OS dependent system requirements checks
    def sys_check(self):

        # sets up values for iteration loop
        systemchecks = ['net.core.rmem_max','net.core.wmem_max','kernel.shmall',
                        'kernel.shmmax','kernel.msgmax','kernel.msgmnb','vm.swappiness']
        systemrequirementvalues = []
        minvalues = ['4192608', '4192608', '4294967295', '68719476736', '65536', '65536', '10']
        temparray = []
        x = 0

        # creates values for systemrequirementvalues array
        for i in range(7):
            systemrequirement = systemchecks[x].replace(".","")
            systemrequirement = systemrequirement.replace("_","")
            os.system("sysctl "+systemchecks[x]+" | awk -F '=' '{print$2}' > "+self.logdir+'/'+systemrequirement+'.txt')
            systemrequirementfile = open(str(self.logdir)+"/"+systemrequirement+".txt")
            systemrequirementvalues.append((int(systemrequirementfile.read())))
            temparray.append(systemrequirementvalues[x]-int(minvalues[x]))
            x += 1
            
        # writes error message for any failed system requirements checks
        # loops through each item in the list conifrming if any values are false
        x = 0
        for i in range(7):
            if temparray[x]<0:
                self.comp_comment.append('')
                self.comp_comment[x] = 'FAIL'
            else:
                self.comp_comment.append('')
                self.comp_comment[x] = 'PASS'
            self.comp_value.append('')
            self.comp_name.append('')
            self.comp_value[x] = systemrequirementvalues[x]
            self.comp_name[x] = systemchecks[x]
            x += 1

        # removes temporary text files
        os.system("rm "+self.logdir+'/*.txt')

    # checks if files/directories/file systems exists, OS indepdendent
    def check_file(self):

        # checks if log directory exists
        if os.path.exists(self.logdir) == 0:
            os.mkdir(self.logdir)

        # removes contents of sysreadiness csv file if exists
        if os.path.exists(self.confcsv) == 1:
            os.remove(self.confcsv)
            
    # creates a system readiness csv file and inital headings
    def create_csv(self):
        
        # headings for csv file
        headings = [['hostname','packagechecks','','','','limitchecks','','','systemchecks'],
                   [socket.gethostname(),'name','version','architecture','comment','name',
                    'value','comment','name','value','comment']]

        infoarray = ['***','***','***',
                     'IF THERE ARE BLANK',
                     'SPACES BUT THE',
                     'COMMENT IS Y OR',
                     'PASS THEN PRESS',
                     '<CTRL> <A> &',
                     'DOUBLE CLICK ON',
                     'THE EDGE OF FIRST ROW',
                     'AND COLUMN TO VIEW',
                     'DETAILS',
                     '***','***','***']

        # writes values retreived by other functions and stored in lists in csv file
        with open(self.confcsv,'wb+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(headings)
            rcount = 0
            for row in self.package_name:
                writer.writerow((infoarray[rcount],self.package_name[rcount],self.package_versions[rcount],
                                 self.package_architecture[rcount],self.package_comment[rcount],
                                 self.limit_name[rcount],self.limit_value[rcount],
                                 self.limit_comment[rcount],self.comp_name[rcount],
                                 self.comp_value[rcount],self.comp_comment[rcount]))
                infoarray.append('')
                self.limit_name.append('')
                self.limit_value.append('')
                self.limit_comment.append('')
                self.comp_name.append('')
                self.comp_value.append('')
                self.comp_comment.append('')
                rcount += 1
                
        csvFile.close()
            
    # program to delete log directory
    def del_logdir(self):
        os.system('rm -r '+self.logdir)
            
# runs program    
if __name__ == "__main__":
    app = package_query()
    app.check_file()
    app.verify_package()
    app.limits_check()
    app.sys_check()
    app.del_logdir()
    app.create_csv()
