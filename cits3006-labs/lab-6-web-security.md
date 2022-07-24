# Lab 6: Web Security (NOT READY)

{% hint style="danger" %}
READ: Any knowledge and techniques presented here are for your learning purposes only. It is **ABSOLUTELY ILLEGAL** to apply the learned knowledge to others without proper consent/permission, and even then, you must check and comply with any regulatory restrictions and laws.&#x20;
{% endhint %}

---

## 6.0.0 Introduction

SQL injection (SQLi) and Cross Site Scripting (XSS) are a type of **injection (AS03:2021)** vulnerability that have been listed as one of the top 10 web application security risks by OWASP ([OWASP Top 10](https://owasp.org/www-project-top-ten/)). This lab will explore these two types of vulnerabilities on vulnerable web applications and explain how to detect these vulnerabilities via source code review and black box testing.

---

## 6.1.0  SQLi

A SQLi attack injects a malicious SQL query via input data from the client to the web application. If a website does not securely sanitise user inputs being inserted into a SQL query, then an attacker can malform the query to perform additional operations that were never intended.

For this section, we will explore how SQLi vulnerabilities can occur, how to exploit the follow types of SQLi attacks and using tools such as `sqlmap` to automatically discover and exploit SQLi vulnerabilities.

- Union-based SQLi
- Error-based SQLi
- Blind-based SQLi
- Time-based SQLi

---

### 6.1.1 How SQLi vulnerabilities occur

A relational database is a collection of data that has been structured by predefined relations that are stored in tables. They are widely used for managing information for web applications and the following are the most popular relational database management systems that are currently used:

- MySQL
- SQLite
- PostgreSQL
- Amazon Aurora
- MSSQL

The Structured Query Language (SQL) is a programming language for querying or inserting data into a relational databases. Web applications that need to store persistent data would connect to the database and execute a set of SQL queries. However, if user inputs are insecurely inserted into the SQL query by the web application then an attacker can malform the query to perform additional opperations.

To demonstrate, lets explore how a SQLi vulnerability can be exploited to bypass authentication on a website.

For most websites when you login, the backend web application will query the SQL database using a query like below. In the below example, the credentials are stored in a table called `users` and `{username}` and `{password}` are replaced with the user's **username** and **password** they send respectively. If the SQL query returns a result then the backend web application would state that user has authenticated themselves.

```sql
SELECT username FROM users WHERE username = '{username}' AND password = '{password}';
```

The issue with just replacing `{username}` and `{password}` in the above query is that you can insert a `'` character that would break the query! If the attacker sends `admin'--` (`--` are comments for most DB management systems) as the username then the SQL query would only search for a username with the name `admin`! You can see how the query becomes malformed in the following SQL query and would always return a result if there is an account with the username `admin`.

```sql
SELECT username FROM users WHERE username = 'admin'--' AND password = '{password}';
```

However, if there isn't a user with the username `admin` you can still bypass the authentication by malforming the query to always return a result by inserting an `OR` conditional that will always return **true**. If the attacker changes their username payload to `admin' OR '1'='1'--` into the SQL query the DB management system would first check if the user `admin` exists **or '1'='1'** (which is always true).

```sql
SELECT username FROM users WHERE username = 'admin' OR '1'='1'--' AND password = '{password}';
```

The above query would now return all of the users stored in the `users` table and since this applications authenticates users when a result is returned from the query the attacker would be authenticated, bypassing the authentication.

---

### 6.1.2 How to prevent SQLi vulnerabilites

To prevent SQLi vulnerabilities **all user inputs need to be santised before being inserted into a SQL query** . The most effective strategy is to use **prepared statements** that decouples the SQL query from the data and **eliminates SQLi vulnerabilities**. You do this by first preparing the statement and indicating where data should be placed using the special character `?`, then you bind the actual values when the query is executed.

Continuing from the previous example, the prepared statement for authentication is shown below and when it's executed the user's `username` and `password` would be binded to the query.

```sql
SELECT username FROM users WHERE username = ? AND password = ?;
```

An example is the python code below that uses prepared statements using SQLite as the DB management system.

```python
import sqlite3

def login(username: str, password: str) -> bool:
    with sqlite3.connect('/tmp/somedatabase.sqlite') as con
        cur = con.cursor()
        cur.execute("SELECT username FROM users WHERE username = ? AND password = ?", (username, password))

        # Returns True if there is one result, False otherwise
        return len(cur.fetchall()) == 1
```

The only issue with prepared statements is that they can only be used for parameter values (eg. in `WHERE` and `VALUES` clauses) and cannot be used to santise **table names** or the `ORDER BY` clauses. To mitigate the risk of an SQLi vulnerability, web applications should implement a Web Application Firewall (WAF) that **whitelists** what the expected input should be. For an example, if user input is being inserted after an `ORDER BY` statement and assumes the input is an integer then the WAF **should only allow integers and no other characters**.

The following python code filters the user input by using prepared statement and a whitelist to make sure only integers are inserted after the `ORDER BY` statement.

```python
import sqlite3

def search_memes(meme_name: str, order_by_str: str) -> list:
    try:
        # int() would throw an exception if any non-integer characters are in order_by_str
        order_by = int(order_by_str)
    except Exception as e:
        # Return nothing since the user supplied invalid input
        return []

    with sqlite3.connect('/tmp/somedatabase.sqlite') as con
        cur = con.cursor()
        cur.execute("SELECT * FROM memes WHERE name ORDER BY {}".format(order_by), (meme_name,))

        return cur.fetchall()
```

---

### 6.1.3 Union-based SQLi Attacks

Union-based SQLi attacks exploit a SQLi vulnerability by appending the results of a malicious query after the results of the original query. This is done by injecting `UNION` statement into the SQL query then using `SELECT` to query data from other databases. It is the easiest type of SQLi vulnerability to exploit and can be used to dump all data from a SQL database quickly.

This section will explore how to detect Union-based SQLi attack vectors, the methodology of enumerating the database to find sensitive information quickly and dumping the data you need.

**Detecting a SQLi attack vector**

The easiest way to see if some input is not properly santised for a SQL query is by sending a single `'` or `"` character. If the website crashes (sends a 500 HTTP status code) then it is a strong indication that the malicious input has caused a SQL syntax error, which caused the website to crash. 

However, if the web application properly handles errors the page would not return a 500 HTTP status code, making the SQLi attack vector harder to detect. Therefore, a more effective way to detect if an input is vulnerable to SQLi is to first discover an input that always returns a result, then try injecting a SQL conditional and see if the same result returns.

For an example, a web application executes the following SQL query when you search for items on the store, where `{search}` is replaced with the user's input. The contents of the `items` table is shown below the query.

```sql
SELECT name, description, amount, price FROM items WHERE name LIKE '{search}'
```

*items table*
| name | description | amount | price |
| ---- | ----------- | ------ | ----- |
| milk crate | a milk crate stolen from coles | 20 | 10000 |
| 1L of 4 year old petrol | some petrol siphoned out of a lawn mower | 13 | 600 |
| 1g of dirt | literally dirt | 20000 | 999999 |

If you just searched `milk crate` on the store then it would only show you the results for the item named `milk crate`. However, if you searched `milk crate' AND '1'='1` and it returns with the same results then you have found the attack vector for exploiting the SQLi vulnerability. This is because the input malforms the query to still search for `milk crate` and insert a SQL `AND` conditional that always returns **true** (the malformed query is shown below). However, if the input was not vulnerable then the DB would of searched for `milk crate' AND '1'='1` and return no results since there are no items with that name.

*The malformed query*
```sql
SELECT name, description, amount, price FROM items WHERE name LIKE 'milk crate' AND '1'='1'
```

**Methodology for exploiting Union-based SQLi**

**Step 1: Finding the number of columns your payload needs to return**

Once you have discovered the vulnerable input to SQLi, the first step is to determine how many columns should be returned by the vulnerable SQL query. This is because when you use `UNION SELECT` to append additional results the number of columns needs to match the number of columns of the original query, otherwise the SQL query will cause an SQL error.

You can determine the number of columns you need by using `ORDER BY` or `GROUP BY` and incrementing the column index until an error or no result is returned.

Using the previous `items` example.

- `milk crate' ORDER BY 1--`: Returns the milk crate result
- `milk crate' ORDER BY 2--`: Returns the milk crate result
- `milk crate' ORDER BY 3--`: Returns the milk crate result
- `milk crate' ORDER BY 4--`: Returns the milk crate result
- `milk crate' ORDER BY 5--`: Returns no results. This is because there is no column with the index 5 in the `items` table and causes an SQL error. Therefore, it indicates that the original query returns 4 columns.

An alternative is using the `UNION SELECT` statement with constant values until an error does not occur.

- `milk crate' UNION SELECT 1--`: Returns no results.
- `milk crate' UNION SELECT 1,2--`: Returns no results.
- `milk crate' UNION SELECT 1,2,3--`: Returns no results.
- `milk crate' UNION SELECT 1,2,3,4--`: Returns the milk crate result and a row with the numbers 1, 2, 3 4, and 5.
- `milk crate' UNION SELECT 1,2,3,4,5--`: Returns no results.

**Step 2: Leaking Information About the Database Management System**

The next step is to discover what databases are available, the table names in those databases and the columns of those database. For this section it will be assumed that the database management system is MySQL, since the queries can be different across DB management systems. For more information about SQLi enumeration for other DB management systems check out the [PayloadAllTheThings repository](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection).

On MySQL databases, the **`information_schema`** database stores all of the metadata about databases, tables and columns stored on the MySQL server. The following SQL queries show how you can retrieve this information from the `information_schema`.

```sql
-- Dumps the names of databases
SELECT schema_name FROM information_schema.schemata;

-- Dumps the names of tables from a database called 'storedb'
SELECT table_name FROM information_schema.tables WHERE table_schema = 'storedb';

-- Dumps the columns for the table called 'users'
SELECT column_name FROM information_schema.columns WHERE table_name = 'users';
```

To execute these queries for our SQLi attack, we need craft our `UNION SELECT` to return 4 columns and also show the columns that we want to view.

```
' UNION SELECT 1,schema_name,3,4 FROM information_schema.schemata--
```

**Step 3: Dumping Information from Tables**

Once you have discovered the tables and columns you want to dump, you then just rewrite your `UNION SELECT` payload to dump those columns you want to view.

eg.
```
' UNION SELECT username,password,3,4 FROM users--
```

---

### 6.1.4 Union-based SQLi Exercise

**TODO**

---

### 6.1.5 Error-based SQLi Attacks

The only issue with Union-based SQLi is that it relies on the results of the SQL query being shown to the end user on the website to work. In a number of circumstances the results of a vulnerable SQL query are never displayed on the website and are only used by the backend web application.

Error-based SQLi attacks are an alternative to Union-based SQLi that exploits verbose error messages that are displayed on a website if a SQL error occurs. An attacker can abuse these error messages to leak out information from the database using the error messages that are shown on the website.

For MySQL servers, the **`updatexml`** is a useful functioning for causing an SQL error and leaking the result of a different query in the error message. For an example, the below payload is an example of using `updatexml` to leak a name of a database from the `information_schema.schemata` table.

```
' AND updatexml(rand(),concat(0x3a,(SELECT concat(CHAR(126),schema_name,CHAR(126)) FROM information_schema.schemata LIMIT 1,1)),null)--
```

---

### 6.1.6 Error-based SQLi Exercise

**TODO**

---

### 6.1.7 Blind-based SQLi Attacks

There are a number of scenarios where a vulnerable SQL query is executed on the backend web application and the results/errors are never directly displayed to the end user. However, if the content on the page changes depending on the results of the vulnerable SQL query then an attacker can still exfiltrate data from the SQL server.

Blind-based SQLi works by executing malicious queries that return a boolean value that impacts the response of the web application to indicate the correct value that is being queried. An example of python code with a vulnerable SQLi query that impacts content of a page is shown below.

```python
import sqlite3

def count_items(search: str) -> int:
    with sqlite3.connect('/tmp/somedatabase.sqlite') as con
        cur = con.cursor()
        cur.execute("SELECT name FROM items WHERE name LIKE '{search}'".format(search))
        return len(cur.fetchall())
```

In the above code snippet, the actual results of the query are never returned to the end user and only returns the number of rows. An attacker can use the returned the count value to indicate if they have found a true value for a malicious character.

For an example, let's say an attacker is trying to dump the password for the `admin` user stored in the `users` table on the database. The attacker will first want to figure out the length of the stored password by brute forcing the length until the count changes to indicate the correct length has been found. This can be done using the `length` SQL function then executing query as a parameter for the `length` function (shown below).

```sql
length((SELECT password FROM users WHERE username='admin' LIMIT BY 1))=1
```

The attacker can then determine if the password has a length of 1 character by sending `milk crate' AND length((SELECT password FROM users WHERE username='admin' LIMIT BY 1))=1--` (the malformed query is shown below).

```sql
SELECT name FROM items WHERE name LIKE 'milk crate' AND length((SELECT password FROM users WHERE username='admin' LIMIT BY 1))=1--'
```

If the `admin` password has a length of 1, then the application response will show a count of 1 since 1=1. If the count is 0, then it would indicate that the length of the password is not 1 and the attacker will then check if the length is equal to 2 and so on.

This methodology can also be used to exfiltrate the values of the password by brute forcing the value of a character in the password until the full password has been leaked. Instead of using the `length` function to exfiltrate the length of the password you can use the MySQL `substring` function (if the DB management system is MySQL). `substring` returns a substring of a string, for an example `substring("hack the planet", 4, 1)` would return the letter `k`. Now let's say that the actual password for the `admin` account is `carrot`. An attacker can retrieve the full value of the payload as shown below:

```
# Count is 0 since the first letter of the password is not 'a'
milk crate' AND substring((SELECT password FROM users WHERE username='admin' LIMIT BY 1), 1, 1)='a'--

# Count is 0 since the first letter of the password is not 'b'
milk crate' AND substring((SELECT password FROM users WHERE username='admin' LIMIT BY 1), 1, 1)='b'--

# Count is 1 since the first letter of the password is 'c'
milk crate' AND substring((SELECT password FROM users WHERE username='admin' LIMIT BY 1), 1, 1)='c'--

# Count is 1 since the second letter of the password is 'a'
milk crate' AND substring((SELECT password FROM users WHERE username='admin' LIMIT BY 1), 2, 1)='a'--

# Count is 0 since the third letter of the password is not 'a'
milk crate' AND substring((SELECT password FROM users WHERE username='admin' LIMIT BY 1), 3, 1)='a'--

...
```

There is one issue with this approach. For MySQL string searches for nonbinary strings (`CHAR`, `VARCHAR` and `TEXT`) use the collation of the comparison operands and are **case insensitive**! However, binary strings (`BINARY`, `VARBINARY` and `BLOB`) compare the numeric values of the bytes and the comparison is **case sensitive**. The following exercise would be constructing a Blind-based SQLi payload that is **case sensitive**.

---

### 6.1.8 Blind-based SQLi Exercise

**TODO**

*Students will not have to write the full exploit code and just have to fill in the payload for exploiting the blind-based injection*

--- 

### 6.1.9 Time-based SQLi Attacks

If the vulnerable SQL query does not have show any results or alter the response, then a time-based SQLi attack is required. Time-based is similar to Blind-based SQLi, but instead of altering the response you cause the web application to **sleep** when you find the correct value and delaying the response from the website.

In SQL you can write an **if** statement using the MySQL function `IF`. The below SQLi payload queries if the first character of the `admin` password is `a` and sleeps for 3 seconds if it is `a`.

```
' AND IF(substring((SELECT password FROM users WHERE username='admin' LIMIT BY 1), 2, 1)='a', SLEEP(3), 0)--
```

---

### 6.1.10 Time-based SQLi Exercise

**TODO**

Similar to the blind-based exercise

---

### 6.1.11 `sqlmap` Exercise

**DO NOT USE `sqlmap` ON ANY WEBSITES YOU DO NOT HAVE PERMISSION! IT IS A CYBER CRIME IF YOU DO!**

`sqlmap` is a powerful penetration testing tool that automates detecting and exploiting SQLi vulnerabilities. It supports exploiting a large variety of relational database management systems, has built-in tamper scripts for altering payloads to bypass web applicaiton filters, and can perform all of the SQLi attacks that have been mentioned during this lab plus more.

The downside of `sqlmap` is that it isn't as reliable for detecting SQLi vulnerabilities as source code review, cannot easily exploit union-based and blind-based SQLi attacks, and is **extremely aggressive** (so you will be caught immediately if use it on a website that has any monitoring implemented).

To see the help options for `sqlmap` you can type `sqlmap --help` to see the list of command options.

For this part of the lab, we will use `sqlmap` to exploit a Time-based SQLi vulnerability that has a WAF that removes all spaces from the user input. You will need to set a tamper script in order for the SQLi payloads to work, that can be listed by executing `sqlmap --list-tampers`.

**TODO**

---

## 6.2.0 XSS Attacks

**TODO**

---

### 6.2.1 JavaScript and the DOM for Hackers

**TODO**

---

### 6.2.2 Exploiting a Basic XSS Vulnerability

**TODO**

---

### 6.2.3 Exploiting XSS Using Other HTML Tags

**TODO**

---

### 6.2.3 Bypassing Content Security Policy Protections

**TODO**

---

### 6.2.4 Bypassing `self` Content Security Policy Using Polyglots

**TODO**

*Might exclude since it is tough*