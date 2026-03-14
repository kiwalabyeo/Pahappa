import csv
import json

# File names
input_file = "contacts.csv"
output_file = "output_groupName.txt"
json_output_file = "dashboard_data.json"

# Tracking variables -> here we shall start / initialize our variables to count
total_processed = 0
valid_unique_contacts = 0
messages_sent = 0
duplicates_ignored = 0
invalid_numbers_ignored = 0
missing_names = 0

seen_numbers = set() 
sent_messages = []

with open(input_file, "r", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        total_processed += 1

        name = row["Name"].strip().lower()
        phone = row["Phone"].strip().lower()

        # Check missing name
        if name == "":
            missing_names += 1
            continue

        # Validate phone number
        if not (phone.isdigit() and len(phone) == 12 and phone.startswith("256")):
            invalid_numbers_ignored += 1
            continue

        # Check duplicates
        if phone in seen_numbers:
            duplicates_ignored += 1
            continue

        seen_numbers.add(phone)
        valid_unique_contacts += 1

        
        message = f"Sending to {phone}: Hello {name}, you are welcome to the Pahappa Programming Challenge Sprint"

        sent_messages.append({
            "name": name,
            "phone": phone,
            "message": message
        })

        messages_sent += 1


# Summary dictionary
summary = {
    "total_processed": total_processed,
    "valid_unique_contacts": valid_unique_contacts,
    "messages_sent": messages_sent,
    "duplicates_ignored": duplicates_ignored,
    "invalid_numbers_ignored": invalid_numbers_ignored,
    "missing_names": missing_names
}


# writing the summary 
with open(output_file, "w", encoding="utf-8") as outfile:

    for msg in sent_messages:
        outfile.write(msg["message"] + "\n")

    outfile.write("\n----- Summary -----\n")
    outfile.write(f"Total processed: {summary['total_processed']}\n")
    outfile.write(f"Valid unique contacts: {summary['valid_unique_contacts']}\n")
    outfile.write(f"Messages sent: {summary['messages_sent']}\n")
    outfile.write(f"Duplicates ignored: {summary['duplicates_ignored']}\n")
    outfile.write(f"Invalid numbers ignored: {summary['invalid_numbers_ignored']}\n")
    outfile.write(f"Missing names: {summary['missing_names']}\n")


# preparing our json data for the web page
dashboard_data = {
    "summary": summary,
    "messages": sent_messages,
    "team": {
        "team_name": "Your Team Name",
        "members": [
            "Ahamada Shamuran",
            "Kiwalabye Oscar",
            "Joseph Sempebwa",
            "Nicolas Ojambo"
        ]
    }
}

# we write a summury of our successes in here
with open(json_output_file, "w", encoding="utf-8") as jsonfile:
    json.dump(dashboard_data, jsonfile, indent=4)

print("Processing complete.")
print("Text output written to:", output_file)
print("Dashboard JSON written to:", json_output_file)