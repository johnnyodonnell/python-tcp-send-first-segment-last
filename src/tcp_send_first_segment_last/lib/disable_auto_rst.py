import socket
import subprocess



# Need this to prevent OS from automatically responding to TCP SYN
# with a RST response.
# This is kind of a hack, and I should try to find a better
# way to mitigate the OS behavior. However, I think this is
# better than creating a routing rule.
# I first tried mitigating this by opening a dummy port;
# however, I was not able to get that to work. And
# I have resorted to creating a routing rule.

def add_ip_table_entry():
    subprocess.run([
        "iptables", "-A", "OUTPUT", "-p", "tcp",
        "--tcp-flags", "RST", "RST",
        "-j", "DROP"])

def remove_ip_table_entry():
    # iptables -D OUTPUT -p tcp --tcp-flags RST RST -j DROP
    for i in range(0,3):
        subprocess.run([
            "iptables", "-D", "OUTPUT", "-p", "tcp",
            "--tcp-flags", "RST", "RST",
            "-j", "DROP"])

def open_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", port))
    sock.listen(0x7FFFFFFF)
    return sock

def cleanup():
    remove_ip_table_entry()
    pass

def disable(port):
    # sock = open_port(port)
    add_ip_table_entry()

    def cleanup_lambda():
        # sock.close()
        cleanup()

    return cleanup_lambda

