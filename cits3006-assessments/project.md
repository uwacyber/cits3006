# Project

In this project, you will be working in a group as cybersecurity experts who develop cybersecurity practical exercises for pen testers.  
Please note, you are expected to conduct further research to learn more about various penetration testing techniques and use them in this project.

More details are as follows.

{% hint style="warning" %}
**Using AI — you must be able to demonstrate your own understanding.** You are permitted to use AI tools in this project, but you remain responsible for understanding everything your group submits. Marks for the take-home components (Tasks 1 and 2) are awarded only for work that can be **explained and reproduced on request** — including during the live demo and Q&A (Task 3), where questions may be directed to any individual member. Any challenge, exploit, or finding that the responsible member(s) cannot explain or reproduce when asked will not count towards the marks, regardless of what the report states.
{% endhint %}

{% hint style="warning" %}
The standard UWA late penalty applies to ALL members if you defer your group deliverable/demo (i.e., -5% per day from raw marks for 7 days, then 0).
{% endhint %}

## Task 0: Group forming (Week 3)

This project is to be carried out as a group.

You are free to form your own group, but your group must meet the following requirements:

* Ensure that the group has access to both AMD and ARM architecture computers/laptops, as challenges may be architecture-specific.

The number of members should be 5 (4 or 6 may be considered for late groups, requires approval).


