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