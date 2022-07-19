<<<<<<< HEAD:cits3006-labs/lab-3-malware-analysis-and-reverse-engineering.md
# Lab 3: Malware Analysis and Reverse Engineering - DearCry Ransomware
=======
# Lab 3: Reverse Engineering (NOT READY)
>>>>>>> a2d58fea9e7b0490ffbb94594b50f0117266fa7f:cits3006-labs/lab-3-reverse-engineering.md

{% hint style="danger" %}
READ: Any knowledge and techniques presented here are for your learning purposes only. It is **ABSOLUTELY ILLEGAL** to apply the learned knowledge to others without proper consent/permission, and even then, you must check and comply with any regulatory restrictions and laws.&#x20;
{% endhint %}





## TODO:

* update instructions for kali linux: capa tool, IDA,
* tools section
* check figure references

The aim of this lab is to perform deep analysis of DearCry ransomware and demonstrate some techniques of malware analysis, and especially reverse engineering of malicious sample for educational purposes. Materials in this lab adapted from [LIFARS](https://lifars.com/wp-content/uploads/2021/04/DearCry\_Ransomware.pdf).

<<<<<<< HEAD:cits3006-labs/lab-3-malware-analysis-and-reverse-engineering.md
## 3.0. Introduction
=======
### X.0. Introduction
>>>>>>> a2d58fea9e7b0490ffbb94594b50f0117266fa7f:cits3006-labs/lab-3-reverse-engineering.md

The DearCry ransomware has been used in current attacks related to the exploitation of Microsoft Exchange Servers. Unlike other ransomwares, DearCry is special in terms of its complexity. It is very simple malware, and it could be reverse engineered in couple of minutes as we demonstrate in this paper. The main objective of this document is to provide not only the analysis of DearCry ransomware, but also to provide educational tips and tricks, which could be useful in the cybersecurity community and students of computer science.

### X.1. Static Analysis

<<<<<<< HEAD:cits3006-labs/lab-3-malware-analysis-and-reverse-engineering.md
## 3.1. Static Analysis

Static analysis is usually the initial stage of malware analysis. Commonly the samples are scanned with antivirus software and IOC scanners. This phase also includes the analysis of sample metadata, embedded strings, resources, imports and exports (in case of Portable executable files, .EXE), presence of macros and auto-open or auto-close actions (in case of Office Documents). 

### 3.1.1. DearCry Sample

We will analyze the DearCry ransomware sample (often classified also as DoejoCrypt) obtained from [Malware Bazaar](https://bazaar.abuse.ch/sample/e044d9f2d0f1260c3f4a543a1e67f33fcac265be114a1b135fd575b860d2b8c6/). It is a portable executable file, and it is approximately 1.2 MB in size. This means that it is relatively large malware sample.

![](/.gitbook/assets/lab-3-assets/1.png "1")
*Figure 1: DearCry Metadata from Malware Bazaar repository*


### 3.1.2. Strings

DearCry is very simple ransomware, as we can see even by extraction of the embedded strings. We use the `strings` command (Unix), or the Sysinternals tool called strings.exe (Windows).

![](/.gitbook/assets/lab-3-assets/2.png "2")
*Figure 2: Extracted strings with ransom note template and name of the ransomware.*

There is no obfuscation, all strings are clearly visible. For example, the ransom note. The sample leaks some debug information about its origin, too. From the PDB filepath we can determine the username, used development tools and original name of the project.

![](/.gitbook/assets/lab-3-assets/3.png "3")
*Figure 3: Extracted strings with RSA public key and file extensions to be encrypted*

RSA Public key is visible here, and also the list of file extensions. DearCry ransomware will probably encrypt files with these extensions, as we will see later.

### 3.1.3. Capabilities

![](/.gitbook/assets/lab-3-assets/4.png "4")
*Figure 4: Sample overview reported by capa tool*
![](/.gitbook/assets/lab-3-assets/5.png "5")
*Figure 5: Sample capabilities - file operations; OpenSSL crypto library used.*

As a next step, we can quickly identify capabilities in the analyzed sample with the [capa tool](https://github.com/mandiant/capa). There is lot of cryptography, ciphers, hashes. And it is linked against OpenSSL cryptography library.

## 3.2. Behavioural Analysis
=======
Static analysis is usually the initial stage of malware analysis. Commonly the samples are scanned with antivirus software and IOC scanners. This phase also includes the analysis of sample metadata, embedded strings, resources, imports and exports (in case of Portable executable files, .EXE), presence of macros and auto-open or auto-close actions (in case of Office Documents).

#### X.1.1. DearCry Sample

We will analyze the DearCry ransomware sample (often classified also as DoejoCrypt) obtained from [Malware Bazaar](https://bazaar.abuse.ch/sample/e044d9f2d0f1260c3f4a543a1e67f33fcac265be114a1b135fd575b860d2b8c6/). It is a portable executable file, and it is approximately 1.2 MB in size. This means that it is relatively large malware sample.

![](../.gitbook/assets/lab-X-assets/1.png) _Figure 1: DearCry Metadata from Malware Bazaar repository_

#### X.1.2. Strings

DearCry is very simple ransomware, as we can see even by extraction of the embedded strings. We use the `strings` command (Unix), or the Sysinternals tool called strings.exe (Windows).

![](../.gitbook/assets/lab-X-assets/2.png) _Figure 2: Extracted strings with ransom note template and name of the ransomware._

There is no obfuscation, all strings are clearly visible. For example, the ransom note. The sample leaks some debug information about its origin, too. From the PDB filepath we can determine the username, used development tools and original name of the project.

![](../.gitbook/assets/lab-X-assets/3.png) _Figure 3: Extracted strings with RSA public key and file extensions to be encrypted_

RSA Public key is visible here, and also the list of file extensions. DearCry ransomware will probably encrypt files with these extensions, as we will see later.

#### X.1.3. Capabilities

![](../.gitbook/assets/lab-X-assets/4.png) _Figure 4: Sample overview reported by capa tool_ ![](../.gitbook/assets/lab-X-assets/5.png) _Figure 5: Sample capabilities - file operations; OpenSSL crypto library used._

As a next step, we can quickly identify capabilities in the analyzed sample with the [capa tool](https://github.com/mandiant/capa). There is lot of cryptography, ciphers, hashes. And it is linked against OpenSSL cryptography library.

### X.2. Behavioural Analysis
>>>>>>> a2d58fea9e7b0490ffbb94594b50f0117266fa7f:cits3006-labs/lab-3-reverse-engineering.md

During behavioral analysis, the sample is executed in sandbox. This protected environment is monitored for any activities performed by the sample, such as spawning new processes, network communication, dropping files or overwriting the existent files. By reviewing of sample’s behavior, we can often say if the sample is malicious and if yes, what kind of malware it is (e.g., ransomware).

With behavioral analysis we can also quickly collect lot of indicators of compromise (IOC) which could be used by rest of the team for effective incident response, forensic analysis, threat hunting or for monitoring and prevent threats in the customers’ infrastructure.

We will skip this step for now, because we already know that this is a DearCry ransomware sample which encrypts files. We will rather deep dive into the DearCry internals and code. We will demonstrate the process of reverse engineering the malware. However, we will later do a crosscheck of our findings with output from the sandbox, in this case, just for educational purposes.

<<<<<<< HEAD:cits3006-labs/lab-3-malware-analysis-and-reverse-engineering.md
## 3.3. Reverse Engineering

Reverse engineering is the phase in which we decompile or disassemble the machine instructions of program into more readable form. In this case, analyzed sample is a Portable Executable file produced by Microsoft Visual Studio compiler. We use IDA, Interactive Disassembler, for reverse engineering of this DearCry sample.

### 3.3.1. IDA Flirt Signatures

When IDA finished its automatic analysis, we can see disassembled program with lot of functions. By default, almost all functions are assumed to be regular (blue color in program navigation bar), without known library functions (light cyan in navigation bar). We can fix this by applying IDA's FLIRT signatures, for example, Microsoft Visual C runtime signatures identified more than 600 functions. But there is still very small portion of all functions.

![](/.gitbook/assets/lab-3-assets/6.png "6")
*Figure 6:Applied IDA FLIRT Signatures and Program overview in Navigation Bar*

Recall that capa tool identified that this sample is linked against OpenSSL, and there are many strings containing the OpenSSL term. It seems that DearCry is statically linked against OpenSSL version 1.1.

![](/.gitbook/assets/lab-3-assets/7.png "7")
*Figure 7: GitHub repository with FLIRT signatures for OpenSSL*

We can obtain the signatures for OpenSSL from the [community driven collection of IDA FLIRT signature files](https://github.com/Maktm/FLIRTDB/tree/master/openssl/windows). They are available for couple of common libraries. We will download and use two which fits most to our case - OpenSSL 1.1 compiled by Visual Studio 2008, as we saw in the extracted strings. With these two FLIRT signatures applied, we have identified more than 3000 of library functions. Now it seems that only small portion of DearCry functions is custom, developed by authors of the ransomware.

![](/.gitbook/assets/lab-3-assets/8.png "8")
*Figure 8: Applied IDA FLIRT Signatures for OpenSSL library*

When we examine imports, they are mostly related to cryptography, because of dependencies of embedded OpenSSL library. On the other hand, there is only one exported symbol called start, which is the usual entry point of portable executable files.

### 3.3.2. Ransomware Logic

&#x20;**3.3.2.1. Entry Point**

Now we are ready to begin with analysis of disassembled code. Our objective is to understand what the analyzed program does and how it works.

![](/.gitbook/assets/lab-3-assets/9.png "9")
*Figure 9: Start routine of the analyzed sample*

This is more less standard start routine, with checking for “MZ” (5A4Dh) and “PE” executable headers, then parsing command line arguments and set environment variables. After that, near to the end of start routine, there is a call with three arguments. This is the main function of the programs developed in C or C++.

![](/.gitbook/assets/lab-3-assets/10.png "10")
*Figure 10: End of the start routine with call to main function*

&#x20;**3.3.2.2. Main Function**

The main function is simple. It starts service control dispatcher, which connects the main service thread to the service control manager. The service related to this ransomware is called “msupdate”.

![](/.gitbook/assets/lab-3-assets/11.png "11")
*Figure 11: Disassembled main function of the ransomware sample*

&#x20;**3.3.2.3. ServiceMain Function**
=======
### X.3. Reverse Engineering

Reverse engineering is the phase in which we decompile or disassemble the machine instructions of program into more readable form. In this case, analyzed sample is a Portable Executable file produced by Microsoft Visual Studio compiler. We use IDA, Interactive Disassembler, for reverse engineering of this DearCry sample.

#### X.3.1. IDA Flirt Signatures

When IDA finished its automatic analysis, we can see disassembled program with lot of functions. By default, almost all functions are assumed to be regular (blue color in program navigation bar), without known library functions (light cyan in navigation bar). We can fix this by applying IDA's FLIRT signatures, for example, Microsoft Visual C runtime signatures identified more than 600 functions. But there is still very small portion of all functions.

![](../.gitbook/assets/lab-X-assets/6.png) _Figure 6:Applied IDA FLIRT Signatures and Program overview in Navigation Bar_

Recall that capa tool identified that this sample is linked against OpenSSL, and there are many strings containing the OpenSSL term. It seems that DearCry is statically linked against OpenSSL version 1.1.

![](../.gitbook/assets/lab-X-assets/7.png) _Figure 7: GitHub repository with FLIRT signatures for OpenSSL_

We can obtain the signatures for OpenSSL from the [community driven collection of IDA FLIRT signature files](https://github.com/Maktm/FLIRTDB/tree/master/openssl/windows). They are available for couple of common libraries. We will download and use two which fits most to our case - OpenSSL 1.1 compiled by Visual Studio 2008, as we saw in the extracted strings. With these two FLIRT signatures applied, we have identified more than 3000 of library functions. Now it seems that only small portion of DearCry functions is custom, developed by authors of the ransomware.

![](../.gitbook/assets/lab-X-assets/8.png) _Figure 8: Applied IDA FLIRT Signatures for OpenSSL library_

When we examine imports, they are mostly related to cryptography, because of dependencies of embedded OpenSSL library. On the other hand, there is only one exported symbol called start, which is the usual entry point of portable executable files.

#### X.3.2. Ransomware Logic

**X.3.2.1. Entry Point**

Now we are ready to begin with analysis of disassembled code. Our objective is to understand what the analyzed program does and how it works.

![](../.gitbook/assets/lab-X-assets/9.png) _Figure 9: Start routine of the analyzed sample_

This is more less standard start routine, with checking for “MZ” (5A4Dh) and “PE” executable headers, then parsing command line arguments and set environment variables. After that, near to the end of start routine, there is a call with three arguments. This is the main function of the programs developed in C or C++.

![](../.gitbook/assets/lab-X-assets/10.png) _Figure 10: End of the start routine with call to main function_

**X.3.2.2. Main Function**

The main function is simple. It starts service control dispatcher, which connects the main service thread to the service control manager. The service related to this ransomware is called “msupdate”.

![](../.gitbook/assets/lab-X-assets/11.png) _Figure 11: Disassembled main function of the ransomware sample_

**X.3.2.3. ServiceMain Function**
>>>>>>> a2d58fea9e7b0490ffbb94594b50f0117266fa7f:cits3006-labs/lab-3-reverse-engineering.md

ServiceMain function is also simple, it registers service control handler for this “msupdate” service. And then, it calls yet unknown function sub\_401D10.

<<<<<<< HEAD:cits3006-labs/lab-3-malware-analysis-and-reverse-engineering.md
![](/.gitbook/assets/lab-3-assets/12.png "12")
*Figure 12: Disassembled ServiceMain function*
=======
![](../.gitbook/assets/lab-X-assets/12.png) _Figure 12: Disassembled ServiceMain function_
>>>>>>> a2d58fea9e7b0490ffbb94594b50f0117266fa7f:cits3006-labs/lab-3-reverse-engineering.md

Back in main function, we can see that the same sub\_401D10 function is called right after service dispatcher. It seems that this function is responsible for all malicious things performed by this ransomware sample. Hence, it will probably do some ransomware stuff.

<<<<<<< HEAD:cits3006-labs/lab-3-malware-analysis-and-reverse-engineering.md
&#x20;**3.3.2.4. “Do-ransomware-stuff” Function**

![](/.gitbook/assets/lab-3-assets/13.png "13")
*Figure 13: "do_ransomware_stuff" function called from main and ServiceMain functions*
=======
**X.3.2.4. “Do-ransomware-stuff” Function**

![](../.gitbook/assets/lab-X-assets/13.png) _Figure 13: "do\_ransomware\_stuff" function called from main and ServiceMain functions_
>>>>>>> a2d58fea9e7b0490ffbb94594b50f0117266fa7f:cits3006-labs/lab-3-reverse-engineering.md

Let's look into the ransomware stuff function. First interesting function is sub\_401000. It references the embedded RSA Public Key and creates string with hexadecimal representation of some values in loop. It actually creates a formatted string with hash value of RSA key.

<<<<<<< HEAD:cits3006-labs/lab-3-malware-analysis-and-reverse-engineering.md
![](/.gitbook/assets/lab-3-assets/14.png "14")
*Figure 14: Obtaining the hexadecimal representation of the embedded RSA Public Key’s hash value*

Next, the ransomware stuff function then prepares a formatted ransom note message and get list of logical drives of the infected machine. It searches for drives with letters between C and Z included, and all types of drive except CD-ROM drive.

![](/.gitbook/assets/lab-3-assets/15.png "15")
*Figure 15: Preparation of formatted ransom note message in the ransomware stuff function*
![](/.gitbook/assets/lab-3-assets/16.png "16")
*Figure 16: Enumeration of logical drives of the infected machine*
=======
![](../.gitbook/assets/lab-X-assets/14.png) _Figure 14: Obtaining the hexadecimal representation of the embedded RSA Public Key’s hash value_

Next, the ransomware stuff function then prepares a formatted ransom note message and get list of logical drives of the infected machine. It searches for drives with letters between C and Z included, and all types of drive except CD-ROM drive.

![](../.gitbook/assets/lab-X-assets/15.png) _Figure 15: Preparation of formatted ransom note message in the ransomware stuff function_ ![](../.gitbook/assets/lab-X-assets/16.png) _Figure 16: Enumeration of logical drives of the infected machine_
>>>>>>> a2d58fea9e7b0490ffbb94594b50f0117266fa7f:cits3006-labs/lab-3-reverse-engineering.md

After that, it passes each drive to the function sub\_401640, which will probably be responsible for encrypting drive or folder.

<<<<<<< HEAD:cits3006-labs/lab-3-malware-analysis-and-reverse-engineering.md
![](/.gitbook/assets/lab-3-assets/17.png "17")
*Figure 17: Hypothesis: function sub_401640 is responsible for encrypting drive or folder and creation of readme.txt file with ransom note*

Then, this ransomware stuff function drops readme.txt file with the ransom note. And finally, the last call will delete service “msupdate”, created by this ransomware previously.

![](/.gitbook/assets/lab-3-assets/18.png "18")
*Figure 18: Removing msupdate service created by this ransomware previously*

### 3.3.3. File Encryption

Until now, we used top-down methodology for analysis of ransomware logic. Now we can change our approach and use bottom-up methodology instead of top-down.

&#x20;**3.3.3.1. Encrypt-file Function**

During static analysis we saw string “.CRYPT”, which looks like an extension of the files encrypted by this ransomware. Let's examine the cross references to this string in IDA. It is referenced only in one function; thus this function should be responsible for writing an encrypted file to disk.

![](/.gitbook/assets/lab-3-assets/19.png "19")
*Figure 19: Cross references to ".CRYPT" and creating the encrypted file by ransomware*
=======
![](../.gitbook/assets/lab-X-assets/17.png) _Figure 17: Hypothesis: function sub\_401640 is responsible for encrypting drive or folder and creation of readme.txt file with ransom note_

Then, this ransomware stuff function drops readme.txt file with the ransom note. And finally, the last call will delete service “msupdate”, created by this ransomware previously.

![](../.gitbook/assets/lab-X-assets/18.png) _Figure 18: Removing msupdate service created by this ransomware previously_

#### X.3.3. File Encryption

Until now, we used top-down methodology for analysis of ransomware logic. Now we can change our approach and use bottom-up methodology instead of top-down.

**X.3.3.1. Encrypt-file Function**

During static analysis we saw string “.CRYPT”, which looks like an extension of the files encrypted by this ransomware. Let's examine the cross references to this string in IDA. It is referenced only in one function; thus this function should be responsible for writing an encrypted file to disk.

![](../.gitbook/assets/lab-X-assets/19.png) _Figure 19: Cross references to ".CRYPT" and creating the encrypted file by ransomware_
>>>>>>> a2d58fea9e7b0490ffbb94594b50f0117266fa7f:cits3006-labs/lab-3-reverse-engineering.md

Let us examine this encrypt file function. Mode “rb+” means that the original file is opened for updating. To be more specific, for reading and writing. The “wb” mode means, that file with “.CRYPT” extension is opened for writing. Hence, DearCry uses copy encryption instead of in-place encryption of files, and it is similar to the infamous WannaCry ransomware.

In Figure 20 we can see that DearCry ransomware prepends a “DEARCRY!” marker to the beginning of the encrypted .CRYPT files.

<<<<<<< HEAD:cits3006-labs/lab-3-malware-analysis-and-reverse-engineering.md
![](/.gitbook/assets/lab-3-assets/20.png "20")
*Figure 20: DEARCRY! file marker and encryption of AES key with RSA*

&#x20;**3.3.3.2. OpenSSL Encryption: RSA+AES**
=======
![](../.gitbook/assets/lab-X-assets/20.png) _Figure 20: DEARCRY! file marker and encryption of AES key with RSA_

**X.3.3.2. OpenSSL Encryption: RSA+AES**
>>>>>>> a2d58fea9e7b0490ffbb94594b50f0117266fa7f:cits3006-labs/lab-3-reverse-engineering.md

The ransomware uses OpenSSL for generating a random key for symmetric encryption (AES-256-CBC) and encrypts this symmetric key with RSA using the embedded public key (2048-bit length):

```
-----BEGIN RSA PUBLIC KEY-----
MIIBCAKCAQEA5+mVBe75OvCzCW4oZHl7vqPwV2O4kgzgfp9odcL9LZc8Gy2+NJPD
wrHbttKI3z4Yt3G04lX7bEp1RZjxUYfzX8qvaPC2EBduOjSN1WMSbJJrINs1Izkq
XRrggJhSbp881Jr6NmpE6pns0Vfv//Hk1idHhxsXg6QKtfXlzAnRbgA1WepSDJq5
H08WGFBZrgUVM0zBYI3JJH3b9jIRMVQMJUQ57w3jZpOnpFXSZoUy1YD7Y3Cu+n/Q
6cEft6t29/FQgacXmeA2ajb7ssSbSntBpTpoyGc/kKoaihYPrHtNRhkMcZQayy5a
XTgYtEjhzJAC+esXiTYqklWMXJS1EmUpoQIBAw==
-----END RSA PUBLIC KEY-----
```

<<<<<<< HEAD:cits3006-labs/lab-3-malware-analysis-and-reverse-engineering.md
![](/.gitbook/assets/lab-3-assets/21.png "21")
*Figure 21:Prime factors of 2048-bit RSA public key*

Then, the encrypted symmetric key is written as a part of header of the encrypted file after the “DEARCRY!” marker.

![](/.gitbook/assets/lab-3-assets/22.png "22")
*Figure 22: OpenSSL functions for encryption. sub_402F00 has not been identified by used FLIRT signature*
=======
![](../.gitbook/assets/lab-X-assets/21.png) _Figure 21:Prime factors of 2048-bit RSA public key_

Then, the encrypted symmetric key is written as a part of header of the encrypted file after the “DEARCRY!” marker.

![](../.gitbook/assets/lab-X-assets/22.png) _Figure 22: OpenSSL functions for encryption. sub\_402F00 has not been identified by used FLIRT signature_
>>>>>>> a2d58fea9e7b0490ffbb94594b50f0117266fa7f:cits3006-labs/lab-3-reverse-engineering.md

In the Figure 22 there are calls to OpenSSL’s functions \_EVP\_CIPHER\_CTX\_new, \_EVP\_CipherInit\_ex and sub\_402F00, which has not been recognized by used FLIRT signature, but this function should return the type of encryption to be used. Let’s identify this function manually by quick review of OpenSSL library and its usage in DearCry ransomware. From the OpenSSL documentation, the first two parameters of EVP\_CipherInit\_ex are context (EVP\_CIPHER\_CTX) and type (EVP\_CIPHER):

```
int EVP_CipherInit_ex(EVP_CIPHER_CTX *ctx, const EVP_CIPHER *type,
ENGINE *impl, const unsigned char *key, const unsigned char *iv, int enc);
```

Example usage of this function could look like this:

```
EVP_CIPHER_CTX ctx;
EVP_CIPHER_CTX_init(&ctx);
EVP_CipherInit_ex(&ctx, EVP_rc4(), NULL, &key, &iv, 1);
```

The EVP\_rc4() function is the example of candidate for the unknown function sub\_402F00. Actually, functions such as EVP\_rc4() are very simple, they contain only couple of instructions which return the object describing the type of the cipher, as is depicted in the Figure 23.

<<<<<<< HEAD:cits3006-labs/lab-3-malware-analysis-and-reverse-engineering.md
![](/.gitbook/assets/lab-3-assets/23.png "23")
*Figure 23: EVP_Cipher type object returned by sub_402F00*

The first value (427) is something called NID, numbered value of ASN.1 object identifier. The NID value of 427 is associated with the AES-256-CBC cipher.

![](/.gitbook/assets/lab-3-assets/24.png "24")
*Figure 24: Identification of AES-256-CBC encryption used by DearCry ransomware*

### 3.3.4. Put it all together
=======
![](../.gitbook/assets/lab-X-assets/23.png) _Figure 23: EVP\_Cipher type object returned by sub\_402F00_

The first value (427) is something called NID, numbered value of ASN.1 object identifier. The NID value of 427 is associated with the AES-256-CBC cipher.

![](../.gitbook/assets/lab-X-assets/24.png) _Figure 24: Identification of AES-256-CBC encryption used by DearCry ransomware_

#### X.3.4. Put it all together
>>>>>>> a2d58fea9e7b0490ffbb94594b50f0117266fa7f:cits3006-labs/lab-3-reverse-engineering.md

So, what have we analyzed? It seems that the chain between start or main function and encrypt\_file function is almost completely analyzed, except one function, sub\_4015D0; see Figure 25.

<<<<<<< HEAD:cits3006-labs/lab-3-malware-analysis-and-reverse-engineering.md
![](/.gitbook/assets/lab-3-assets/25.png "25")
*Figure 25: Function graph with already analyzed functions*

&#x20;**3.3.4.1. Check-marker Function**
=======
![](../.gitbook/assets/lab-X-assets/25.png) _Figure 25: Function graph with already analyzed functions_

**X.3.4.1. Check-marker Function**
>>>>>>> a2d58fea9e7b0490ffbb94594b50f0117266fa7f:cits3006-labs/lab-3-reverse-engineering.md

Let’s focus on function sub\_4015D0. This time, a file is opened in read mode, and handle to this file is passed to another function, sub\_4010C0. It reads first 8 bytes and compare them with the string DearCry. After that, it performs additional checks. Therefore, it checks header and marker and verifies if file is already encrypted by the ransomware. After these checks by check\_marker function (originally sub\_4010C0), the actual encrypt file function is executed depending on the results of checks.

<<<<<<< HEAD:cits3006-labs/lab-3-malware-analysis-and-reverse-engineering.md
![](/.gitbook/assets/lab-3-assets/26.png "26")
*Figure 26: Checking the “DEARCRY!” file marker in sub_4010C0, followed by encrypt_file in sub_4015D0*

So, we just analyzed another two functions, for checking files and “DEARCRY!” markers before encryption itself. But we also see now, that the encrypt drive/folder function calls itself recursively, and it seems that it will be rather function for encrypting folders instead of drives only.

![](/.gitbook/assets/lab-3-assets/27.png "27")
*Figure 27: Function graph related to the files encryption and recursive function encrypt_drive/folder*

&#x20;**3.3.4.2. Encrypt-folder Function**
=======
![](../.gitbook/assets/lab-X-assets/26.png) _Figure 26: Checking the “DEARCRY!” file marker in sub\_4010C0, followed by encrypt\_file in sub\_4015D0_

So, we just analyzed another two functions, for checking files and “DEARCRY!” markers before encryption itself. But we also see now, that the encrypt drive/folder function calls itself recursively, and it seems that it will be rather function for encrypting folders instead of drives only.

![](../.gitbook/assets/lab-X-assets/27.png) _Figure 27: Function graph related to the files encryption and recursive function encrypt\_drive/folder_

**X.3.4.2. Encrypt-folder Function**
>>>>>>> a2d58fea9e7b0490ffbb94594b50f0117266fa7f:cits3006-labs/lab-3-reverse-engineering.md

Let's dive into the encrypt\_folder function. It uses Find first file and find next file API calls for searching files in current directory. For files with extension from the aforementioned list of extensions, it calls already analyzed encryption function.

<<<<<<< HEAD:cits3006-labs/lab-3-malware-analysis-and-reverse-engineering.md
![](/.gitbook/assets/lab-3-assets/28.png "28")
*Figure 28: Encrypt_folder function uses Win32 API calls FindFirstFileA and FindNextFileA*

![](/.gitbook/assets/lab-3-assets/29.png "29")
*Figure 29: Checking of file extensions to encrypt*

&#x20;**3.3.4.3. ReportServiceStatus Function**
=======
![](../.gitbook/assets/lab-X-assets/28.png) _Figure 28: Encrypt\_folder function uses Win32 API calls FindFirstFileA and FindNextFileA_

![](../.gitbook/assets/lab-X-assets/29.png) _Figure 29: Checking of file extensions to encrypt_

**X.3.4.3. ReportServiceStatus Function**
>>>>>>> a2d58fea9e7b0490ffbb94594b50f0117266fa7f:cits3006-labs/lab-3-reverse-engineering.md

Now there is only one not yet analyzed function, sub\_401C10. Quick look into it reveals that it is kind of report service status for indicating the service state.

<<<<<<< HEAD:cits3006-labs/lab-3-malware-analysis-and-reverse-engineering.md
![](/.gitbook/assets/lab-3-assets/30.png "30")
*Figure 30: Last custom function - ReportServiceStatus*

Now we have analyzed every regular function written by authors of the ransomware and we have rather good understanding what this ransomware does and how it works.

![](/.gitbook/assets/lab-3-assets/31.png "31")
*Figure 31: Function graph of analyzed functions reveals the program logic, too*

### 3.3.5. Cross-check with behavioural analysis

We can cross-check our results with the results from the behavioral analysis previously performed in sandbox. For example, the encrypted files with the CRYPT extension and DearCry marker in its beginning are clearly visible in the results.

![](/.gitbook/assets/lab-3-assets/32.png "32")
*Figure 32: File with .CRYPT extension and "DEARCRY!" file marker*

Also, file readme.txt contains the formatted ransom note message including the contact emails and hash of the RSA key.

![](/.gitbook/assets/lab-3-assets/33.png "33")
*Figure 33: Formatted ransom note with emails and hash of the RSA key*

## 3.4. Conclusion
=======
![](../.gitbook/assets/lab-X-assets/30.png) _Figure 30: Last custom function - ReportServiceStatus_

Now we have analyzed every regular function written by authors of the ransomware and we have rather good understanding what this ransomware does and how it works.

![](../.gitbook/assets/lab-X-assets/31.png) _Figure 31: Function graph of analyzed functions reveals the program logic, too_

#### X.3.5. Cross-check with behavioural analysis

We can cross-check our results with the results from the behavioral analysis previously performed in sandbox. For example, the encrypted files with the CRYPT extension and DearCry marker in its beginning are clearly visible in the results.

![](../.gitbook/assets/lab-X-assets/32.png) _Figure 32: File with .CRYPT extension and "DEARCRY!" file marker_

Also, file readme.txt contains the formatted ransom note message including the contact emails and hash of the RSA key.

![](../.gitbook/assets/lab-X-assets/33.png) _Figure 33: Formatted ransom note with emails and hash of the RSA key_

### X.4. Conclusion
>>>>>>> a2d58fea9e7b0490ffbb94594b50f0117266fa7f:cits3006-labs/lab-3-reverse-engineering.md

We introduced several principles of malware analysis and demonstrated them during the analysis of DearCry ransomware sample, which has been used in connection with the recent attacks on vulnerable Microsoft Exchange servers.

During this analysis, we spent most of the time with reverse engineering, including top-down and bottomup methodologies for analysis of unknown programs. As a result, we provided overview of DearCry ransomware’s logic and in-depth analysis of files encryption. We also covered all of the functions written by authors of this ransomware.

Last, but not least, this lab equips somebody interested in, and wanting to do their own analyze of DearCry ransomware. Analyzed samples are available on the Malware Bazaar website and this lab can be used as a walkthrough for educational purposes.

<<<<<<< HEAD:cits3006-labs/lab-3-malware-analysis-and-reverse-engineering.md
## 3.5. Appendix

### 3.5.1. Sample Information
=======
### X.5. Appendix
>>>>>>> a2d58fea9e7b0490ffbb94594b50f0117266fa7f:cits3006-labs/lab-3-reverse-engineering.md

#### X.5.1. Sample Information

|             |                                                                                             |
| ----------- | ------------------------------------------------------------------------------------------- |
| File Name   | e044d9f2d0f1260c3f4a543a1e67f33fcac265be114a1b135fd575b860d2b8c6.bin                        |
| File Size   | 1,322,496 bytes                                                                             |
| Mime Type   | application/x-dosexec                                                                       |
| File Type   | PE32 executable (console) Intel 80386, for MS Windows                                       |
| MD5 hash    | cdda3913408c4c46a6c575421485fa5b                                                            |
| SHA1 hash   | 56eec7392297e7301159094d7e461a696fe5b90f                                                    |
| SHA256 hash | e044d9f2d0f1260c3f4a543a1e67f33fcac265be114a1b135fd575b860d2b8c6                            |
| SSDeep hash | 24576:C5Nv2SkWFP/529IC8u2bAs0NIzkQS+KpPbEasBY2iKDl1fpxkLVZgMCS+: oB70s9yjE62iIl1fpxkLVZgMC3 |
| Imphash     | f8b8e20e844ccd50a8eb73c2fca3626d                                                            |

<<<<<<< HEAD:cits3006-labs/lab-3-malware-analysis-and-reverse-engineering.md
### 3.5.2. List of File Extensions
=======
#### X.5.2. List of File Extensions
>>>>>>> a2d58fea9e7b0490ffbb94594b50f0117266fa7f:cits3006-labs/lab-3-reverse-engineering.md

DearCry ransomware encrypts the files with the following extensions:

```
.TIF .TIFF .PDF .XLS .XLSX .XLTM .PS .PPS .PPT .PPTX .DOC .DOCX .LOG .MSG
.RTF .TEX .TXT .CAD .WPS .EML .INI .CSS .HTM .HTML .XHTML .JS .JSP .PHP
.KEYCHAIN .PEM .SQL .APK .APP .BAT .CGI .ASPX .CER .CFM .C .CPP .GO
.CONFIG.CSV .DAT .ISO .PST .PGD .7Z .RAR .ZIP .ZIPX .TAR .PDB .BIN .DB
.MDB .MDF .BAK .LOG .EDB .STM .DBF .ORA
```

<<<<<<< HEAD:cits3006-labs/lab-3-malware-analysis-and-reverse-engineering.md
### 3.5.3. RSA Public Key
=======
#### X.5.3. RSA Public Key

>>>>>>> a2d58fea9e7b0490ffbb94594b50f0117266fa7f:cits3006-labs/lab-3-reverse-engineering.md
```
-----BEGIN RSA PUBLIC KEY-----
MIIBCAKCAQEA5+mVBe75OvCzCW4oZHl7vqPwV2O4kgzgfp9odcL9LZc8Gy2+NJPD
wrHbttKI3z4Yt3G04lX7bEp1RZjxUYfzX8qvaPC2EBduOjSN1WMSbJJrINs1Izkq
XRrggJhSbp881Jr6NmpE6pns0Vfv//Hk1idHhxsXg6QKtfXlzAnRbgA1WepSDJq5
H08WGFBZrgUVM0zBYI3JJH3b9jIRMVQMJUQ57w3jZpOnpFXSZoUy1YD7Y3Cu+n/Q
6cEft6t29/FQgacXmeA2ajb7ssSbSntBpTpoyGc/kKoaihYPrHtNRhkMcZQayy5a
XTgYtEjhzJAC+esXiTYqklWMXJS1EmUpoQIBAw==
-----END RSA PUBLIC KEY-----
```
<<<<<<< HEAD:cits3006-labs/lab-3-malware-analysis-and-reverse-engineering.md
### 3.5.4. Ransomnote
=======

#### X.5.4. Ransomnote
>>>>>>> a2d58fea9e7b0490ffbb94594b50f0117266fa7f:cits3006-labs/lab-3-reverse-engineering.md

```
Your file has been encrypted!
                                    If you want to decrypt, please contact us.
                                    konedieyp@airmail.cc or uenwonken@memail.com
                                    And please send me the following hash!
                                    d37fc1eabc6783a418d23a8d2ba5db5a
```
