import os
import glob
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import random
import textwrap
import string
import random
import re

import random
from datetime import date
from essential_generators import DocumentGenerator

g = DocumentGenerator()

def generate_sentence():
    sentence = g.gen_sentence(min_words=2, max_words=10)
    return sentence

def generate_account_name():
    sentence = g.gen_sentence(min_words=2, max_words=4)
    sentence = sentence.replace(" ", " and ", random.randint(0, sentence.count(" ")))
    sentence = sentence.replace(" ", " & ", random.randint(0, sentence.count(" ")))
    return sentence

def generate_curr_tick():
    letters = string.ascii_uppercase
    return "".join(random.choices(letters, k=3))

def generate_random_iban():
    # define the possible characters for each part of the IBAN number
    country_code_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    check_digits_chars = "0123456789"
    basic_bank_account_number_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    # generate random characters for each part of the IBAN number
    country_code = "".join([random.choice(country_code_chars) for _ in range(2)])
    check_digits = "".join([random.choice(check_digits_chars) for _ in range(2)])
    basic_bank_account_number = "".join([random.choice(basic_bank_account_number_chars) for _ in range(16)])

    # return the random IBAN number as a string
    return f"{country_code}{check_digits}{basic_bank_account_number}"

def generate_random_swift_code():
    # define the possible characters for each part of the SWIFT code
    bank_code_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    country_code_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    location_code_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    branch_code_chars = "0123456789"

    # generate random characters for each part of the SWIFT code
    bank_code = "".join([random.choice(bank_code_chars) for _ in range(4)])
    country_code = "".join([random.choice(country_code_chars) for _ in range(2)])
    location_code = "".join([random.choice(location_code_chars) for _ in range(2)])
    branch_code = "".join([random.choice(branch_code_chars) for _ in range(3)])

    # return the random SWIFT code as a string
    return f"{bank_code}{country_code}{location_code}{branch_code}"

def generate_random_date():
    # generate a random date or return "ASAP" 20% of the time
    if random.random() < 0.2:
        return "ASAP"
    else:
        year = random.randint(1900, 2100)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        d = date(year, month, day)

    # generate a random format for the date string
    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m-%d-%Y",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%B %d, %Y",
        "%A, %B %d %Y",
        "%B %d, %Y",
        "%A, %B %d %Y",
        "%A, %B %d %Y",
        "%B %d, %Y",
        "%B %d %Y",
    ]
    format = random.choice(formats)

    # return the date as a string in the chosen format
    return d.strftime(format)

def generate_currency_value():
    # generate a random numerical value
    value = random.uniform(1, 100000)

    # generate a random currency symbol
    currency_symbol = random.choice(list(string.ascii_letters.split()))

    # generate a random position for the currency symbol
    position = random.choice(["before", "after", "split"])

    # add the currency symbol and split the value as needed
    if position == "before" or position == "after":
        # round the value to 2 decimal places
        value = round(value, 2)
        # add the currency symbol before or after the value
        if position == "before":
            value = f"{currency_symbol}{value}"
        elif position == "after":
            value = f"{value}{currency_symbol}"
    elif position == "split":
        # generate a random split character
        split_char = random.choice([",", "."])

        # split the value by the split character
        value = re.sub(r"(\d)(?=(\d{3})+$)", r"\1" + split_char, f"{value:,.2f}")

    # return the formatted value
    return value

def generate_ticker():
    # generate a random length for the string
    length = random.randint(1, 3)

    # generate a random string of the desired length
    string = "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(5)])

    # split the string into chunks of 5 or 7 characters and join them with underscores
    return "_".join(["".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(5)]) for i in range(length)])

def blur_region(image, label):
    # crop the image to the desired region
    cropped_image = image.crop((label.x, label.y, label.x1, label.y1))

    # apply the blur filter to the cropped image
    blurred_image = cropped_image.filter(ImageFilter.BLUR)
    blurred_image = blurred_image.filter(ImageFilter.BLUR)
    # paste the blurred image back onto the original image
    image.paste(blurred_image, (label.x, label.y, label.x1, label.y1))

def add_text(image, label, text):
    # crop the image to the desired region
    cropped_image = image.crop((label.x, label.y, label.x1, label.y1))

    # create a Draw object to draw on the blurred image
    draw = ImageDraw.Draw(cropped_image)

    # generate some random text
    text_width, text_height = draw.multiline_textsize(text)

    while text_width > cropped_image.width or text_height > cropped_image.height:
        text = text[:-1]
        if text == "":
            break
        text_width, text_height = draw.multiline_textsize(text)

    # generate a random x and y coordinate within the blurred region
    x = random.randint(0, cropped_image.width - text_width)
    y = random.randint(0, cropped_image.height - text_height)

    # draw the text at the random position
    alignments = ["left", "center", "right"]
    align = random.choice(alignments)
    draw.multiline_text((x, y), text, fill=(0,0,0), align=align)

    # paste the blurred image back onto the original image
    image.paste(cropped_image, (label.x, label.y, label.x1, label.y1))

def blur_region_with_text(image, label):
    # crop the image to the desired region
    cropped_image = image.crop((label.x, label.y, label.x1, label.y1))

    # apply the blur filter to the cropped image
    blurred_image = cropped_image.filter(ImageFilter.BLUR)
    blurred_image = blurred_image.filter(ImageFilter.BLUR)

    # create a Draw object to draw on the blurred image
    draw = ImageDraw.Draw(blurred_image)

    # generate some random text
    random_text = "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range( 5* (label.x1 - label.x)) ])

    # measure the size of the text
    text_width, text_height = draw.multiline_textsize(random_text)

    # calculate the vertical center of the blurred image
    y = (blurred_image.height - text_height) / 2

    # draw the text at the vertical center of the blurred image
    draw.multiline_text((0, y), random_text, fill=(0,0,0))

    # paste the blurred image back onto the original image
    image.paste(blurred_image, (label.x, label.y, label.x1, label.y1))

class Label():
    def __init__(self, x, y, x1, y1, label_type):
        self.x = x
        self.y = y
        self.x1 = x1
        self.y1 = y1
        self.type = label_type

files = [i for i in glob.glob("templates/*") if os.path.splitext(i)[1] in [".png", ".jpg", ".tif"] if os.path.exists(os.path.splitext(i)[0] + ".txt")]
text_files = [os.path.splitext(file_path)[0] + ".txt" for file_path in files if os.path.exists(os.path.splitext(file_path)[0] + ".txt")]

index = 0

with open(text_files[0], "r") as f:
    label_data = [i.strip().split(" ") for i in f.readlines()]
    labels = [Label(int(float(j[1])), int(float(j[2])), int(float(j[3])), int(float(j[4])), j[0]) for j in label_data]

img = Image.open(files[0])

for label in labels:
    print(label.type)
    if label.type == "Redact_Blur":
        # blur_region(img, label)
        blur_region_with_text(img, label)
    elif label.type == "Redact_Blur_Text":
        blur_region_with_text(img, label)
    elif label.type == "Value":
        add_text(img, label, generate_currency_value())
    elif label.type == "Curr_Ticker":
        add_text(img, label, generate_curr_tick())
    elif label.type == "Ticker":
        add_text(img, label, generate_ticker())
    elif label.type == "Date":
        add_text(img, label, generate_random_date())
    elif label.type == "Account_Name":
        add_text(img, label, generate_account_name())
img.show()