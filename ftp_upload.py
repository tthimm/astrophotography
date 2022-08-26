import ftplib

def ftp_upload(self, file):
    try:
        remote_path = 'astrophotography'
        ftp = ftplib.FTP()
        ftp.connect(self.config['FTP']['Host'])
        ftp.login(self.config['FTP']['User'], self.config['FTP']['Password'])
        my_file = open(file, 'rb')
        try:
            ftp.mkd(remote_path)
        except BaseException as e:
            pass
        else:
            ftp.cwd(remote_path)
            ftp.storbinary("STOR upload1.png", my_file)
    except BaseException as e:
        print("+++ Upload failed")
        print("+++ Unexpected: {0}".format(e))
    finally:
        ftp.quit()