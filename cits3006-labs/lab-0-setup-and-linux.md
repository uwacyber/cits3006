# Lab 0: Setup and Linux

## 0.1. Setup VM and Docker

You will be using Kali as your based VM, and likely various other VM images and/or Docker containers to carry out labs and the project. So it is essential that you setup your system to be able to use them wherever required.

{% hint style="info" %}
If you already have VM and Docker set up and running on your machine, you can skip to [Section 0.2](lab-0-setup-and-linux.md#0.2-linux-refresher) (and maybe revisit here later if things aren't working as intended).
{% endhint %}

### 0.1.1. VM setup

We will be using [Kali Linux](https://www.kali.org/) as our base VM (the bare metal option), as it comes with various tools we will be using already. Kali also has native builds for both AMD64 and ARM64 (see below), so it is easy to have it ready on most of our machines. Please see below for recommendations if you haven't used a VM before (minimum instruction provided, you are required to do your own research for setting up VMs on your machine):

{% hint style="danger" %}
In general, you are expected to troubleshoot your setup issues yourself (we already did this in your first year). We will still try to help you with your setup issues, but the helpers will prioritise helping lab-related questions first especially if the labs are very busy.
{% endhint %}

#### Windows, Linux or Mac using Intel chips AMD64

* You should be good using [VirtualBox](https://www.virtualbox.org/) - all instructions for AMD64 will be based on using VirtualBox.
* If it doesn't work well, you can try using [VMware Workstation Player](https://www.vmware.com/au/products/workstation-player.html).
* If the above two fail, please contact the lab facilitator.

{% hint style="warning" %}
A typical issue people have running VMs on Windows machines are that you have Hyper-V on. You should research and turn it off if your VMs have issues.
{% endhint %}

#### Mac using Apple Silicon chips ARM64 (M1 series, M2 etc.)

* You can use [UTM](https://mac.getutm.app/) - all instructions for ARM64 will be based on using UTM.
* You can also use other apps like [Parallels](https://www.parallels.com/au/products/desktop/) only if you prefer, but it would not be required.

{% hint style="warning" %}
Apple Silicon machines still have a lot of incompatibility issues, so not all functionalities may be available to use. Best efforts are made to do the labs on AS machines, but we may not be able to help you if you used different tools and face problems.
{% endhint %}

### 0.1.2. Docker setup

The process for installing Docker Desktop is straightforward and involves using the installer for the particular operating system you have (from the drop-down menu, select the appropriate OS):

{% embed url="https://www.docker.com/get-started" %}

It is recommended to use Docker within your VM (e.g., Kali) if needed, especially when handling malicious files, carrying out tasks that could damage your system, etc. You will be advised of such activities in the labs.

## 0.2 Linux refresher

This lab is to provide a refresher on your Linux knowledge, and you can do this on your Kali VM. You may skim/skip through this lab if you feel confident, but if you haven't done much in Linux for a while (a semester or two), you are strongly advised to complete this lab before moving on to other labs to improve your workflow efficiency. For each example, you should try it yourself before moving on to the next section.

### 0.2.1. Distributions

The base system of Linux comes in many different distributions which contain different packages and features written by different groups. These are referred to as distros for short, and they have a wide variety of different uses, purposes, systems, features, and fan bases. This guide will attempt to be distro-independent, however, a few of the more popular distros are listed:

| <p>· Ubuntu</p><p>· Debian</p><p>· Fedora</p><p>· Linux Mint</p> | <p>· Red Hat</p><p>· CentOS</p><p>· Arch Linux</p><p>· Gentoo</p> |
| ---------------------------------------------------------------- | ----------------------------------------------------------------- |

### 0.2.2. Package manager and repositories

Each distribution comes with a package manager, which handles software installed on the system and has a number of remote repositories from which it gets its software. For example, Ubuntu (also Kali) uses a package manager called aptitude (apt for short). You can type:

`sudo apt-get install firefox`

to install the Mozilla Firefox web browser. It will search the remote repositories (listed in `/etc/apt/-sources.list`) for the required packages and instructions to install them and once found, it will install the software on your computer for you. The package manager can also update and remove software, and manage your local package database. This is one of the brilliant things of a package manager: you can run a single command and you've installed new software - You can run a single command, and update all your packages, etc.

{% hint style="info" %}
`apt-get` is the package manager for Ubuntu. Fedora uses `dnf` (previously `yum`), Arch uses `pacman`, and Debian uses aptitude, etc. For instance:

`yum install firefox`

will install Firefox on a Fedora machine. You can also install multiple package managers on any one distro, but as they say\_: too many cooks spoil the broth\_.
{% endhint %}

### 0.2.3. The Terminal

**0.2.3.1. Commands**

Firstly you should get familiar with the man pages, which are essentially the manual, and will display help pages on almost all commands.

`Usage: man COMMAND`

Where COMMAND is replaced with whatever command you want help on. Press '`q`' to exit a manual page. Alternatively, most commands will allow you to add `--help` on the end to get their own personal help pages. Here is a list of the essential commands that you should become familiar with (and you can use the manual to learn how to use them):

`cd ------ # Change directory`\
`ls ------ # Show contents of directory`\
`echo ---- # Print text to the screen`\
`cat ----- # Display contents of a file`\
`nano ---- # Edit a file via the command line`\
`mv ------ # Move (or rename) a file`\
`cp ------ # Copy a file`\
`rm ------ # Remove (delete) a file`

These are some extra commands which aren't totally essential but are certainly helpful:

`mkdir --- # Make a new directory`\
`rmdir---- # Delete a directory`\
`grep ---- # Search for specific text within text`\
`pwd ----- # Print working (current) directory`\
`whoami -- # Display user`\
`ps ------ # Display running processes`\
`pstree -- # Display a tree showing running processes and processes they started`\
`top ----- # Display most intensive running programs`\
`who ----- # Display logged on users`\
`w ------- # Display logged on users`\
`which --- # Display the path to a command's binary`\
`df ------ # Disk space free`\
`du ------ # Disk space used`\
`passwd -- # Change user password (not to be confused with pwd)`\
`more ---- # Display text one screenful at a time`\
`less ---- # Display text one screenful at a time`\
`wc ------ # Word/letter/byte count`\
`id ------ # Display the uid, gid and groups of a user`\
`su ------ # Switch user`\
`tty ----- # Display which tty you are on`

####

#### **0.2.3.2. Shortcuts**

Every key pressed ends a character to the terminal, and you can send different characters by holding down keys like \[Ctrl] or \[Alt]. This is how the shell can tell what key is pressed, and thus, allow shortcuts to be defined. Some of the more useful keyboard shortcuts are defined:

* `Up or Down arrows :` Scroll through typed commands
* `Home or End :` Move to the start or end of a line, respectively
* `Tab :` Autocomplete a file name, directory name or command name.
* `Ctrl + C :` End a running process
* `Ctrl + D :` End an End-Of-File (EOF) character (usually ends a process or signifies the end of input data)
* `Ctrl + Z :` Send the currently running process to the background
* `Ctrl + L :` Clear the screen, same as running the clear command

####

#### 0.2.3.3. **Piping and redirection**

There are a number of little quirks that the shell has that gives it more functionality. Piping takes the `stdout` of the left program and connects it (i.e. _pipes_ it) into `stdin` of the right program with the pipe operator `|`. For example:

`# Count number of words in helloworld.txt`\
`cat helloworld.txt | wc -w`

Redirection directs data in and out of files, i.e.

`# Redirect stdout to file`\
`echo "Hello world" > helloworld.txt`\
``\ `# Redirect stdout to the end of a file`\ `echo "world." >> hello.txt`\``\
`# Redirect a file to stdin`\
`more < helloworld.txt`

####

#### **0.2.3.4. Wildcards**

The shell uses a number of special characters called wildcards, similar to regular expressions or regex, which can be used to manipulate what is being dealt with on the command line. The standard wildcards are thus:

`*` Match 0 or more characters. For example, `rm *.txt` will delete all files that end in .txt, and `cp somedirectory/* .` will copy all files from \`somedirectory' to the current directory.

`?` Match any single character. For example, `cp example.?` will copy all files named \`example' with a single character extension, into the directory \`somedir'

`[]` Match any single character in the square brackets. You can even specify a range, i.e. `rm m[a-e]m` will delete any files starting and ending with `m`, and with any letter between \`a' and \`e' in between. `rm m[abc]m` will delete files \`mam', \`mbm', \`mcm'.

`{}` Match any item in the braces. For example, `cp {*.doc,*.pdf} ~` copies any files with the extension \`.doc' or \`.pdf' to the home directory.

**0.2.3.5. Conditional execution**

You can chain commands together on one line by separating them with a semicolon \`;'.

`cmd1; cmd2; cmd3`

However, every program returns a number back to the OS once it has finished running to tell if it was completed successfully or not, and we can use this to chain execute commands conditionally.

To run a command if and only if the last command completed successfully, we use `&&`:

`user@MY-PC:~$ mkdir foo && cd foo && echo "hooray" > somefile`\
`user@MY-PC:~/foo$ cat somefile`\
`hooray`\
`user@MY-PC:~/foo$`

To run a command if and only if the last command failed, we use `||`:

`user@MY-PC:~$ ls foo || cd foo || mkdir foo && ls -ld foo`\
`ls: cannot access foo: No such file or directory`\
`bash: cd: foo: No such file or directory`\
`drwxrwxr-x 2 user user 4096 May 24 00:57 foo`

#### **0.2.3.6. Processes**

Every program that runs, runs in virtual memory as a process, even the shell. You can list the currently running processes with the command `top`. When you run a command, the terminal session runs it on its process, waits for it to complete, then regains control once the command is finished. So, if you were to close the terminal window while a command was running, that would stop the command. Since this can be inconvenient, we can \`fork' the command into its own process to run in the background, and still use the shell while it runs (which is useful for commands that take a long time). To do this, we end the command with a single ampersand `&`. For example:

`user@MY-PC:~$ (sleep 15; date) & date`\
`[1] 12186`\
`Thu May 24 02:06:14 AWST 2022`\
`user@MY-PC:~$`\
`user@MY-PC:~$ Thu May 24 02:06:29 AWST 2022`\
\`\`\
`[1]+ Done ( sleep 15; date )`\
`user@MY-PC:~$`

`(sleep 15; date)` is sent to the background and returns the process ID (PID), then the next date is run and the shell is returned. After sleeping for 15 seconds, the date sent to the background outputs and the shell reports that the command completed.

There is a command, `nohup` (no hangup), which prevents a program from being forcefully terminated under normal circumstances. We can combine this with `&` to run programs that need to run uninterrupted for long periods of time.

Another way to list the processes running is with `ps`, and then end them with `killall` (kill by process name), or with `pkill` (kill by process ID), or even with the keyboard shortcut \[Ctrl] + \[C] as mentioned above. Check the man page, as well as \[8] for more options.

You can also check what is running in the background and foreground with `bg` and `fg`, respectively.

### 0.2.4. File system structure

The file system is structured as a tree that flows down from the root directory, which is simply represented as /. Below shows an example listing of a system’s root directory using the ls command:

`user@MY-PC:~$ ls /`\
`bin   etc        initrd.img.old lost+found proc selinux usr`\
`boot  fixdm      lib            media      root srv     var`\
`cdrom home       lib32          mnt        run  sys     vmlinuz`\
`dev   initrd.img lib64          opt        sbin tmp     vmlinuz.old`

The standard path is listed as all the directories to a file, separated by the `/` character. You can also use `..` to represent the folder that the current folder is in, `.` to represent the current directory, and `~` to represent your home directory. For example

`# Move two folders up, then into dir1 and then dir2, then back into dir1, then back into dir2`\
`cd ../../dir1/dir2/../dir2`\
`# Get a listing of the current directory`\
`ls .`\
`# Change into your home directory`\
`cd ~`

Linux will automatically complete a command or filename if you are part-way through typing it; all you have to do is hit the \[Tab] key. Press \[Tab] enough times and it will list possible suggestions based on what you currently have typed in the terminal.

#### ****

#### **0.2.4.1. File operations**

There are a number of useful programs that allow us to do file manipulation. To list some of the main operations:

|   `cp` | Copy a file from one location to the other.                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| -----: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
|   `mv` | Move a file from one location to the other. Note, this is also used to rename files - you just \`move' the file to the directory it is already in but as a new name, for example `mv foo bar` would rename the file from \`foo' to \`bar', assuming you didn't have a directory named \`bar', in which case, the file would be moved to that directory instead.                                                                                                                                              |
|   `rm` | Delete a file. Note that you can also delete empty directories this way, and you can delete a directory and its subdirectories by using `rm -r`. However, be **VERY** careful: if you were to run `rm -rf /`, you would erase every file on your whole computer, because it would delete the root directory and then every file and subdirectory below it and it wouldn't stop because the \`f' in \`-rf' means \`force'. Use `rm -rf` with extreme caution, or even use `rmdir`, which removes a directory. |
| `grep` | grep stands for Global Regular Expressions Parser, and can search through text for a match. For example, `grep foo bar` searches the file bar for the string foo, and you can also use `ls -l \| grep "foo"`, which searches the file listing for a file called foo. When combined with `sed` and `awk`, you can do almost anything string related.                                                                                                                                                          |

#### **0.2.4.2. $PATH and the environment**

Variables in the shell are defined using the export command, and when variables are used, they start with a `$`.\
\
`user@MY-PC:~$ export FOO="This is a string"`\
`user@MY-PC:~$ echo $FOO`\
`This is a string`

You can see a list of the set environment variables by typing `set` by itself into the terminal.

Linux uses a global terminal variable to find programs. This is the $PATH variable and it consists of a list of file paths to search in for a specified program, in order, separated by the colon (:). For example, a listing of my path:

`user@MY-PC:~$ echo $PATH`\
`/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games`

This would mean that if I were to use the command `ls`, it would search for a binary file called 'ls' in `/usr/local/sbin`, then in `/usr/local/bin`, and so on until it found it. Then it would be executed. Because these are searched in order, if you were to prepend a directory path to the front of `$PATH` with your own copy of `ls` in it, and then run the ls command, then your copy would be run instead.

This is sometimes used as an exploit by modifying the user's `$PATH` variable so that a path containing malicious binaries with the same names as common commands is on the front. When the user runs these commands, then the malicious binaries are run instead.

### 0.2.5. Users and Permissions

Every user has a user ID (uid) and a group ID (gid). Each user also has a list of groups they are a part of which give them the permissions that are assigned to those groups. You can see this by using the 'id' command:\
\
`user@MY-PC:~$ id`\
`uid=1000(user)gid=1000(user)groups=1000(user),4(adm),24(cdrom),27(sudo),29(audio),30(dip),44(video),46(plugdev),109(lpadmin),119(pulse),124(sambashare)`

#### ****

#### **0.2.5.1. sudo and root**

Now for the most powerful user on Linux: The root user. Root's uid and gid are both 0.

`user@MY-PC:~$ id root`\
`uid=0(root) gid=0(root) groups=0(root)`

The root account can do anything, while other accounts would be denied due to the lack of permissions required. Root is the first account created on a newly installed Linux distro, and it is generally encouraged that you do not use the root account unless you absolutely have to because since root can do anything, then there's no stopping you from accidentally deleting something important.

This is where the `sudo` command comes in (a.k.a "super-user do"). You can use `sudo` to execute commands that require elevated privileges without having to actually switch to root.

Say you want to edit the hostname file, which contains the name of your computer, but, by default, you need elevated privileges to edit it. You would type:

`sudo nano /etc/hostname`

to which it asks you for your password, and then opens nano with the extra privileges provided by `sudo`. There is a `sudoers` file which contains a list of users who can use `sudo`, and what privileges they get from using it.



#### **0.2.5.2. File permissions**

Linux inherits its file permissions system from Unix. You can use the command `ls -l` to display the permissions of a file or files:

`user@MY-PC:~/junk$ ls -l`\
`total 8`\
`-rw-rw-r-- 1 user user 9 Apr 25 21:28 junk1`\
`drwxrwxr-x 2 user user 4096 Apr 25 21:29 other_junk`

The first string consists of a sequence of letters, which represent the permissions on the file. The two names refer to the owner and group the file belongs to, respectively.

Let's take the file, `junk1`, as our example. The first character is the file type. This is a \`d' if the file is a directory (like `other_junk`). The next part should be read as three sets of permissions

`-rw-rw-r--`\
`( d )( u )( g )( o )`\
`( - )(rw-)(rw-)(r--)`

where the first set, `u`, refers to the permissions for the user who owns the file. The next set, `g`, refers to the permissions for the group that the file belongs to. The final set, `o`, refers to the permissions for any other user. Each set uses \`rwx' to specify the permission to (r)ead, (w)rite or e(x)ecute, or `-` if that permission is not set. Let’s take a look at the folder `other_junk`.

`drwxrwxr-x`

This is a directory, the user has read/write/execute access, users belonging to the group of the file have read/write/execute access, and everyone else has read/execute access, but not write access.



#### **0.2.5.3. Changing permissions**

If you want to change a file's permissions, you can use `chmod`, meaning "change mode". There are two ways to do this: using u/g/o and +/- r/w/x:\
\
`chmod o+x junk1 # Add execute permission to others`\
`chmod og+wx junk1 # Add execute and write permissions to other and group`\
`chmod +x junk1 # Make junk1 executable for the user`\
`chmod g-w junk1 # Remove write permissions from junk1 for group`

etc...

or with a number that represents permissions, called a bitmask. This will set all the permissions at once for you.

`user@MY-PC:~/junk$ chmod 755 junk1`\
`user@MY-PC:~/junk$ ls -l`\
`total 8`\
`-rwxr-xr-x 1 user user 9 Apr 25 21:28 junk1`\
`drwxrwxr-x 2 user user 4096 Apr 25 21:29 other_junk`

The bit mask is three digits (sometimes four digits) between the numbers 0 and 7. Each digit represents what the read/write/execute permissions would be in binary. Take a look:

`0 = 000 = ---`\
`1 = 001 = --x`\
`2 = 010 = -w-`\
`3 = 011 = -wx`\
`4 = 100 = r--`\
`5 = 101 = r-x`\
`6 = 110 = rw-`\
`7 = 111 = rwx`

So, as a few examples,

`777 = rwxrwxrwx`\
`755 = rwxr-xr-x`\
`132 = --x-wx-w-`\
`564 = r-xrw-r--`\
`000 = ---------`

etc...

So when we set our file junk1 to 755 earlier, we set it to rwxr-xr-x, which is a pretty good permission set on your average file. Realistically, you will usually always have your own user permissions set to rwx or rw-, otherwise you are just inconveniencing yourself. You can also use `chown` to change ownership of a file.

### Need more practice?

Please have a look at the below links for more UNIX tutorials.

* [http://www.ee.surrey.ac.uk/Teaching/Unix/](http://www.ee.surrey.ac.uk/Teaching/Unix/)
* [https://www.sporcle.com/games/sporcilicious/common\_linux\_commands](https://www.sporcle.com/games/sporcilicious/common\_linux\_commands)
* [https://0xax.gitbooks.io/linux-insides/?fbclid=IwAR1UOzoLvB-OKfCpLcxB0JMy-6GBkKVRZnSdgxydoW8jJLgjAX9BiKHKzf8](https://0xax.gitbooks.io/linux-insides/?fbclid=IwAR1UOzoLvB-OKfCpLcxB0JMy-6GBkKVRZnSdgxydoW8jJLgjAX9BiKHKzf8)
