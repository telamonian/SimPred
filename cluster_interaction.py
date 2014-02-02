
# Modules to import
#   - paramiko is the ssh interface
#   - sendgrid is an email interface
import paramiko

# Class for handling all jobs being delt to a cluster
class RemoteInterface:
    'A Class for Remotely Accessing Cluster/Other Computer Systems'

    def __init__(self, hostname, args, username='mklein', password=None):
        self.hostname = hostname
        if username=='':
            username=None
        self.username = username
        if password=='':
            password=None
        self.password = password
        self.args = args
        return

    def displayRemoteInterface(self):
        print '''
Hostname:  %s
Username:  %s
Password:  %s
''' % (self.hostname, self.username, self.password)
        return

    def submit_job(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.hostname, username=self.username, password=self.password)
        ftp = ssh.open_sftp()
        ftp.put('simpredRawData.npz','simpredRawData.npz')
        ftp.close()
        print self.args
        ssh.exec_command('python2.7 ~/six_models.py ' + ' '.join(self.args))
        ssh.close()

# Function for User Input
def interface_generate():
    hostname = str(raw_input('What is the cluster hostname from your computer?  '))
    
    check1 = str(raw_input('Does your cluster require a username (Y/n)?  '))
    if check1 == 'Y' or check1 == 'y':
        username = str(raw_input('What is the username for the cluster?  '))
    elif check1 == 'N' or check1 == 'n':
        username = None
    else:
        print 'Input incorrect, please try again'
        exit()
    
    check2 = str(raw_input('Does your cluster require a password(Y/n)?  '))
    if check2 == 'Y' or check2 == 'y':
        password = str(raw_input("what is the password for the cluster?  "))
    elif check2 == 'N' or check2 == 'n':
        password = None
    else:
        print 'Input incorrect, please try again'
        exit()
    return hostname, username, password

# A main function for testing
def main():
    job1 = RemoteInterface('10.188.181.234', args=['-e','-row9','[1,2,3,4,5,6,7,8,9,10]','-svm'])
    job1.submit_job()
    #job1.displayRemoteInterface()
    return

if __name__=='__main__':
    main()