Once the group has been formed, go to MS Teams -> Project Discussion, and there is the "CITS3006 Project Groups" tab. There is a "Groups" tab, where you enter your group details (group name, group leader (main contact) and members' student IDs). The group leader will also contact me to confirm the group formation. Once confirmed, you may start with Task 1 below.

Please note that the project contains an individual part, so you should keep clear records of your individual contributions so that the individual assessment components can be evaluated later. If the individual contributions are not clear, you may not receive marks for the individual component.

Your contribution to the group is also assessed through peer evaluation: each member submits a contribution weight for the other members of their group. This weight is used as an indicator, not an automatic multiplier. If your weight is below 1, the coordinator will review your actual contribution — from your activity/commit records, the group report's contribution statement, and how you demonstrate and answer questions on your work during the live demos — before deciding whether and how it affects your marks on the group components. The benefit of the doubt is given. However, if you have no demonstrable contribution to the project, you may be awarded no marks — including for the group components — even if you are assigned to a group.

{% hint style="info" %}

## Task 1: Create CTF Challenges (Weeks 4-10)

Your group of renowned cybersecurity experts is developing security exercises for CTF events. This is done by building a vulnerable web/app/logs/containers/etc. (you can use any kind of theme you would like, so long as it's easily accessible to others (i.e., other students)). Then the CTF participants are tasked to find flags by exploiting the vulnerabilities you have “hidden” in the exercise you created. The following requirements are to be met with your CTF challenges:

* 3 network-based vulnerabilities.
* 3 types of web-based vulnerabilities (e.g., SQLi, XSS).
* 3 horizontal and 3 vertical privilege escalation vulnerabilities.
* 3 reverse engineering-related vulnerabilities.

For the privilege escalation vulnerabilities, there must be at least 3 different ways to gain root access in the vulnerable machine. You may combine other vulnerabilities to complete this task. 

In addition to above, you must create two advanced CTF challenges from the below requirements:

* Kernel vulnerabilities
* Cryptographic vulnerabilities (no classical ciphers accepted)
* Side-channel vulnerabilities (excluding time-based SQLi) 
* Windows-based vulnerabilities
* AI-related vulnerabilities (e.g., prompt injection, model poisoning, etc.)

The total number of challenges you need to create is not set, which means you can individually present each vulnerability, or combine them to create a more complex challenge. However, you must ensure that the vulnerabilities are not easily exploitable, as this will be used to assess the difficulty of your CTF challenges (please refer to the marking rubric below for more details).

There will be bonus marks for "fun" components of your CTF challenges, which will be based on the votes from other groups. Please note that any defense mechanisms you implement will NOT count towards your grade. There is a mark for difficulty of your CTF challenges, but this is based on the quality of vulnerabilities themselves, not the defense mechanisms in place.

Later in Task 2, your challenges will be completed by the pen testers (i.e., other groups). To ensure you train your pen testers to the highest quality, make sure the vulnerabilities are not easily exploitable.&#x20;

Although individual members may lead different challenges, every member is expected to keep a good overview of **all** the challenges the group submits — what vulnerabilities they contain and how they are exploited — not only the ones they personally built. During the live demo, any member may be asked to explain or walk through any of the group's challenges.


### Task 1 todo:

1. By Wednesday 11:59pm of week 10, your group leader must submit the group report on LMS outlining the CTF challenges and their details, including the sample solution. It is a good idea to include an exploit map in your report. This report will be used during the live demo as a guideline for the marker, and any new vulnerabilities not in the report will not be counted toward the grade. Also, the report must explicitly and clearly state individual contributions (you can structure your report as you like, but it should be clear and concise). This will be used to assess the individual contribution to the project. Remember, unclear contributions may result in no marks for the individual component.
2. The group leader must share the CTF challenge files in appropriate format via email to me (e.g., a link is sufficient). You are also to submit an instruction document (PDF) for any setup required to run your challenges (if any). Remember, no security implementations should be used to increase the difficulty of the vulnerability, unless it is part of how the vulnerability is exploited (e.g., omitting error messages from SQL database for blind-based SQLi).
3. The group leader must schedule your demo slot from the available slots provided on MS Teams -> Project Discussion -> CITS3006 Project Groups -> Project Demo booking (week 12). Both the implementation and the CTF solutions must be demonstrated.

{% hint style="warning" %}
DON'T do everything yourself. This is not a race among the group members. If you read the rubric on individual reports, the marks are based on your ability to demonstrate penetration testing skills, which means QUALITY over QUANTITY (i.e., you don't have to get full marks in other tasks to receive full marks for your individual report).

What does "Quality" mean? In the context of this project, it means that you are able to not only demonstrate skills you have learned in the unit, but have also researched and applied more advanced skills derived from further research into the topic, with an in-depth understanding and explanation of skills and techniques demonstrated. That is, you are expected to conduct further research to learn more about various penetration testing techniques and use them in this project as appropriate.

Of course, you will need to meet all requirements to receive marks for other tasks, which means your contributions may vary (i.e., you might have to cover for other members if needed).
{% endhint %}



## Task 2: Solve CTF Challenges (Week 11)

Your group, acting as pen testers, will now have access to all other CTF Challenges (access details TBC). Exploit as many vulnerabilities as you can in all available CTF challenges as a group. The CTF challenges will be available until Friday 11.59pm of week 11. However, 2 different rounds will be considered for marking: (1) Live in-person during the lecture CTF challenge, and (2) anytime before the deadline. Your submitted flags in (1) and (2) will have separate scores for your project mark.

### Task 2 todo:

1. Attend the Lecture with your group to solve CTF challenges live. 
2. Complete the remaining CTF challenges before the deadline (Friday 11.59pm of week 11). You are expected to submit all flags found in the CTF portal (TBC) before the deadline. 
3. You are also expected to submit a report on your findings, including the flags found, the vulnerabilities exploited, and the techniques used to exploit them. The report should also include any challenges faced and how they were overcome. Even if you did not find the flag, you should still report about that experience, as that will also contribute in demonstrating your penetration testing skills. Remember to clearly outline the individual contributions in your report. Finally, indicate the most fun challenge you found and why you think it was fun. This will be used to assess the "fun" component of your CTF challenges.
4. Ensure that your group leader has scheduled your group's demo from the available slots provided on MS Teams -> Project Discussion -> CITS3006 Project Groups -> Project Demo booking (week 12). Both the implementation and the CTF solutions must be demonstrated.


## Task 3: Live Demo (Week 12)

Your group will demonstrate live the development of your CTF challenges and the completion of CTF challenges. All members are expected to attend the scheduled session, and be able to demonstrate the contributed portion of the configurations as required. You won't have to demo all challenges created and/or completed, but be expected to demo any of the ones you presented in your report.

### Task 3 todo:
1. Perform demonstration during the scheduled time (booking required).

{% hint style="info" %}
The live demo will be an hour, you should think about how the demo should be structured to ensure that all members have a chance to demonstrate their contributions, as well as highlighting key vulnerabilities and techniques used in the CTF challenges. You should also be prepared to answer questions from the marker about your contributions, the vulnerabilities you created, and the techniques you used to exploit them.
{% endhint %}


## Bonus Marks: Complete the survey

You can complete the survey to receive a bonus mark of 5%. Make sure to enter your student ID correctly (on the first page).
Link: TBC 
<!-- [https://docs.google.com/forms/d/e/1FAIpQLSex3sFSr3HByvuVsHGqJ8C8L54lFkZ6fDn0DzDDFAw8CmlSNw/viewform](https://docs.google.com/forms/d/e/1FAIpQLSex3sFSr3HByvuVsHGqJ8C8L54lFkZ6fDn0DzDDFAw8CmlSNw/viewform) -->

Please note, you must complete the survey by (insert date here) to receive the bonus marks.


## Bonus Marks: Most fun challenge

Other groups vote for the most "fun" CTF challenge in their Task 2 report (see Task 2 todo). The group whose challenge receives the most votes will receive a bonus of 5%, and the runner-up group will receive 3%.



## Marking Rubrics
***
### 25%: Creating CTF Challenges (T1)

| Grade | Criteria |
| --- | --- |
| **N** | Required categories missing or below the required count; fewer than 2 working root paths, or challenges do not run as documented; vulnerabilities trivial or solvable by automated tools alone; report, sample solutions, and setup instructions missing or unusable. |
| **P** | Each of the four required categories implemented; at least 2 working root paths and at least one advanced challenge attempted; vulnerabilities function but are mostly straightforward to exploit; report, sample solutions, and setup instructions provided but lacking detail. |
| **CR** | All four categories at the required counts, plus both advanced challenges; at least 3 distinct working root paths, some combining multiple vulnerabilities; vulnerabilities require moderate effort and are not solvable by automated tools alone; report includes an exploit map with adequate sample solutions and setup docs, and all challenges are reproducible. |
| **D** | All required and both advanced challenges implemented, with variety and a coherent theme; multiple non-trivial root paths requiring chained exploitation; vulnerabilities are challenging and reflect research beyond the unit material; report, sample solutions, and setup instructions are clear, complete, and well formatted. |
| **HD** | All required and advanced challenges implemented to a professional standard with original, creative design; numerous well-designed root paths requiring sophisticated chaining; vulnerabilities are difficult, realistic, and use advanced, researched techniques that resist trivial or automated exploitation; documentation is professional and complete — a marker could reproduce every challenge from it. |

**Note on difficulty:** "Difficulty" means well-designed, solvable challenges that resist easy or automated exploitation. A challenge that cannot be solved because it is broken, unreachable, or undocumented does **not** count as difficult and will score low on this criterion.
***
### 10%: Solving CTF Challenges Live (T2-1)

| Grade | Criteria |
| --- | --- |
| **N** | Few or no flags captured during the live session; little evidence of a working approach under time pressure. |
| **P** | Some flags captured, mostly from easier challenges; a limited range of challenges attempted. |
| **CR** | A reasonable number of flags captured across several challenges; more than one vulnerability class covered. |
| **D** | Many flags captured, including some difficult challenges; worked effectively across a range of vulnerability classes under time pressure. |
| **HD** | Most available flags captured, including the hardest challenges; strong, efficient skills demonstrated across many vulnerability classes under time pressure. |
***
### 15%: Solving all CTF Challenges (T2-2)

| Grade | Criteria |
| --- | --- |
| **N** | Few flags captured across the available challenges before the deadline; report missing or does not describe the techniques used. |
| **P** | Flags captured in some challenges; report describes the vulnerabilities exploited but lacks technical detail and reflection. |
| **CR** | Flags captured across many challenges and several vulnerability classes; report clearly documents the techniques and tools used, with adequate detail. |
| **D** | Many flags captured, including difficult challenges, with some challenge sets fully solved; report is detailed and documents techniques, tools, and reflection on unsolved challenges. |
| **HD** | Most or all flags captured across the available challenges, including the most difficult; report is professional and thorough — advanced techniques, clear reasoning, and insightful reflection on both solved and unsolved challenges. |
***
### 30%: Live Demo (T3)

| Grade | Criteria |
| --- | --- |
| **N** | Demo did not clearly demonstrate the created or solved challenges; poorly structured, with one or more members not presenting; Q&A answers poor and lacking technical detail. |
| **P** | Demo demonstrated some created and/or solved challenges; reasonably structured, with most members presenting their contributions; Q&A answers reasonable with some technical detail. |
| **CR** | Demo clearly demonstrated both created and solved challenges; well structured and within time, with all members presenting their contributions; Q&A answers good with technical detail. |
| **D** | Demo clearly and effectively demonstrated created and solved challenges with good technical depth; well organised and paced, with all members demonstrating their contributions clearly; Q&A answers excellent with high technical detail. |
| **HD** | Demo demonstrated created and solved challenges at a professional level with high technical depth; professionally organised and paced, with every member demonstrating substantial contributions seamlessly; Q&A answers excellent, showing deep understanding and knowledge. |
***
### 20%: Individual contributions (T1, T2, T3)

| Grade | Criteria |
| --- | --- |
| **N** | No or nearly no evidence of contribution (report and/or peer evaluation indicate minimal involvement); no indication of independent research beyond the class material; unable to demonstrate or answer questions on any contributed work. |
| **P** | Some contribution across the tasks, demonstrating some penetration testing skills; some independent research beyond the class material; demonstrates and answers questions on their contribution at a reasonable level. |
| **CR** | Some key contributions, demonstrating a variety of penetration testing skills; a reasonable amount of independent research beyond the class material; demonstrates and answers questions on their contribution well, with technical detail. |
| **D** | Major contributions, demonstrating a variety of penetration testing skills; a high level of independent research into new and advanced techniques; demonstrates and answers questions on their contribution excellently, with high technical detail. |
| **HD** | Major contributions, demonstrating advanced penetration testing skills; a comprehensive level of independent research into new and advanced techniques; demonstrates and answers questions on their contribution excellently, with deep understanding. |
***
