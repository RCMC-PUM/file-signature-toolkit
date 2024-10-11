from paramiko import SSHClient
from scp import SCPClient
from pathlib import Path
import paramiko

import sys


def progress(filename, size, sent):
    sys.stdout.write(
        f"progress: {(filename, float(sent) / float(size) * 100)}"
    )


class Connection:
    def __init__(self, address: str, port: int, user: str, password: str, host_public_key: str):
        self.address = address
        self.port = port
        self.user = user
        self.password = password
        self.host_public_key = host_public_key

    def __repr__(self) -> str:
        return f"""
                Address: {self.address}
                User: {self.user}
                Password: {'*' * len(self.password)}
                Port: {self.port}
                
                Public key file: {self.host_public_key}
                """

    def upload(self, file: Path | str, output: Path | str) -> None:
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.RejectPolicy())  # Reject unknown host keys

        ssh.connect(
            hostname=self.address,
            port=self.port,
            username=self.user,
            password=self.password,
        )

        scp = SCPClient(ssh.get_transport(), progress=progress)
        scp.put(str(file), str(output))
        scp.close()

    def download(self, file: Path | str, output: Path | str) -> None:
        ssh = SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.RejectPolicy())  # Reject unknown host keys

        ssh.connect(
            hostname=self.address,
            port=self.port,
            username=self.user,
            password=self.password,
        )

        scp = SCPClient(ssh.get_transport(), progress=progress)
        scp.get(str(file), str(output))
        scp.close()
