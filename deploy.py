import paramiko


def ssh_checkout(host, user, passwd, cmd, text, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=user, password=passwd, port=port)
    stdin, stdout, stderr = client.exec_command(cmd)
    exit_code = stdout.channel.recv_exit_status()
    out = stdout.read().decode("utf-8")
    err = stderr.read().decode("utf-8")
    client.close()
    if (text in out and exit_code == 0) or text in err:
        return True
    else:
        return False


def upload_files(host, user, passwd, local_path, remote_path, port=22):
    print(f'Upload file {local_path} to folder {remote_path}')
    transport = paramiko.Transport((host, port))
    transport.connect(None, username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(local_path, remote_path)
    if sftp:
        sftp.close()
    if transport:
        transport.close()


def download_files(host, user, passwd, local_path, remote_path, port=22):
    print(f'Download file {local_path} from {remote_path}')
    transport = paramiko.Transport((host, port))
    transport.connect(None, username=user, password=passwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.get(remote_path, local_path)
    if sftp:
        sftp.close()
    if transport:
        transport.close()


def deploy():
    res = []
    upload_files("0.0.0.0", "user2", "user2", "p7zip-full.deb", "/home/user2/p7zip-full.deb")
    res.append(ssh_checkout("0.0.0.0", "user2", "user2", "echo 'user2' | sudo -S dpkg -i /home/user2/p7zip-full.deb", "Setting up"))
    res.append(ssh_checkout("0.0.0.0", "user2", "user2", "echo 'user2' | sudo -S dpkg -s p7zip-full", "Status: install ok installed"))
    # res.append(ssh_checkout("0.0.0.0", "user2", "user2", "echo 'user2' | sudo -S dpkg -r p7zip-full", "Removing"))
    # res.append(ssh_checkout("0.0.0.0", "user2", "user2", "echo 'user2' | sudo -S dpkg -s p7zip-full", "deinstall ok"))
    return all(res)


if __name__ == "__main__":
    if deploy():
        print("Deploy succesfull")
    else:
        print("Error deploy")



