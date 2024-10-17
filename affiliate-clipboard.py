"""
Script Name: affiliate-clipboard.py
Description: This script assists SD agents with bulk data entry by using regex to automatically parse affiliate request tickets. The output is organized into a sorted list.
Author: Jonah Anthony
Date: 2024-10-16
Version: 1.0.1

Dependencies:
    - This script uses only standard Python libraries (tkinter, re, and tkinter.messagebox), so no additional installations are required.

Usage:
    python affiliate-clipboard.py

"""


import tkinter as tk
from tkinter import ttk, messagebox
import re

def parse_data(data):
    fields = {
        'First Name': '',
        'Middle Name or Initial': '',
        'Last Name': '',
        'Date of Birth': '',
        'Gender': '',
        'Phone': '',
        'Email': '',
        'Street Address': '',
        'City': '',
        'State': '',
        'Postal': '',
        'Affiliate Type': '',
        'Start Date': '',
        'End Date': '',
        'Department': '',
        'Requested For': ''
    }

    # Extracting fields using regular expressions
    patterns = {
        'First Name': r'^First Name:\s*(.*)$',
        'Middle Name or Initial': r'^Middle Name or Initial:\s*(.*)$',
        'Last Name': r'^Last Name:\s*(.*)$',
        'Date of Birth': r'^Date of Birth:\s*(.*)$',
        'Gender': r'^Gender:\s*(.*)$',
        'Email': r'^Email Address:\s*(.*)$',
        'Phone': r'^Phone Number:\s*(.*)$',
        'Affiliate Type': r'^Affiliate Type:\s*(.*)$',
        'Start Date': r'^Start Date:\s*(.*)$',
        'End Date': r'^End Date:\s*(.*)$',
        'Department': r'^Department:\s*(.*)$',
        'Requested For': r'^Requested For:\s*(.*)$',
        'Street Address': r'^Street Address:\s*(.*)$',
        'City': r'^City:\s*(.*)$',
        'State': r'^State:\s*(.*)$',
        'Postal': r'^Zip Code:\s*(.*)$',
    }

    for field, pattern in patterns.items():
        match = re.search(pattern, data, re.MULTILINE)
        if match:
            fields[field] = match.group(1).strip()

    # Clean up State (remove code after '-')
    if fields['State']:
        fields['State'] = fields['State'].split(' - ')[0].strip()

    # Clean up Postal Code (remove code after '-')
    if fields['Postal']:
        fields['Postal'] = fields['Postal'].split('-')[0].strip()

    return fields

def process_input():
    data = text_input.get("1.0", tk.END)
    if not data.strip():
        messagebox.showwarning("Input Error", "Please paste the data into the text area.")
        return
    extracted_fields = parse_data(data)
    display_fields(extracted_fields)

def copy_to_clipboard(value):
    root.clipboard_clear()
    root.clipboard_append(value)
    # messagebox.showinfo("Copied", f"'{value}' has been copied to clipboard.")

def display_fields(fields):
    # Clear previous results
    for widget in result_frame.winfo_children():
        widget.destroy()

    for field, value in fields.items():
        # Skip fields that are empty, whitespace, or 'Not Specified'
        if not value.strip() or value.strip().lower() == 'not specified':
            continue

        frame = ttk.Frame(result_frame)
        frame.pack(fill='x', pady=2)

        label = ttk.Label(frame, text=f"{field}: {value}", anchor='w')
        label.pack(side='left', fill='x', expand=True)

        btn = ttk.Button(frame, text="Copy to Clipboard", command=lambda v=value: copy_to_clipboard(v))
        btn.pack(side='right')

# GUI Setup
root = tk.Tk()
root.title("Affiliate Clipboard")

# Set the style
style = ttk.Style()
style.theme_use('clam')

# Main Frame
main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill='both', expand=True)

# Title Label
title_label = ttk.Label(main_frame, text="Affiliate Clipboard", font=('Helvetica', 16, 'bold'))
title_label.pack(pady=10)

# Input Frame
input_frame = ttk.LabelFrame(main_frame, text="Input Data")
input_frame.pack(fill='both', padx=5, pady=5, expand=True)

instruction_label = ttk.Label(input_frame, text="Paste the ticket description below and click 'Process Data':")
instruction_label.pack(anchor='w', padx=5, pady=5)

text_input = tk.Text(input_frame, height=10)
text_input.pack(fill='both', padx=5, pady=5, expand=True)

process_btn = ttk.Button(input_frame, text="Process Data", command=process_input)
process_btn.pack(pady=5)

# Separator
separator = ttk.Separator(main_frame, orient='horizontal')
separator.pack(fill='x', pady=5)
    
# Result Frame
result_frame = ttk.LabelFrame(main_frame, text="Extracted Fields")
result_frame.pack(fill='both', padx=5, pady=5, expand=True)

root.mainloop()
