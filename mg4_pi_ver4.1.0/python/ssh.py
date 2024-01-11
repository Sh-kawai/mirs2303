import paramiko

from define import *

def execute_command_on_jetson(hostname, username, password, command):
    # SSHセッションの開始
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # SSH接続
        ssh.connect(hostname, username=username, password=password)

        # コマンドの実行
        stdin, stdout, stderr = ssh.exec_command(command)

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

# SSH接続とコマンド実行
if __name__ == "__main__":
    # JetsonのIPアドレス、ユーザー名、パスワードを設定

    # 実行するコマンドを設定
    command_to_execute = "cd cals -l"
    execute_command_on_jetson(JETSON_IP, JETSON_USER, JETSON_PASS, command_to_execute)
