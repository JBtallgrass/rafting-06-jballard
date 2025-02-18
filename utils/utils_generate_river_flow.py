"""
utils_generate_river_flow.py

Generates rafting-specific river flow data for Section 9 and Section 10 of the French Broad River.
Information pulled from https://www.exploreasheville.com/marshall/group-friendly-activities/outdoor/french-broad-adventures
"""

from datetime import datetime, timedelta
import random
import json
import pathlib
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def classify_rapid_difficulty(river_flow):
    """Classify rapid difficulty based on river flow (cfs)."""
    if river_flow < 1000:
        return "Class II"
    elif 1000 <= river_flow <= 2500:
        return "Class III"
    elif river_flow > 2500:
        return "Class IV"
    else:
        return "Unknown"

def assess_river_condition(river_flow, recent_precipitation):
    """Assess overall river condition based on flow and recent rainfall."""
    if river_flow > 4000 or recent_precipitation > 2.0:
        return "Flood Stage"
    elif river_flow > 3000 or recent_precipitation > 1.5:
        return "High Risk"
    elif 2000 <= river_flow <= 3000:
        return "Moderate Risk"
    else:
        return "Safe"

def determine_water_visibility(river_flow, recent_precipitation):
    """Determine water clarity based on flow and precipitation."""
    if recent_precipitation > 1.5 or river_flow > 3500:
        return "Poor"
    elif recent_precipitation > 0.5 or river_flow > 2500:
        return "Moderate"
    else:
        return "Clear"

def determine_debris_level(recent_precipitation):
    """Estimate floating debris level based on rainfall."""
    if recent_precipitation > 1.5:
        return "High"
    elif recent_precipitation > 0.5:
        return "Moderate"
    else:
        return "Low"

def generate_river_flow_data(output_file="data/enhanced_rafting_conditions.json"):
    """Generate rafting-specific river flow data with additional flood and debris parameters."""
    data_folder = pathlib.Path(output_file).parent
    data_folder.mkdir(parents=True, exist_ok=True)
    data_file = pathlib.Path(output_file)

    memorial_day_2024 = datetime(2024, 5, 24)
    labor_day_2024 = datetime(2024, 9, 2)
    date_range = (labor_day_2024 - memorial_day_2024).days

    river_data = []

    for i in range(date_range + 1):
        current_date = memorial_day_2024 + timedelta(days=i)
        month = current_date.month
        
        # Adjust flow rates based on seasonal trends
        if month in [5, 6]:  # Spring runoff months
            river_flow = random.randint(1200, 4000)
        elif month in [7, 8]:  # Peak summer, typically lower flow
            river_flow = random.randint(800, 2800)
        else:  # Transition months
            river_flow = random.randint(1000, 3200)
        
        # Randomly introduce extreme spikes to simulate rain-driven surges
        if random.random() < 0.1:  # 10% chance of an extreme high flow day
            river_flow += random.randint(1000, 2000)

        water_level = round(random.uniform(2.5, 7.0), 2)  # Extended range
        water_temperature = random.randint(55, 75)
        recent_precipitation = round(random.uniform(0, 2.5), 2)
        rapid_difficulty = classify_rapid_difficulty(river_flow)
        river_condition = assess_river_condition(river_flow, recent_precipitation)
        water_visibility = determine_water_visibility(river_flow, recent_precipitation)
        debris_level = determine_debris_level(recent_precipitation)

        river_record = {
            "date": current_date.strftime("%Y-%m-%d"),
            "river_flow": river_flow,
            "water_level": water_level,
            "water_temperature": water_temperature,
            "rapid_difficulty": rapid_difficulty,
            "recent_precipitation": recent_precipitation,
            "river_condition": river_condition,
            "water_visibility": water_visibility,
            "debris_level": debris_level
        }

        river_data.append(river_record)

    # Save to a JSON file with error handling
    try:
        with open(data_file, "w", encoding="utf-8") as file:
            json.dump(river_data, file, indent=4)
        logging.info(f"Enhanced river flow data saved to {data_file} with {len(river_data)} records.")
    except Exception as e:
        logging.error(f"Error saving file: {e}")

    return data_file

# Example usage:
if __name__ == "__main__":
    generated_file = generate_river_flow_data()
    print(f"Generated enhanced rafting conditions file: {generated_file}")
