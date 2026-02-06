# Q1) Lookup with a fallback

def print_item_price(price_map, item_name):


    if item_name in price_map:
        print(f"{item_name} costs {price_map[item_name]}")
    else:
        print(f"{item_name} not found")


# Test
print_item_price({"bread": 200, "milk": 250}, "bread")   # bread exists
print_item_price({"bread": 200, "milk": 250}, "cheese")  # cheese does not exist



# Q2) Update a dict (add/overwrite)

def set_student_score(scores, name, score):

    scores[name] = score
    print(scores)


# Test
scores = {"Zak": 70, "Bob": 90}
set_student_score(scores, "Zak", 75)  
set_student_score(scores, "Mia", 88)  


# Q3) Frequency counter

def count_codes(codes):
    counts = {}

    for code in codes:
        counts[code] = counts.get(code, 0) + 1
    print(counts)

# Test
count_codes(["OK", "OK", "FAIL", "OK", "ERROR", "FAIL"])


# Q4) Pydantic model + validation

from pydantic import BaseModel, Field, ValidationError

class Reading(BaseModel):

    device_id: str
    temperature: float
    humidity: float
    battery: int = Field(ge=0, le=100)


def validate_reading(data):
    try:
        reading = Reading(**data)
        print("VALID")
        print(reading)
    except ValidationError as e:
        print("INVALID")
        print(e)


valid_data = {
    "device_id": "esp32-1",
    "temperature": 25.1,
    "humidity": 41.2,
    "battery": 88
}
validate_reading(valid_data)


invalid_data = {
    "device_id": "esp32-1",
    "temperature": "hot",  
    "humidity": 41.2,
    "battery": 150         
}
validate_reading(invalid_data)