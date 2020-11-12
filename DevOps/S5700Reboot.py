from telnetlib import Telnet
import time

def telnet_on(command: str):
    tn = Telnet("10.10.10.1", port=23, timeout=10)
    # tn.set_debuglevel(2)
    tn.read_until(b"Username:")
    tn.write(b'admin\n')
    tn.read_until(b"Password:")
    tn.write(b"admin@123\n")
    #tn.read_until(b"Chaos")
    time.sleep(5)
    tn.write(b"system-view\n")
    tn.write(command.encode('ascii') + b'\n')
    time.sleep(2)
    result_list = []
    # command_result = tn.read_very_eager().decode("ascii")
    # print(command_result)
    while (True):
        command_result = tn.read_very_eager().decode('utf-8')
        result_list.append(command_result)
        if '---- More ----' in command_result.strip():
            tn.write(b" ")
            time.sleep(0.5)
        else:
            break
    result_str = "\n".join(result_list)
    return result_str

if __name__ == '__main__':
    result = telnet_on("reboot")
    print(result)