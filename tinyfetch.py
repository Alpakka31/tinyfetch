#!/usr/bin/python3

import socket, platform, subprocess, os, pwd
from shutil import which
from pathlib import Path

# Define constants containing colour codes
RED = "\033[1;31m"
GREEN = "\033[1;32m"
NC = "\033[0m"

def fetch_username() -> str:
    return pwd.getpwuid(os.getuid())[0]

def fetch_hostname() -> str:
    return socket.gethostname()

def fetch_debian_ver() -> str:
    debian_version = Path("/etc/debian_version").read_text().replace("\n", "")
    return debian_version

def fetch_kernel_ver() -> str:
    return platform.release()

def fetch_uptime() -> str:
    uptime = subprocess.run(["uptime", "-p"], stdout=subprocess.PIPE).stdout.decode("utf-8")
    return uptime.replace("up ", "").replace("\n", "")

def fetch_pkgs_amount() -> int:
    pkgs = subprocess.run(["dpkg", "-l"], stdout=subprocess.PIPE).stdout.decode("utf-8")
    counter = 0
    for line in pkgs.splitlines():
        if line.startswith("ii"):
            counter += 1
    return counter

def fetch_user_shell() -> str:
    return os.readlink("/proc/%d/exe" % os.getppid()).split("/")[-1]

def fetch_wm() -> str:
    # Xprop command wasn't found
    if which("xprop") is None:
        return "unknown"

    xprop_id = subprocess.run(["xprop", "-root", "-notype", "_NET_SUPPORTING_WM_CHECK"], stdout=subprocess.PIPE).stdout.decode("utf-8").replace("\n", "")
    xprop_id = xprop_id.split("#")[-1].lstrip() # Get ID after character '#' and strip whitespace from the left side
    xprop_wm = subprocess.run(["xprop", "-id", xprop_id, "-notype", "-len", "25", "-f", "_NET_WM_NAME", "8t"], stdout=subprocess.PIPE).stdout.decode("utf-8").replace("\n", "")
    return xprop_wm.split('"')[1::2][0] # Get string that's between quotation marks

def main():
    # Print logo plus system information
    print(f"{RED}    _____     {RED}{fetch_username()}@{fetch_hostname()}{NC}")
    print(f"{RED}   /  __ \\    {GREEN}OS{NC} Debian GNU/Linux {fetch_debian_ver()}")
    print(f"{RED}  |  /    |   {GREEN}Kernel{NC} {fetch_kernel_ver()}")
    print(f"{RED}  |  \\___-    {GREEN}Uptime{NC} {fetch_uptime()}")
    print(f"{RED}  -_          {GREEN}Pkgs{NC} {fetch_pkgs_amount()}")
    print(f"{RED}    --_       {GREEN}Shell{NC} {fetch_user_shell()}")
    print(f"              {GREEN}WM{NC} {fetch_wm()}")

if __name__ == "__main__":
    main()
