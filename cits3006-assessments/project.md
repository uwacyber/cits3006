# Project 2024

In this project, you will be working as a team to perform penetration testing techniques. 
Please note, you are expected to conduct further research to learn more about various penetration testing techniques and use them in this project.

More details are as follows.

{% hint style="warning" %}
The standard UWA late penalty applies to ALL members if you defer your group deliverable/demo (i.e., -5% per day from raw marks for 7 days, then 0).
{% endhint %}

## Task 0: Team forming (Week 7)

This project is to be carried out as a team.

You are free to form your own team, but your team must meet the following requirements:

* The team's average grade from LQ1 must not exceed 75 (i.e., add all LQ marks, then divide by the number of members). If you don't want to reveal your marks, you can use multiparty encryption!
* Ensure that at least one member has VirtualBox available on an AMD platform, as the boxes that we will be building and use will be in `.ova` format (i.e., Apple Silicon support is not required. Apple Silicon users could emulate the provided box if you wish to).

The number of members should be 5 (4 or 6 may be considered - requires approval).

{% hint style="info" %}
If the team's average grade is higher than 75, and you cannot find an appropriate team, you should contact me. I will either allocate you to a different team or allow an exemption.&#x20; You are encouraged to find team members using the MS Teams.
{% endhint %}

Once the team has been formed, go to MS Teams -> Project Discussion, and there is the "CITS3006 Project Groups" tab. There is a "Groups" tab, where you enter your team details (team name, team leader (main contact) and members' student IDs). The team leader will also contact me to confirm the team formation. Once confirmed, you may start with Task 1 below.

Please note that you are required to submit an individual report, so you should also be keeping records of individual contributions so that individual assessment components can be evaluated later.

## Task 1: Configure a Vulnerable Box for Pentesting Exercise (Weeks 8-9)

Your team of renowned cybersecurity experts is conducting a security exercise for your pen testers. This is done by building a vulnerable web server (you can use any kind of theme you would like). Then the pen testers are tasked to find those vulnerabilities you have “hidden” in the vulnerable web server. The VM must have the following attributes:

* 3 network-based vulnerabilities.
* 3 types of web-based vulnerabilities (e.g., SQLi, XSS).
* 3 horizontal and 3 vertical privilege escalation vulnerabilities.
* 3 reverse engineering-related vulnerabilities.

Using the attributes above, there must be at least 3 different ways to gain root access to the vulnerable machine.

The below attributes will attract bonus marks as indicated if implemented:

* Kernel vulnerabilities (2%)
* Cryptographic vulnerabilities (2%)
* Side-channel vulnerabilities (2%)

Later in Task 2, your server will be exploited by the pen testers (i.e., other teams). To ensure you train your pen testers to the highest quality, make sure the vulnerabilities are not easily exploitable.&#x20;

### Task 1 todo:

1. Remember, when configuring the web server, the vulnerabilities are not easily exploitable.
2. By Friday 11:59pm of week 9, your team leader must submit the group report on LMS outlining the vulnerabilities implemented and how they are exploited to provide at least 3 different ways to gain root access, along with other vulnerabilities. This report will be used during the live demo as a guideline for the marker, and any new vulnerabilities not in the report will not be counted toward the grade. Also, the report must explicitly and clearly state individual contributions. This will be used to assess the individual contribution to the project.
3. The team leader must share the `.ova` file of your vulnerable web server via email to me (e.g., a link is sufficient). Acknowledgement will be made once received. With the `.ova` file, you are also to submit an instruction document for any setup required to run your web application (if any). If vulnerabilities require bypassing some security measures, you should indicate this in the instruction document (not the details of the defence, but stating that there are some security measures in place before the vulnerability can be exploited). The security measures must be able to be bypassed by the pen testers, and will not count towards the difficulty of exploiting the vulnerability itself.
4. The team leader must schedule your demo slot from the available slots provided on MS Teams -> Project Discussion -> CITS3006 Project Groups -> Task 1 Demo booking (week 10).

{% hint style="warning" %}
DON'T do everything yourself. This is not a race among the team members. If you read the rubric on individual reports, the marks are based on your ability to demonstrate penetration testing skills, which means QUALITY over QUANTITY (i.e., you don't have to get full marks in other tasks to receive full marks for your individual report).

