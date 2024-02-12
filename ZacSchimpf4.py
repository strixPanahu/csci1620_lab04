"""

    CSCI 1620 001/851
    Professor Owora
    Week 04 - Lab 04
    12/02/2024
"""
import csv
import os
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
    return [{"Email": "", "Day": "", "Date": "", "Month": "", "Year": "", "Time": ""}]

    # Todo: See Step 2-a


def output_to_csv(emails_dict):
    outbound_name = "outbound.csv"
    header = [f"Email", f"Day", f"Date", f"Month", f"Year", f"Time"]
    with open(outbound_name, 'w', newline='') as outbound_file:
        writer = csv.DictWriter(outbound_file, fieldnames=header, delimiter=',')
        writer.writeheader()

        for message in emails_dict:
            writer.writerow(message)

        outbound_file.close()


def output_to_txt(emails_dict):
    outbound_name = "output.txt"
    totals = get_message_totals(emails_dict)

    # Todo: See Step 2-b & 8-b


def get_message_totals(emails_dict):
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
