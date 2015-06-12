from __future__ import print_function
from TestBase import TestBase 
from util       import run_cmd, capture
import stat, os

class SSH_Perm(TestBase):
  
  error_message=""

  def __init__(self):
    pass

  def setup(self):
    pass

  def __write_group_other_test(self, path):
    #Return grpW/othw=true if the group and other write permission exist!
    st   = os.stat(path)
    grpW = bool(st.st_mode & stat.S_IWGRP)
    othW = bool(st.st_mode & stat.S_IWOTH)

    return [ { 'name' : 'group','value': grpW},
             { 'name' : 'other','value': othW},
           ]

  def __read_user_test(self, path):  
    #Return userR=true if the user read permission does NOT exist!
    st   = os.stat(path)
    userR = not bool(st.st_mode & stat.S_IRUSR)
    return [ { 'name' : 'user','value': userR}]

  def __authorized_keys_test(self, fn):
    st   = os.stat(fn)

    # test 600 permission on ~/.ssh/authorized_keys
    perm = bool(st.st_mode & ( stat.S_IXUSR |
                               stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP |
                               stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH ))
    
    # if the file is not user readable
    perm = perm | (not bool(st.st_mode & stat.S_IRUSR))
    
    # test ownership
    own  = st.st_uid != os.getuid()
    return perm or own

  def description(self):
    return "Check SSH Permission:"

  def help(self):
    print(  "        Make sure you have a .ssh directory under your $HOME directory.\n",
	    "       The following commands can set the proper permissions:\n",
	    "       $ chmod 700 $HOME   #(use 750 or 755 when necessary)\n",
	    "       $ chmod 700 $HOME/.ssh\n",  
            "       $ chmod 600 $HOME/.ssh/authorized_keys\n",
	    "       $ chmod 600 $HOME/.ssh/id_rsa\n",
	    "       $ chmod 644 $HOME/.ssh/id_rsa.pub\n",
            "       $ chown `whoami` $HOME/.ssh/authorized_keys\n"
            )

  def error(self):
	print(self.error_message)

  def execute(self):
    result = True

 #  home = os.environ['HOME']
    userid=capture("whoami").rstrip()
 #  grepcmd="grep %s /etc/passwd | cut -d ':' -f6" %userid
    grepcmd="/bin/awk -F: -v user=%s '$1 == user {print $6}' </etc/passwd" %userid
    home=capture(grepcmd)
    if not home:
        self.error_message+="        Error: Can not find home directory!\n"
        return False
    home=home[:-1]

    sshD = os.path.join(home,".ssh")
    dirA = [ home, sshD ]
    if not os.path.isdir(sshD):
      self.error_message+="        Error: .ssh directory does not exist or is inaccessible!\n"
      return False
    
    keyfile=os.path.join(sshD,"authorized_keys")
    if not os.path.isfile(keyfile):
      self.error_message+="        Error: Authorized key file does not exist or is inaccessible!\n"
      return False
    
    for d in dirA:
      a = self.__write_group_other_test(d)
      for entry in a:
        if (entry['value']):
          result = False
          self.error_message+="        Error: "+entry['name']+ " permission on " + d +" is bad!\n"	  
   
      a = self.__read_user_test(d)
      for entry in a:
        if (entry['value']):
           result = False
           self.error_message+="        Error: "+entry['name']+ " permission on " + d +" is bad!\n"
 
    # test owner and perm on ~/.ssh/authorized_keys
    r = self.__authorized_keys_test(keyfile)
    if (r):
      result = False
      self.error_message+="        Error: The permission and/or ownership on " + keyfile +" is bad!\n"
      
    return result
   
  def name(self):
    return "Check SSH Permission" 
