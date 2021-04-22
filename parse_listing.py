import sys

def clean_end(text):
    # Remove everything after the "click to manage subscription"
    # notice which appears after the last listing
    text = text.split("[ Click here to")
    return text[0]

def parse_listings(text):
    # Parse into separate listings.
    # Each one starts with a Markdown link with no text
    listings = text.split("[](")[1:]
    return listings

def extract_data(listing):
    lines = listing.splitlines()
    url = lines[0]
    url = url.strip()[:-1] # remove extra bracket from end after hack before
    _ = lines[1] # empty line
    description = lines[2]
    description = description.split("**](")[0][3:]
    address = lines[3]
    address = address.split("](")[0][1:]
    price_or_additional_info = lines[4]
    if price_or_additional_info.startswith("CHF") or price_or_additional_info.startswith("by request"):
        # additional info ("furnished, temporary, etc) is skipped - move everything up one
        additional_info = ' '
        price = lines[4]
        rooms = lines[5]
        reference = lines[6]
    else:
        additional_info = lines[4]
        price = lines[5]
        rooms = lines[6]
        reference = lines[7]
    return url, description, address, additional_info, price, rooms, reference

def build_listing(url, description, address, additional_info, price, rooms, reference):
    l = {
            "url": url.strip(),
            "description": description.strip(),
            "address": address.strip(),
            "additional_info": additional_info.strip(),
            "price": price.strip(),
            "rooms": rooms.strip(),
            "reference": reference.strip()
    }
    return l

def process_file(fname):
    with open(fname) as f:
        text = f.read()

    text = clean_end(text)
    listings = parse_listings(text)
    for listing in listings:
        u, d, a, ai, p, ro, re = extract_data(listing)
        structured_listing = build_listing(u, d, a, ai, p, ro, re)
        print(structured_listing)
        print("___")

def get_listings_from_text(text):
    text = clean_end(text)
    listings = parse_listings(text)

    clean_listings = []
    for listing in listings:
        u, d, a, ai, p, ro, re = extract_data(listing)
        clean_listing = build_listing(u, d, a, ai, p, ro, re)
        clean_listings.append(clean_listing)
    return clean_listings


if __name__ == "__main__":
    fname = sys.argv[1]
    process_file(fname)

