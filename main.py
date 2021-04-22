import csv
import traceback
from datetime import datetime
from hashlib import md5

import ftfy
from flask import Flask, render_template, request, jsonify, send_file

from parse_listing import get_listings_from_text

app = Flask(__name__)

OUTFILE = "/berndata/bern.csv"

def save_input(plain):
    try:
        hsh = md5(plain.encode("utf8")).hexdigest()
        with open(f"/berndata/{hsh}.txt", "w", encoding="UTF-8") as f:
            f.write(plain)
            f.write("\n")
            f.write(datetime.utcnow().isoformat())
    except Exception as e:
        print("error in save_input()")
        print(e)

def process_text(plain):
    print("process_text()")
    save_input(plain)
    print("getting listings")
    listings = get_listings_from_text(plain)

    print("opening CSV")
    
    with open(OUTFILE, 'a', encoding='UTF-8') as csvfile:
        columns = ["date", "url", "description", "address", "additional_info", "price", "rooms", "reference"]
        csvwriter = csv.DictWriter(csvfile, delimiter=',', fieldnames=columns)

        for listing in listings:
            try:
                print("writing new listing")
                listing["date"] = datetime.utcnow().isoformat()
                csvwriter.writerow(listing)
            except Exception as e:
                print("Error writing listing to csv")
                print(e)
                traceback.print_exc()

def format_text_listing(plain):
    save_input(plain)
    
    # Split off stuff at end
    plain = plain.split("Click here to change your subscription settings")[0]

    # Split off stuff at start
    plain = plain.split("your search:")[1]

    lines = plain.splitlines()

    # split into separate listings
    # each listing starts with a URL and continues until the first occurrence of a different url

    # remove first lines
    index = 0
    while not lines[index].startswith("<https://flat"):
        index += 1

    curr_listing_url = lines[index].strip()
    listings = []
    curr_listing = []
    while True:
        try:
            curr_listing.append(ftfy.fix_text(lines[index]))
            index += 1
            if lines[index].strip().startswith("<https://flat") and lines[index].strip() != curr_listing_url:
                listings.append(curr_listing[:])
                curr_listing_url = lines[index].strip()
                curr_listing = []
        except Exception as e:
            listings.append(curr_listing[:])
            print("Error in while")
            print(e)
            break

    print("found",len(listings), "listings")
    with open(OUTFILE, 'a', encoding='UTF-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        for listing in listings:
            print(listing)
            print("*********")
            spamwriter.writerow(listing)
    print("Written all and closed file")
    print(OUTFILE)

@app.route("/inemail", methods=["GET", "POST"])
def inemail():
    try:
        print("Starting inemail()")
        js = request.get_json()
        listings = process_text(js['plain'])
        return "I'm done :)"
    except Exception as e:
        print(e)
        traceback.print_exc()
        try:
            js = request.get_json()
            print(js)
            print(":( :( :( ")
            print(js['plain'])
            print(" :( :( ")
        except Exception as ie:
            print("couldn't get json")
            print(ie)

@app.route("/")
def home():
    return send_file(OUTFILE)

@app.route("/get_clean")
def get_clean():
    from create_clean_dataset import create_clean
    create_clean()
    return send_file("/berndata/bern_clean.csv")

if __name__ == "__main__":
    print("Running")
    app.run("0.0.0.0", debug=True)
