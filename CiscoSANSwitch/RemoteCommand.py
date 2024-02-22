import socket
import errno
import os, time
import paramiko
import traceback
from paramiko.ssh_exception import AuthenticationException, SSHException


class RemoteCommand():

    SSH_RETRY_INTERVAL = 30

    def __init__(self, host, user, password, cmd = None, args = [], port=22, retry=5):

        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._cmd = cmd
        self._args = " " . join(args)
        self._ssh = ""
        self._sftp = ""
        self._transport = ""
        self._std_out = ""
        self._std_err = ""
        self._ret_code = ""
        self.ssh_connect(retry)
        #self.sftp_connect(retry)

    def ssh_connect(self, retry=5):
        try:
            self._ssh = paramiko.SSHClient()
            self._ssh.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            self._ssh.connect(self._host,
                        username = self._user,
                        password = self._password)
        except (AuthenticationException, socket.error, SSHException) as e:
            retry = retry - 1
            if retry <= 0:
                raise

            print("SSH connect failed: %s retrying...in %s secs"
                       % (str(e), RemoteCommand.SSH_RETRY_INTERVAL))

            time.sleep(RemoteCommand.SSH_RETRY_INTERVAL)

            self.ssh_connect(retry)
        except:
            raise

        return True

    def sftp_connect(self, retry=5):
        try:
            self._transport = paramiko.Transport(self._host, self._port)
            self._transport.connect(username=self._user, password=self._password)
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        except (AuthenticationException, socket.error, SSHException) as e:
            retry = retry - 1
            if retry <= 0:
                raise
            print("SFTP connect failed: %s retrying...in %s secs"
                       % (str(e), RemoteCommand.SSH_RETRY_INTERVAL))
            time.sleep(RemoteCommand.SSH_RETRY_INTERVAL)
            self.ssh_connect(retry)
        except:
            raise

        return True

    def execute(self, cmd=None, args=None):
        if not cmd:
            cmd = self._cmd

        if not args:
            args = self._args
        
        if type(args) is list:
            args = ' '.join(args)

        cmd = "%s %s" % (cmd, args)

        print("Executing command %s" % cmd)

        try:
            stdin, stdout, stderr = self._ssh.exec_command(cmd)

            ret_code = stdout.channel.recv_exit_status()

            self.set_std_out(stdout)
            self.set_std_err(stderr)
            self.set_err_code(ret_code)

            print("Command Execution Successful..")
            #print("Command STDOUT  : \n%s"%self.get_std_out())
            print("Command STDERR  : \n%s"%self.get_std_err())
            print("Command RetCode : \n%s"%self.get_err_code())
        except:
            raise

        return True

    def change_system_time(self,date_string):
        cmd = "date"
        args = ['-s',"'%s'" % date_string]

        try:
            self.execute(cmd, args)
            self.execute('hwclock', ['--systohc'])
        except:
            raise

        return True

    def sync_ntp_date(self,ntp_server):
        cmd="ntpdate"
        args=[ntp_server]

        try:
            self.execute(cmd, args)
        except:
            raise

        return True


    def download(self, remote_path, local_path=None):
        try:
            self._std_out = self._sftp.get(remote_path, local_path)
        except:
            raise

    def upload(self, local_path, remote_path=None):
        try:
            self._std_out = self._sftp.put(local_path, remote_path)
        except:
            raise

    def is_exists(self, path):
        """os.path.exists for paramiko's SCP object
        """
        try:
            self._sftp.stat(path)
        except IOError as e:
            if e.errno == errno.ENOENT:
                return False
            raise
        else:
            return True

    def set_std_out(self,stdout):
        output = "".join(stdout.readlines())
        self._std_out = output

    def get_std_out(self):
        return self._std_out

    def set_std_err(self,stderr):
        output = "".join(stderr.readlines())
        self._std_err = output

    def get_std_err(self):
        return self._std_err

    def set_err_code(self,ret_code):
        self._ret_code = ret_code

    def get_err_code(self):
        return self._ret_code

    def succeeded(self):
        if self.get_err_code() == 0:
            return True
        else:
            return False

    def ftp_close(self):
        try:
            self._sftp.close()
            self._transport.close()
        except:
            raise

    def copy(self, localpath, remotepath):
       try:
           sftp = self._ssh.open_sftp()
           sftp.put(localpath, remotepath)
           sftp.close()
       except Exception as e:
           raise CopyOverSFTPFailed("Copy Failed: %s : Specify full destination path with filename" % e)

class CommandNotExecutedException(Exception):
    pass
class CommandNotFoundException(Exception):
    pass
class CommandCompletedException(Exception):
    pass
class CommandOSNotSupportedException(Exception):
    pass
class CopyOverSFTPFailed(Exception):
    pass
