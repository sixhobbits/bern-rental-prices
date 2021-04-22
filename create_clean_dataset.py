import pandas as pd
import re

def get_price(price):
    words = price.split()
    if price.startswith("CHF "):
        int_price = words[1].replace('’', '')
        int_price = float(int_price)
        return int_price
    return None

def get_post_code(address):
    reg_postcode = r"\d\d\d\d "
    # if there is a four digit house number, then the post code will be the last match
    postcode = re.findall(reg_postcode, address)[-1].strip()
    return postcode
    
def get_city(address):
    reg_postcode = r"\d\d\d\d "
    # if there is a four digit house number, then the post code will be the last match
    comps = re.split(reg_postcode, address)
    return comps[-1]  

def get_num_rooms(rooms):
    try:
        if rooms.startswith(","):
            return None
        # either `1 rooms , 56m2` or 
        # `1 rooms`
        rms, _ = rooms.split(" , ")
        int_rooms = float(rms.split()[0])
        if "½" in rooms:
            int_rooms += 0.5
        return int_rooms
    except:
        return None
    
def get_size(rooms):
    try:
        _, sqm = rooms.split(", ")
        int_sqm = sqm.split("m²")[0]
        return int_sqm
    except Exception as e:
        return None
    
def is_shared(description):
    return " shared " in description.lower()

def is_temporary(additional_info):
    try:
        return "temporary" in additional_info.lower()
    except:
        return False

def is_furnished(additional_info):
    try:
        return "furnished" in additional_info.lower()
    except:
        return False

def create_clean():
    df = pd.read_csv("https://bern.dwyer.co.za")
    df['price'] = df['price'].apply(get_price)
    df['post_code'] = df['address'].apply(get_post_code)
    df['city'] = df['address'].apply(get_city)
    df['num_rooms'] = df['rooms'].apply(get_num_rooms)
    df['size'] = df['rooms'].apply(get_size)
    df['shared'] = df['description'].apply(is_shared)
    df['temporary'] = df['additional_info'].apply(is_temporary)
    df['furnished'] = df['additional_info'].apply(is_furnished)
    df = df.drop(columns=['address', 'additional_info', 'rooms', 'reference'])
    df.to_csv("/berndata/bern_clean.csv")
