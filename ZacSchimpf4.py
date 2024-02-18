"""
    CSCI 1620 001/851
    Professor Owora
    Week 04 - Lab 04
    12/02/2024

    https://github.com/strixPanahu/csci1620_lab04
"""

from csv import DictWriter
from datetime import datetime
from os import getcwd, linesep
from re import search
from sys import exit


def main():
    """
    Primary logic flow; cli-callable function
    :return: None
    """

    raw_input = read_txt()
    emails_dict = convert_raw_to_dict(raw_input)
    output_to_csv(emails_dict)
    output_to_txt(raw_input)


def read_txt():
    """
    Reads working directory "input.txt"
    :return: A list[] containing each newline separated string
    """

    inbound_name = "input.txt"
    try:
        with open(inbound_name) as inbound_file:
            lines = inbound_file.readlines()
        inbound_file.close()
    except FileNotFoundError:
        exit("Invalid request for file_name \"" + inbound_name + "\" at \"" + getcwd() + "\"")

    return lines


def convert_raw_to_dict(raw_input):
    """
    Clean list[] of email logs to contain only sender & timestamp
    :param raw_input A list[] of the input file's lines
    :return [{Email, Day, Date, Month, Year, Time}, {etc. }]
    """

    day_format = (None, "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
    emails_dict = []

    for line in raw_input:
        try:
            if search(r".*From (.*)", line):
                line = line.rstrip().split()
                del line[0]  # rm ["From", ]

                sender = line[0]
                del line[:2]  # rm [Email, Day, ]

                timestamp_dt = convert_str_to_datetime(line)
                emails_dict.append({"Email": sender,
                                    "Day": day_format[timestamp_dt.weekday()],
                                    "Date": timestamp_dt.day,
                                    "Month": timestamp_dt.month,
                                    "Year": timestamp_dt.year,
                                    "Time": timestamp_dt.time()})
        except AttributeError:
            pass

    return emails_dict


def convert_str_to_datetime(timestamp):
    """
    Cleans a string containing a log file's timestamp
    :param timestamp: [Mon, Date, Time, Year], e.g. ["Jan", "1"," "12:00:00", "1999"]
    :return Datetime object containing the converted timestamp
    """
    months_format = (None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

    try:
        month = months_format.index(timestamp[0])

        day = int(timestamp[1])

        time = str(timestamp[2]).split(':')
        hour = int(time[0])
        minute = int(time[1])
        second = int(time[2])

        year = int(timestamp[3])
    except ValueError:
        exit(timestamp + " does not follow log convention of \"[Jan,  1, 12:00:00, 1999]\"")

    return datetime(year, month, day, hour, minute, second)


def output_to_csv(emails_dict):
    """
    Write a List[{}, {}] to a csv file in the current working directory, named output.csv
    :param emails_dict A list containing dictionaries
    :return None
    """

    outbound_name = "output.csv"
    header = list(emails_dict[0].keys())

    with open(outbound_name, 'w', newline='') as outbound_file:
        writer = DictWriter(outbound_file, fieldnames=header, delimiter=',')
        writer.writeheader()
        writer.writerows(emails_dict)


def output_to_txt(raw_input):
    """
    Write a List[{}, {}] to a txt file in the current working directory, named output.txt
    :param raw_input: A string converted copy of the log
    :return: None
    """

    outbound_name = "output.txt"
    summary = get_log_summary(raw_input)
    total = 0

    with open(outbound_name, 'w') as outbound_file:
        # header
        outbound_file.write(f"{'Email':<40}{'- Count' + linesep}")

        # summary
        for email, quantity in summary.items():
            outbound_file.write(f"{email + ':':<40}{'- ' + str(quantity) + linesep}")
            total += quantity

        # eof
        outbound_file.write(f"{' ':->46}{linesep}")  # break = len(header)
        outbound_file.write(f"{'Total:':<40}{'- ' + str(total)}")


def get_log_summary(raw_input):
    """
    Creates a summary of a list of emails, such as totals for each address.
    :param raw_input: A string converted copy of the log
    :return: A dictionary containing how many messages each email sent
    """

    totals = {}

    for line in raw_input:
        try:
            if search(r".*From:(.*)", line):
                line = line.rstrip().split()

                if line[1] in totals:
                    new_total = totals.get(line[1]) + 1
                    totals.update({line[1]: new_total})
                else:
                    totals.update({line[1]: 1})

        except AttributeError:
            pass
            
    return totals


if __name__ == '__main__':
    main()
