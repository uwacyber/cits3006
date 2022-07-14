# Lab 1: Security tools (NOT READY)

The aim of this lab is to introduce you to some useful security tools commonly used to get familiar with attack styles, as well as practice Linux commands from Lab 0 in the context.

The tools we will cover are: `wireshark`, `nmap` and `metasploit`, the tools that are often used to gather information and gain the first step into the target host(s). Those tools are already installed on your Kali Linux. Of course, we will cover more useful and interesting tools later on as well.

## 1.0. vulnerable VM: metasploitable

First, we will set up a vulnerable VM named [_metasploitable_](https://docs.rapid7.com/metasploit/metasploitable-2) (click the link and download the VM).

If your machine uses an Intel chip AMD64, you can move on to the next tasks.

If your machine uses an Apple Silicon ARM64, you must do the following tasks to run metasploitable on UTM:

1. Install [brew](https://brew.sh/) if not done already
2. Install qemu from the terminal: `brew install qemu`
3. Navigate to the directory containing the metasploitable image file you downloaded
4. Convert image: \
   `qemu-img convert -p -O qcow2 Metasploitable.vmdk Metasploitable.qcow2`
5. Open UTM: add new -> Emulate -> Other -> skip ISO
6. Settings -> remove drive
7. Settings -> QEMU -> untick "UEFI boot"
8. Settings -> add drive -> select the created image (`.qcow2` file) from step 4
9. Start the VM

Please note, that the VMs used in the lab should be able to reach each other (test using `ping`).

## 1.1. wireshark



## 1.2. nmap

## 1.3. metasploit
