"""
    CSCI 1620 001/851
    Professor Owora
    Week 04 - Lab 04
    12/02/2024
"""

import csv
import datetime
import os
import re
import sys

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
        sys.exit("Invalid request for file_name \"" + inbound_name + "\" at \"" + os.getcwd() + "\"")

    return lines


def convert_raw_to_dict(raw_input):
    emails_dict = []
    sender = None

    for line in raw_input:

        if sender is None:  # seek sender
            try:
                result = re.search(r".*From: (.*)", line)
                index = result.start() + len("From: ")
                sender = line[index:].strip()
            except AttributeError:
                pass

        else:  # seek time
            try:
                result = re.search(r".*X-DSPAM-Processed: (.*)", line)
                index = result.start() + len("X-DSPAM-Processed: ") + len("Day ")
                timestamp_str = line[index:].strip()

                timestamp_dt = convert_str_to_datetime(timestamp_str)

                emails_dict.append({"Email": sender, "Timestamp": timestamp_dt})

                sender = None
            except AttributeError:
                pass

    return emails_dict


def convert_str_to_datetime(timestamp_str):
    timestamp_list = timestamp_str.split()

    months_format = [None, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month = int(months_format.index(timestamp_list[0]))

    day = int(timestamp_list[1])

    hour = int(timestamp_list[2][:2])
    minute = int(timestamp_list[2][3:5])
    second = int(timestamp_list[2][6:])

    year = int(timestamp_list[3])

    return datetime.datetime(year, month, day, hour, minute, second)


def output_to_csv(emails_dict):
    outbound_name = "output.csv"
    header = [f"Email", f"Timestamp"]
    with open(outbound_name, 'w', newline='') as outbound_file:
        writer = csv.DictWriter(outbound_file, fieldnames=header, delimiter=',')
        writer.writeheader()

        for message in emails_dict:
            writer.writerow(message)

        outbound_file.close()


def output_to_txt(emails_dict):
    outbound_name = "output.txt"
    total = 0

    summary = get_message_summary(emails_dict)

    with open(outbound_name, 'w', newline='') as outbound_file:
        # header
        outbound_file.write(f"{"Email":<40}{"- Count\n"}")

        # summary
        for email, quantity in summary.items():
            outbound_file.write(f"{email + ":":<40}{"- " + str(quantity) + '\n'}")
            total += quantity

        # eof
        outbound_file.write(f"{'\n':->47}")  # break = len(header)
        outbound_file.write(f"{"Total:":<40}{"- " + str(quantity)}")

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
