#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 Copyright © 2025 stajl <stajl@outlook.com>
"""

import requests 
import json
import subprocess
import argparse 
import os

CONFIG_PATH = "/usr/local/bin/config.json"

try:
    with open(CONFIG_PATH, "r") as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    print(f"Error: {CONFIG_PATH} not found. Exiting.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {CONFIG_PATH}. Exiting.")
    exit(1)

API_KEY = config.get("APIKEY")
API_URL = "https://api.mxtoolbox.com/api/v1/Lookup/blacklist/"
ARRAY_IP = config.get("ARRAY_IP")
MAIL_TO = config.get("MAIL_TO")
MAIL_FROM = config.get("MAIL_FROM")
MAIL_SUBJECT = config.get("MAIL_SUBJECT", "MXTOOLBOX IP Blacklist Report")

if not all([API_KEY, ARRAY_IP]):
    print("Error: Missing required configuration in config.json. Exiting.")
    exit(1)

parser = argparse.ArgumentParser(description="Check IP blacklists and send reports.")
parser.add_argument(
    "--report", action="store_true", help="Send email report if IPs are listed."
)
args = parser.parse_args()

print(f"API Key: {API_KEY[:4]}********\n")

listed_ips = {}

for ip in ARRAY_IP:
    print(f"Checking IP: {ip}")
    full_url = f"{API_URL}?argument={ip}"

    try:
        response = requests.get(full_url, headers={"Authorization": API_KEY})
        response.raise_for_status()

        data = response.json()

        if data and "Failed" in data and data["Failed"]:
            listed_ips[ip] = data["Failed"]

    except requests.exceptions.RequestException as e:
        print(f"Error: API request failed: {e}")
    except json.JSONDecodeError:
        print("Error: Invalid JSON response from API.")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")

if listed_ips:
    message_text = "\nMXTOOLBOX IP Blacklist Report:\n\n"
    for ip, failures in listed_ips.items():
        message_text += f"IP: {ip}\n"
        message_text += f"https://mxtoolbox.com/SuperTool.aspx?action=blacklist%3a{ip}&run=toolpage#\n"
        message_text += f"Total Blacklists: {len(failures)}\n"
        if failures:
            first_listed = failures[0]
            message_text += "First Listed[0]:\n"
            message_text += json.dumps({
                "Name": first_listed["Name"],
                "BlacklistReasonDescription": first_listed.get("BlacklistReasonDescription", "Listed")
            }, indent=2) + "\n\n"

    if args.report:
        if not all([MAIL_TO, MAIL_FROM]):
            print("Error: MAIL_TO or MAIL_FROM not defined in config.json. Cannot send email.")
        else:   
            try:
                headers = f"Subject: {MAIL_SUBJECT}\nTo: {MAIL_TO}\nFrom: {MAIL_FROM}\n\n"

                process = subprocess.Popen(
                    ["sendmail", "-t"],
                    stdin=subprocess.PIPE,
                    encoding="utf-8",
                )
                process.communicate(headers + message_text)
                print("\nEmail sent successfully via sendmail.")
            except FileNotFoundError:
                print(
                    "Error: sendmail command not found. Please ensure it is installed and in your PATH."
                )
            except Exception as e:
                print(f"Error sending email: {e}")
    else:
        print(message_text)
else:
    print("\nNo IPs listed on any blacklists.")