What does "Quality" mean? In the context of this project, it means that you are able to not only demonstrate skills you have learned in the unit, but have also researched and applied more advanced skills derived from further research into the topic, with an in-depth understanding and explanation of skills and techniques demonstrated. That is, you are expected to conduct further research to learn more about various penetration testing techniques and use them in this project as appropriate.

Of course, you will need to meet all requirements to receive marks for other tasks, which means your contributions may vary (i.e., you might have to cover for other members if needed).
{% endhint %}

## Task 1 Live Demo of the Configured Vulnerable Box (Week 10)

Your team will demonstrate live the configured vulnerable box during the scheduled lab. All members are expected to attend the scheduled session, and be able to demonstrate the contributed portion of the configurations as required (however, how you perform demonstration is up to the group i.e., a single presenter could perform the demo if it seems more appropriate).

### **Task 1 live demo todo:**
1. Perform demonstration during the scheduled time.
2. Access released exercise boxes for Task 2, which will be available once all demos have completed.

{% hint style="info" %}
The live demo will be no longer than 30 mins, you should aim it to be around 20 mins + 10 mins embedded Q&A (i.e., questions asked during the demo).
{% endhint %}

## Task 2: Pentesting Exercise (Week 11)

Your team, acting as pen testers, will now have access to all other vulnerable boxes, available from MS Teams -> Project Discussion -> Files -> Boxes.

Exploit as many vulnerabilities as you can in all available exercise boxes.

### Task 2 todo:

1. By Friday 11:59pm of week 11, your team leader must submit the group report outlining the exploits conducted to exploit the exercise boxes. This report will be used during the live demo as a guideline for the marker, and any new exploits not in the report will not be counted toward the grade. You must also state individual contributions explicitly and clearly. Remember, quality over quantity.
2. You will also rate the boxes you attempt to exploit (the rating should be noted in your group report explicitly). For rating, use a scale of 1 to 10, where 1 is being very easy, and 10 being very hard. You only have to rate the ones you have attempted.
3. Your team leader should have scheduled your demo from the available slots provided on MS Teams -> Project Discussion -> CITS3006 Project Groups -> Task 2 Demo booking (week 12).


## Task 2 Live Demo (Presentation) of Exploiting Other Boxes (Week 12)

Your team will demonstrate live the exploitation of boxes you have completed in Task 2. All members are expected to attend the scheduled session, and be able to demonstrate the contributed portion of the configurations as required (however, how you perform demonstration is up to the group i.e., a single presenter could perform the demo if it seems more appropriate).

### Task 2 live demo todo:
1. Perform demonstration during the scheduled time (booking required).

{% hint style="info" %}
The live demo will be no longer than 30 mins, you should aim it to be around 20 mins + 10 mins embedded Q&A (i.e., questions asked during the demo).
{% endhint %}

<!--
## Bonus Marks: Complete the survey

