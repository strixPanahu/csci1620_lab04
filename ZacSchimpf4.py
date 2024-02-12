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
    return [{"Email": "", "Day": "", "Date": "", "Month": "", "Year": "", "Time":""}]


def output_to_csv(emails_dict):
    outbound_name = "outbound.csv"
    header = [f"Email", f"Day", f"Date", f"Month", f"Year", f"Time"]
    with open(outbound_name, 'w', newline='') as outbound_file:
        writer = csv.DictWriter(outbound_file, fieldnames=header, delimiter=',')
        writer.writeheader()

        for message in emails_dict:
            writer.writerow(message)

        outbound_file.close()


if __name__ == '__main__':
    main()
