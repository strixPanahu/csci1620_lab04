"""
    CSCI 1620 001/851
    Professor Owora
    Week 04 - Lab 04
    12/02/2024

    Todo:
        Separate datetime
        Sort methods
        Add docstrings
        Optimise regex
        Unit Tests
"""

from csv import DictWriter
from datetime import datetime
from os import getcwd, linesep
from re import search
from sys import exit


def main():
    raw_input = read_txt()
    emails_dict = convert_raw_to_dict(raw_input)
    output_to_csv(emails_dict)
    output_to_txt(emails_dict)


def read_txt():
    inbound_name = "input.txt"
    try:
        with open(inbound_name) as inbound_file:
            lines = inbound_file.readlines()
        inbound_file.close()
    except FileNotFoundError:
        exit("Invalid request for file_name \"" + inbound_name + "\" at \"" + getcwd() + "\"")

    return lines


def convert_raw_to_dict(raw_input):
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
            try:
                result = search(r".*X-DSPAM-Processed: (.*)", line)
                index = result.start() + len("X-DSPAM-Processed: ") + len("Day ")
                timestamp_str = line[index:].strip()

                timestamp_dt = convert_str_to_datetime(timestamp_str)

                emails_dict.append({"Email": sender,
                                    "Day": day_format[timestamp_dt.weekday()],
                                    "Date": timestamp_dt.day,
                                    "Month": timestamp_dt.month,
                                    "Year": timestamp_dt.year})

                sender = None
            except AttributeError:
                pass

    return emails_dict


def convert_str_to_datetime(timestamp_str):
    timestamp_list = timestamp_str.split()

    months_format = (None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
    month = months_format.index(timestamp_list[0])

    day = int(timestamp_list[1])

    hour = int(timestamp_list[2][:2])
    minute = int(timestamp_list[2][3:5])
    second = int(timestamp_list[2][6:])

    year = int(timestamp_list[3])

    return datetime(year, month, day, hour, minute, second)


def output_to_csv(emails_dict):
    outbound_name = "output.csv"
    header = list(emails_dict[0].keys())

    with open(outbound_name, 'w', newline='') as outbound_file:
        writer = DictWriter(outbound_file, fieldnames=header, delimiter=',')
        writer.writeheader()
        writer.writerows(emails_dict)
        outbound_file.close()


def output_to_txt(emails_dict):
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
        outbound_file.write(f"{'Total:':<40}{'- ' + str(quantity)}")

        outbound_file.close()


def get_message_summary(emails_dict):
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