You can complete the survey to receive a bonus mark of 5%. Make sure to enter your student ID correctly (on the first page).
Link: [https://docs.google.com/forms/d/e/1FAIpQLSex3sFSr3HByvuVsHGqJ8C8L54lFkZ6fDn0DzDDFAw8CmlSNw/viewform](https://docs.google.com/forms/d/e/1FAIpQLSex3sFSr3HByvuVsHGqJ8C8L54lFkZ6fDn0DzDDFAw8CmlSNw/viewform)

{% hint style="info" %}
1. You must complete the survey by Monday 9 October 5pm to receive the bonus marks.
2. The game server is not built for scalability, so if it isn't working, please try again a bit later. If it still doesn't work after a while, please let me know.
{% endhint %}
-->


## Marking Rubrics

<table>
    <thead>
        <tr>
            <th width="200">Component</th>
            <th width="100">Weight</th>
            <th width="200">N</th>
            <th width="200">P</th>
            <th width="200">CR</th>
            <th width="200">D</th>
            <th width="200">HD</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Configuring a vulnerable web server (T1)</td>
            <td>25%</td>
            <td>(1) Failed to implement the four types of vulnerability attributes.<br><br>(2) Demo failed to demonstrate the implemented vulnerabilities.<br><br>(3) Report is not aligned with the demo.</td>
            <td>(1) Implemented each of the four types of vulnerability attributes.<br><br>(2) Demo demonstrated the implemented vulnerabilities.<br><br>(3) Report aligns with the demo but is lacking details.</td>
            <td>(1) Implemented each of the four types of vulnerability attributes, with at least 8 vulnerabilities in total.<br><br>(2) Demo demonstrated the implemented vulnerabilities clearly.<br><br>(3) Report aligns with the demo with adequate details.</td>
            <td>(1) Implemented all required vulnerabilities.<br><br>(2) Demo demonstrated the implemented vulnerabilities clearly.<br><br>(3) Report aligns with the demo and is formatted well.</td>
            <td>(1) Implemented all required vulnerabilities.<br><br>(2) Demo demonstrated the implemented vulnerabilities at a professional level.<br><br>(3) Report aligns with the demo and is formatted professionally.</td>
        </tr>
        <tr>
            <td>Pen testing (T2)</td>
            <td>25%</td>
            <td>(1) Much of the vulnerabilities were not exploited in the provided exercise boxes.<br><br>(2) Demo failed to demonstrate the implemented vulnerabilities.<br><br>(3) Report is not aligned with the demo.</td>
            <td>(1) Various vulnerabilities were exploited in provided exercise boxes.<br><br>(2) Demo demonstrated the exploitation of vulnerabilities.<br><br>(3) Report aligns with the demo but is lacking details.</td>
            <td>(1) Many vulnerabilities were exploited in many of the provided exercise boxes.<br><br>(2) Demo demonstrated the exploitation of vulnerabilities clearly.<br><br>(3) Report aligns with the demo with adequate details.</td>
            <td>(1) Many vulnerabilities were exploited, with some boxes completely compromised with all vulnerabilities exposed.<br><br>(2) Demo demonstrated the exploitation of vulnerabilities clearly.<br><br>(3) Report aligns with the demo and is formatted well.</td>
            <td>(1) Many vulnerabilities were exploited, with many (if not most) boxes completely compromised with all vulnerabilities exposed.<br><br>(2) Demo demonstrated the exploitation of vulnerabilities at a professional level.<br><br>(3) Report aligns with the demo and is formatted professionally.</td>
        </tr>
        <tr>
            <td>Difficulty of compromising the configured web server</td>
            <td>25%</td>
            <td>Many teams have rated the box supplied as easy (i.e., ratings mostly 1~2).</td>
            <td>Many teams have rated the box supplied as moderately easy (i.e., ratings mostly 3~4).</td>
            <td>Many teams have rated the box supplied as moderate (i.e., ratings mostly 5~6).</td>
            <td>Many teams have rated the box supplied as moderately hard (i.e., ratings mostly 7~8).</td>
            <td>Most teams have rated the box supplied as hard (i.e., ratings mostly 9~10).</td>
        </tr>
        <tr>
            <td>Individual contributions (from T1 and T2)</td>
            <td>25%</td>
            <td>No or nearly none evidence of contributions made to the project.</td>
            <td>(1) Made some contribution to the project, demonstrating some penetration testing skills.<br><br>(2) Shows some indication of research done, exploring new penetration testing skills not covered in the class.</td>
            <td>(1) Made some key contributions to the project, demonstrating a variety of penetration testing skills.<br><br>(2) Shows a reasonable amount of research done, exploring new penetration testing skills not covered in the class.</td>
            <td>(1) Made major contributions in the project, demonstrating a variety of penetration testing skills.<br><br>(2) Shows a high level of research done, exploring new and advanced penetration testing skills not covered in the class.</td>
            <td>(1) Made major contributions in the project, demonstrating advanced penetration testing skills.<br><br>(2) Shows a comprehensive level of research done, exploring new and advanced penetration testing skills not covered in the class.</td>
        </tr>
    </tbody>
</table>
 




