# Project (NOT READY)

In this project, you will be working as a team to perform penetration testing techniques. Details are as follows.

{% hint style="warning" %}
The standard UWA late penalty applies to ALL members if you defer your deliverable/demo (i.e., -5% per day from raw marks for 7 days, then 0).
{% endhint %}

## Task 0: Team forming (Week 8)

This project is to be carried out as a team.

You are free to form your own team, but your team must meet the following requirements:

* The team's average grade from LQ1 and LQ2 must not exceed 73 (i.e., add all LQ marks, divide it by 2 (i.e., there are 2 LQs), then divide by the number of members).
* Ensure that at least one member has VirtualBox available on an AMD platform, as the provided boxes will be in `.ova` format (i.e., Apple Silicon support is not required).

The number of members should be 5 (4 or 6 may be considered - requires approval).

{% hint style="info" %}
If the team's average grade is higher than 73, and you cannot find an appropriate team, you should contact me. I will either allocate you to a different team or allow an exemption.&#x20;
{% endhint %}

Once the team has been formed, go to MS Teams -> Project Discussion, and there is the "CITS3006 Project Group Allocations" tab. Open the tab and enter your team's details (team name, team leader (main contact) and members' student IDs).

Please note that you are required to submit an individual report, so you should also be keeping records of individual contributions so that individual assessment components can be evaluated later.

## Task 1: Configure a Vulnerable Box for Pentesting Exercise (Week 9)

Your team, of renowned cybersecurity experts, is conducting a security exercise for your pen testers. This is done by building a vulnerable web server (you can use any kind of theme you would like). Then the pen testers are tasked to find those vulnerabilities you have “hidden” in the vulnerable web server. The VM must have the following attributes:

* 3 network-based vulnerabilities.
* 3 types of web-based vulnerabilities (e.g., SQLi, XSS).
* 3 horizontal and 3 vertical privilege escalation vulnerabilities.
* 3 reverse engineering-related vulnerabilities.

Using the attributes above, there must be at least 3 different ways to gain root access to the vulnerable machine.

The below attributes will attract bonus marks as indicated if implemented:

* Kernel vulnerabilities (2%)
* Cryptographic vulnerabilities (2%)
* Side-channel vulnerabilities (2%)

Later in Task 3, your server will be exploited by the pen testers (i.e., other teams). To ensure you train your pen testers to the highest quality, make sure the vulnerabilities are not easily exploitable.&#x20;

### Task 1 todo:

1. Remember, when configuring the web server, the vulnerabilities are not easily exploitable.
2. By Friday 5 pm of week 9, your team must submit the report outlining the vulnerabilities implemented and how they are exploited to provide at least 3 different ways to gain root access. This report will be used during the live demo (Taks 2) as a guideline for the marker, and any new vulnerabilities not in the report will not be counted toward the grade.

{% hint style="warning" %}
DON'T do everything yourself. This is not a race among the team members. If you read the rubric on individual reports, the marks are based on your ability to demonstrate penetration testing skills, which means QUALITY over QUANTITY (i.e., you don't have to get full marks in other tasks to receive full marks for your individual report).

What does "Quality" mean? In the context of this project, it means that you are able to not only demonstrate skills you have learned in the unit, but have also researched and applied more advanced skills derived from further research into the topic. That is, you are expected to conduct further research to learn more about various penetration testing techniques and use them in this project.

Of course, you will need to meet all requirements to receive marks for other tasks, which means your contributions may vary (i.e., you might have to cover for other members if needed).
{% endhint %}

## Task 2: Live Demo of the Configured Vulnerable Box (Week 10)

Your team will demonstrate live the configured vulnerable box during the scheduled lab. All members are expected to attend the scheduled session, and be able to demonstrate the contributed portion of the configurations.

### **Task 2 todo:**

1. Your team (via the team leader) must schedule your demo from the available slots provided on MS Teams -> Project Discussion -> Files -> Demo Scheduling.

{% hint style="info" %}
The live demo will be no longer than 30 mins.
{% endhint %}

## Task 3: Pentesting Exercise (Week 11)

Your team, acting as pen testers, will now have access to all other vulnerable boxes, available from MS Teams -> Project Discussion -> Files -> Boxes.

Exploit as many vulnerabilities as you can in all available exercise boxes.

### Task 3 todo:

1. By Friday 5 pm of week 11, your team must submit the report outlining the exploits conducted to exploit the exercise boxes. This report will be used during the live demo (Taks 4) as a guideline for the marker, and any new exploits not in the report will not be counted toward the grade.
2. In addition, you must also submit your individual report. This should outline your contribution to the group project clearly and concisely. Remember, quality over quantity.
3. You will also rate the boxes you attempt to exploit (the rating should be noted in your group report explicitly).

## Task 4: Live Demo (Presentation) of Exploiting Other Boxes (Week 12)

Your team will demonstrate live the exploitation of boxes you have completed in Task 3. All members are expected to attend the scheduled session, and be able to demonstrate the contributed portion of the configurations.

### Task 4 todo:

1. Your team (via the team leader) must schedule your demo from the available slots provided on MS Teams -> Project Discussion -> Files -> Demo Scheduling.

{% hint style="info" %}
The live demo will be no longer than 30 mins.
{% endhint %}

## Marking Rubrics



<table><thead><tr><th width="179">Component</th><th width="97">Weight</th><th width="166">N</th><th width="162">P</th><th width="201">CR</th><th width="198">D</th><th width="206">HD</th><th></th></tr></thead><tbody><tr><td>Configuring a vulnerable web server (T1, T2)</td><td>30%</td><td>(1) Failed to implement the four types of vulnerability attributes.<br><br>(2) Demo failed to demonstrate the implemented vulnerabilities.<br><br>(3) Report is not aligned with the demo.</td><td>(1) Implemented each of the four types of vulnerability attributes.<br><br>(2) Demo demonstrated the implemented vulnerabilities.<br><br>(3) Report aligns with the demo but is lacking details.</td><td>(1) Implemented each of the four types of vulnerability attributes, with at least 8 vulnerabilities in total.<br><br>(2) Demo demonstrated the implemented vulnerabilities clearly.<br><br>(3) Report aligns with the demo with adequate details.</td><td>(1) Implemented all required vulnerabilities.<br><br>(2) Demo demonstrated the implemented vulnerabilities clearly.<br><br>(3) Report aligns with the demo and is formatted well.</td><td>(1) Implemented all required vulnerabilities.<br><br>(2) Demo demonstrated the implemented vulnerabilities at a professional level.<br><br>(3) Report aligns with the demo and is formatted professionally.</td><td></td></tr><tr><td>Difficulty of compromising the configured web server (T3)</td><td>10%</td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Pen testing (T3, T4)</td><td>30%</td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Individual report (T3)</td><td>30%</td><td>No or nearly none evidence of contributions made to the project.</td><td>Made some contribution to the project, demonstrating some penetration testing skills.</td><td>Made some key contributions to the project, demonstrating a variety of penetration testing skills.</td><td>Made major contributions in the project, demonstrating a variety of penetration testing skills.</td><td>Made major contributions in the project, demonstrating advanced penetration testing skills.</td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr></tbody></table>





