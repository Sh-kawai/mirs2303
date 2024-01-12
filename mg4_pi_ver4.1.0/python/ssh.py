import paramiko
import threading

from define import *

def execute_command(hostname, username, password, command):
    # SSHセッションの開始
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # SSH接続
        ssh.connect(hostname, username=username, password=password)

        # コマンドの実行
        stdin, stdout, stderr = ssh.exec_command(command)
        print(command)

        # 実行結果の取得
        output = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")

        # 結果の表示
        if output:
            print(f"Command Output:\n{output}")
        if error:
            print(f"Command Error:\n{error}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # SSHセッションの終了
        ssh.close()

def bringup_jetson():
    command_to_execute = "/home/mirs2303/mirs2303/mg4_jetson/bringup.bash"
    thread = threading.Thread(target=execute_command, kwargs={"command": command_to_execute, "hostname":JETSON_IP, "username":JETSON_USER, "password":JETSON_PASS}, daemon=True)
    thread.start()

# SSH接続とコマンド実行
if __name__ == "__main__":
    bringup_jetson()
