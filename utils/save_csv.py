

import csv

def write_to_csv(filename, name, phone, address_line1, address_line2, amount):
    """
    Writes customer information to a CSV file.

    Args:
        filename (str): The name of the CSV file.
        name (str): Customer's name.
        phone (str): Customer's phone number.
        address_line1 (str): First line of the address.
        address_line2 (str): Second line of the address.
        amount (float or int): The amount.
    """
    try:
        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Check if the file is empty and write the header if needed
            if csvfile.tell() == 0:
                writer.writerow(['Name', 'Phone', 'Address Line 1', 'Address Line 2', 'Amount'])

            writer.writerow([name, phone, address_line1, address_line2, amount])
        print(f"Data written to {filename} successfully.")
    except Exception as e:
        print(f"An error occurred while writing to CSV: {e}")

# Example usage:
# write_to_csv('customer_data.csv', 'John Doe', '123-456-7890', '123 Main St', 'Apt 4B', 150.50)
# write_to_csv('customer_data.csv', 'Jane Smith', '987-654-3210', '456 Oak Ave', '', 75)