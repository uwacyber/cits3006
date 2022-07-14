# Lab 1: Security tools (NOT READY)

The aim of this lab is to introduce you to some useful security tools commonly used to get familiar with attack styles, as well as practice Linux commands from Lab 0 in the context.

The tools we will cover are: `wireshark`, `nmap` and `metasploit`, the tools that are often used to gather information and gain the first step into the target host(s). Those tools are already installed on your Kali Linux. Of course, we will cover more useful and interesting tools later on as well.

{% hint style="info" %}
In this lab, we will be running at least two VMs: Kali and metasploitable.
{% endhint %}

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

Nmap is blah blah



Nmap can be used to scan the network to find vulnerable host(s). This can be done by scanning the IP range.&#x20;

`$ nmap -sn [target IP range]`

e.g.,

`$ nmap -sn 192.168.64.0/24`

![](<../.gitbook/assets/image (3).png>)

Here, the flag `-sn` indicates that it uses ping to check whether the host exists or not. So if the host does not respond to pings, it won't be listed here. There are other flags that could be used, which you can find more from [>>here<<](https://nmap.org/book/man-briefoptions.html).

One of the listed addresses should be your victim machine (metasploitable VM).&#x20;

{% hint style="warning" %}
If you don't see your metasploitable VM in the list, please check your network settings.
{% endhint %}

Now we have discovered our target machine, we can scan to see which ports are open (i.e., what services are running).

`$ nmap -sV -O -T4 192.168.64.5`

{% hint style="info" %}
Find out what those flags mean.
{% endhint %}

Then we should be able to see something like:

![](<../.gitbook/assets/image (6).png>)



## 1.3. Metasploit

For this part of the lab, we will carry out a few exploits using the Metasploit framework. The Metasploit framework is essentially a collection of scripts that performs the described exploit, and most scripts are targeting vulnerabilities on networks and servers. The Metasploit framework is open-source, so it can also be customised to various needs. So let's have a look at a few exploit examples in this lab.

First, you may need to update it to the latest version.

`$ sudo apt update -y; sudo apt install Metasploit-framework -y`

From the nmap scan above, we have discovered the IP address of our target (metasploitable VM) machine and the services running. The first one we will exploit is the one at the top at port 21 - the ftp service.

### 1.3.1. Exploit FTP

The Nmap scan revealed the version of the FTP on the target machine. If you search for vulnerabilities associated with the given version `vsftpd 2.3.4`, you will quickly discover that there is a backdoor vulnerability (more precisely, [`CVE-2011-2523`](https://www.cvedetails.com/cve/CVE-2011-2523/)). The CVSS Score is 10, indicating that the impact of this vulnerability is severe.&#x20;

Since it's there, we'll exploit it. Launch the Metasploit from the terminal:

`$ msfconsole`

![](<../.gitbook/assets/image (5).png>)

From the msfconsole, we can search for the identified service-related exploits

`$ use vsftpd`

![](<../.gitbook/assets/image (4).png>)

In fact, there is only one exploit (the backdoor one) available, so it will be automatically be selected. If it is not automatically selected, just type: `use 0` (i.e., the number 0th exploit) to select it.

{% hint style="info" %}
If you already know the exploit to use and its path, you can type in:

`use [path to the exploit]`
{% endhint %}

Next, we need to check options to see what inputs the exploit requires.

`$ show options`

![](<../.gitbook/assets/image (2).png>)

The exploit is actually simple, and only requires the target host's IP address. So set the RHOST with the target IP address found using Nmap (the RPORT is already set, but if the FTP service runs on a different port or if the RPORT is not set, you can update/set it).

`$ set RHOST 192.168.64.5`

![](<../.gitbook/assets/image (1).png>)

All options are set, so now we can run the exploit by simply typing `run`.

![](../.gitbook/assets/image.png)

{% hint style="info" %}
The exploit may fail (as shown above), but you can simply run it again.
{% endhint %}

Now you have a remote shell on your target host! Try navigating, creating files, deleting files etc., and observe from your metasploitable VM to see those changes.

#### How does this exploit work?

This vulnerability came about when someone had uploaded a modified version of `vsftpd` to the master site and some users downloaded this version for their systems (i.e., it came with the backdoor). The backdoor opened port 6200 to give the attacker a command shell.

This showed the importance of authentication and authorisation (don't let anyone upload/update important data) and the ability to check and approve changes.&#x20;

#### Finishing

Finally, you can press `ctrl + C` to end the session. If you are finished with the exploit, you can type `back` to go back to the main `msfconsole` menu.

### 1.3.2. Exploit SSH

Okay, so the previous one is highly unlikely given the vulnerable service is more than a decade old and people have moved on. So let's try some other exploits - SSH!

