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
    output_to_txt(emails_dict)


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
    sender = None

    for line in raw_input:

        if sender is None:  # seek sender
            try:
                result = search(r".*From: (.*)", line)
                index = result.start() + len("From: ")
                sender = line[index:].strip()
            except AttributeError:
                pass

        else:  # seek time
            try:  # verify the timestamp has not been skipped
                test = search(r".*From: (.*)", line)
                if test is not None:
                    exit(sender + " does not have a succeeding timestamp;" +
                                  " log convention is as follows " +
                                  "\"X-DSPAM-Processed: Sun Jan  1 12:00:00 1999\"")

            except AttributeError:
                pass

            try:  # else check for conventional attribute
                result = search(r".*X-DSPAM-Processed: (.*)", line)
                index = result.start() + len("X-DSPAM-Processed: ") + len("Day ")
                timestamp_str = line[index:].strip()

                timestamp_dt = convert_str_to_datetime(timestamp_str)

                emails_dict.append({"Email": sender,
                                    "Day": day_format[timestamp_dt.weekday()],
                                    "Date": timestamp_dt.day,
                                    "Month": timestamp_dt.month,
                                    "Year": timestamp_dt.year,
                                    "Time": timestamp_dt.time()})

                sender = None
            except AttributeError:
                pass

    return emails_dict


def convert_str_to_datetime(timestamp_str):
    """
    Cleans a string containing a log file's timestamp
    :param timestamp_str: An unformatted timestamp; e.g. e.g. Sat Jan  5 09:14:16 2008
    :return Datetime object containing the converted timestamp
    """

    months_format = (None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
    timestamp_list = timestamp_str.split()

    try:
        month = months_format.index(timestamp_list[0])

        day = int(timestamp_list[1])

        time = str(timestamp_list[2])
        time = time.split(':')
        hour = int(time[0])
        minute = int(time[1])
        second = int(time[2])

        year = int(timestamp_list[3])
    except ValueError:
        exit(timestamp_str + " does not follow log convention of \"Sun Jan  1 12:00:00 1999\"")

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
        outbound_file.close()


def output_to_txt(emails_dict):
    """
    Write a List[{}, {}] to a txt file in the current working directory, named output.txt
    :param emails_dict: A list containing dictionaries
    :return: None
    """

    outbound_name = "output.txt"
    summary = get_message_summary(emails_dict)
    total = 0

    with open(outbound_name, 'w', newline='') as outbound_file:
        # header
        outbound_file.write(f"{'Email':<40}{'- Count' + linesep}")

        # summary
        for email, quantity in summary.items():
            outbound_file.write(f"{email + ':':<40}{'- ' + str(quantity) + linesep}")
            total += quantity

        # eof
        outbound_file.write(f"{' ':->46}{linesep}")  # break = len(header)
        outbound_file.write(f"{'Total:':<40}{'- ' + str(total)}")

        outbound_file.close()


def get_message_summary(emails_dict):
    """
    Creates a summary of a list of emails, such as totals for each address.
    :param emails_dict: A list containing dictionaries
    :return: A dictionary containing how many messages each email sent
    """

    totals = {}

    for message in emails_dict:
        current_email = message.get("Email")

        if current_email in totals:
            current_total = totals.get(message.get("Email")) + 1
            totals.update({current_email: current_total})
        else:
            totals.update({current_email: 1})
            
    return totals


if __name__ == '__main__':
    main()
