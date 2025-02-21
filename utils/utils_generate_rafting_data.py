from datetime import datetime, timedelta
import random
import json
import uuid
import pathlib

"""
utils_generate_rafting_data.py

Utility for generating synthetic rafting feedback data.

This script generates and saves rafting reviews (400 positive, 100 negative)
from Memorial Day to Labor Day 2024, featuring 20 unique guides and a mix of half-day and full-day trips.

Usage:
    from utils_generate_rafting_data import generate_rafting_feedback
    data_file = generate_rafting_feedback()
"""

# Define rafting guides (20 total, including 5 senior guides)
GUIDES = [
    "Jake", "Samantha", "Carlos", "Emily", "Tyler", "Ava", "Liam", "Sophia", 
    "Mason", "Olivia", "John (Senior Guide)", "Mary (Senior Guide)", "Henry (Senior Guide)", 
    "Laura (Senior Guide)", "James (Senior Guide)", "Grace", "Daniel", "Noah", "Emma", "Chloe"
]

# Define possible rafting trip types
TRIP_TYPES = ["Half Day", "Full Day"]

# Define the date range (Memorial Day 2024 to Labor Day 2024)
MEMORIAL_DAY_2024 = datetime(2024, 5, 24)
LABOR_DAY_2024 = datetime(2024, 9, 2)
DATE_RANGE = (LABOR_DAY_2024 - MEMORIAL_DAY_2024).days

# Load predefined positive and negative comments
POSITIVE_COMMENTS = [
    "The rapids were just challenging enough to keep things exciting while still feeling safe and manageable.",
    "Watching the sunrise from the river was a breathtaking way to start our adventure.",
    "Our guide’s storytelling about the area’s history and geology made the trip unforgettable.",
    "Rafting together strengthened our family bond in ways we didn’t expect. A perfect experience!",
    "Their commitment to conservation was inspiring! We learned so much about river ecology.",
    "The entire experience was well-organized and stress-free, from the briefing to the final photo.",
    "Thrilling rapids combined with serene floating sections made for a well-balanced adventure.",
    "Our guide’s expertise and calm approach gave us confidence through every rapid.",
    "The post-trip barbecue was the perfect way to celebrate an incredible day on the river.",
    "Each rapid felt like an exciting puzzle that we worked together to solve.",
    "The staff photographer captured incredible moments—our adventure is now beautifully documented!",
    "Our guide read the river like a book, ensuring a smooth and safe experience.",
    "Meeting other rafting groups at the lunch stop added a fun social element to our trip.",
    "Floating through towering canyon walls was a humbling and awe-inspiring moment.",
    "The teamwork and coordination between guides made everything run smoothly and safely.",
    "Learning river navigation techniques added an educational twist to our adventure.",
    "The company’s safety measures were evident throughout, but never at the cost of fun.",
    "Watching wildlife along the river added a magical element to our experience.",
    "The natural hot springs were a perfect and unexpected mid-trip treat!",
    "Our guide’s enthusiasm and humor made the safety briefing surprisingly entertaining.",
    "Seeing nervous group members gain confidence was heartwarming and inspiring.",
    "Every bend in the river unveiled a new stunning landscape to admire.",
    "Just enough splash to keep us cool without overwhelming us—perfect balance!",
    "Our guide’s awareness of changing weather ensured we had the best possible experience.",
    "Cliff jumping during our break was an adrenaline-pumping bonus to an already great day!",
    "Sunlight and water spray created incredible rainbow effects throughout our journey.",
    "It felt like a nature documentary with all the wildlife we spotted!",
    "Our teens stayed off their phones and fully engaged—an absolute miracle!",
    "The sound of the river and birds created a peaceful, natural soundtrack.",
    "The guides’ professionalism showed in how they handled unexpected situations.",
    "Learning traditional river navigation made the experience even more enriching.",
    "Their commitment to conservation is something every company should strive for.",
    "Our guide knew exactly how to balance excitement and safety for our group.",
    "Meeting people from different backgrounds added an extra layer of enjoyment.",
    "Spotting river otters playing near us was an unforgettable moment!",
    "Hearing indigenous history as we rafted gave us a deeper appreciation for the area.",
    "Navigating each rapid felt like a thrilling challenge we conquered together.",
    "The guides’ attention to river conditions made us feel completely secure.",
    "Morning mist rising from the river was a mystical and unforgettable sight.",
    "Our guide knew all the best spots for stunning photos along the way.",
    "Conquering challenging rapids together was a rewarding and unforgettable experience.",
    "Their passion for conservation added depth and meaning to the adventure.",
    "Even the paddling lesson was engaging, making us feel like pros in no time!",
    "The riverside lunch spot was scenic, peaceful, and felt like a luxury picnic.",
    "Our guide made sure everyone, regardless of skill level, felt included.",
    "The river’s seasonal changes were fascinating to learn about during our trip.",
    "The spontaneous water fights between rafts were a hilarious highlight!",
    "Hearing our guide’s rafting stories kept us entertained between rapids.",
    "Their professional photography service meant we could focus on enjoying the adventure.",
    "Ideal weather and water levels made for an absolutely perfect day on the river!"
]

NEGATIVE_COMMENTS = [
    "The water conditions were too rough for beginners, making it a stressful experience.",
    "Our guide barely engaged with us and spent most of the time chatting with other guides.",
    "The provided equipment was old and poorly maintained, making me question its safety.",
    "Too many people were crammed into the raft, making paddling uncomfortable.",
    "The safety briefing was rushed and left us feeling unprepared for the trip.",
    "The rapids were too intense for beginners, leaving some in our group terrified.",
    "Felt unsafe at multiple points, and the guide didn’t reassure us at all.",
    "This trip was overpriced considering the poor equipment and lack of guidance.",
    "The actual time on the water felt too short and rushed for the price.",
    "The campsite was unkempt, with trash and broken equipment scattered everywhere.",
    "Our guide seemed bored and uninterested, making the trip less enjoyable.",
    "Lunch options were terrible—stale food and no accommodation for dietary needs.",
    "The bus to the start point was hot, long, and full of unexpected delays.",
    "The check-in process was chaotic and took too long, cutting into rafting time.",
    "Restroom facilities at both start and finish were filthy and lacked basic supplies.",
    "None of the provided safety gear fit properly, and there were no replacements available.",
    "Too much downtime between sections; felt like we spent more time waiting than rafting.",
    "We received little to no communication before the trip, leaving us unprepared.",
    "The experience didn’t match the website description—fewer rapids and lower-quality facilities.",
    "Staff were rude and unhelpful when we raised safety concerns about the equipment.",
    "The water was freezing, and we weren’t warned to bring the right gear.",
    "Marketing photos were misleading, showing conditions far better than what we experienced.",
    "Hidden fees made the trip much more expensive than advertised, which felt dishonest.",
    "The wetsuits provided were damp, smelly, and clearly not properly cleaned between uses.",
    "The guides constantly rushed us, leaving no time to enjoy the scenery or take photos.",
    "Despite dangerous weather, no alternatives or refunds were offered, which was unacceptable.",
    "Long, boring stretches with no rapids and no engagement from the guides.",
    "Our group was split up without warning, ruining our planned team-building experience.",
    "Booking was unnecessarily complicated, and customer service was unresponsive to questions.",
    "Guides joked amongst themselves instead of ensuring our safety and enjoyment.",
    "Our guide struggled with basic river navigation, making the experience nerve-wracking.",
    "Clearly an inexperienced guide—they kept hesitating and seeking direction from others.",
    "Very concerning that our guide didn’t seem to know basic safety procedures.",
    "Misreading rapids led to our raft getting stuck on rocks multiple times.",
    "Our guide openly admitted it was their first week leading trips solo.",
    "Their hesitation during rapids made it clear they lacked confidence and experience.",
    "The guide needed constant help from other rafts, making us feel uneasy.",
    "Our guide couldn’t properly explain water patterns, making safety discussions confusing.",
    "The guide seemed overwhelmed, frequently changing course in the middle of rapids.",
    "Other guides had to warn our guide about hazards they should have seen.",
    "Several close calls happened because our guide couldn’t read water conditions properly.",
    "Basic concepts about currents and river safety were not explained to us.",
    "Our guide froze up during a moderate rapid, requiring help from another guide.",
    "They struggled with raft control even in calm water, making us very nervous.",
    "The guide was so focused on remembering their training that they failed to lead.",
    "Their lack of confidence in rescue procedures was deeply concerning for the group.",
    "We expected an experienced guide, but it was clear ours needed more training.",
    "The trip felt disorganized, and our guide’s inexperience made it worse.",
    "Being led by a guide who just finished training didn’t feel safe.",
    "Our guide couldn’t answer basic questions about river currents or safety procedures.",
    "The company should ensure their guides are fully prepared before leading a trip.",
    "Every aspect of this experience felt amateurish, from the gear to the guiding.",
    "Our guide’s uncertainty made the entire journey feel more stressful than exciting.",
    "This trip was marketed as beginner-friendly, but it felt dangerous and unorganized.",
    "It’s unacceptable for a rafting company to send out guides this unprepared.",
    "We paid for a full adventure, but got a chaotic and unsafe experience.",
    "The trip was disappointing in every way—poor planning, untrained staff, and no accountability.",
    "Would not recommend this company to anyone looking for a well-organized trip.",
    "Frustrating experience from start to finish, with no attention to customer needs.",
    "The only thing I enjoyed was getting off the raft at the end.",
    "I expected adventure and got stress—this was not worth the money at all.",
    "The company’s lack of professionalism showed in every aspect of the trip.",
    "Everything about this trip made me question whether safety was a priority here.",
    "We were promised excitement but got a long, frustrating, disorganized mess instead."
]

# Ensure unique positive and negative comments
UNIQUE_POSITIVE_COMMENTS = list(set(POSITIVE_COMMENTS))
UNIQUE_NEGATIVE_COMMENTS = list(set(NEGATIVE_COMMENTS))

def generate_rafting_feedback(output_file="data/all_rafting_remarks.json"):
    """
    Generate and save rafting customer feedback.

    Args:
        output_file (str): Path where the JSON file will be saved.

    Returns:
        pathlib.Path: The path to the generated JSON file.
    """
    data_folder = pathlib.Path(output_file).parent
    data_folder.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists
    data_file = pathlib.Path(output_file)

    # Generate 400 positive and 100 negative comments (allowing duplicates)
    customer_remarks = [
        {
            "comment": random.choice(UNIQUE_POSITIVE_COMMENTS),
            "character_count": len(random.choice(UNIQUE_POSITIVE_COMMENTS)),
            "guide": random.choice(GUIDES),
            "uuid": str(uuid.uuid4()),
            "date": (MEMORIAL_DAY_2024 + timedelta(days=random.randint(0, DATE_RANGE))).strftime("%Y-%m-%d"),
            "trip_type": random.choice(TRIP_TYPES),
            "timestamp": datetime.utcnow().isoformat(),
            "is_negative": False,
        }
        for _ in range(400)
    ] + [
        {
            "comment": random.choice(UNIQUE_NEGATIVE_COMMENTS),
            "character_count": len(random.choice(UNIQUE_NEGATIVE_COMMENTS)),
            "guide": random.choice(GUIDES),
            "uuid": str(uuid.uuid4()),
            "date": (MEMORIAL_DAY_2024 + timedelta(days=random.randint(0, DATE_RANGE))).strftime("%Y-%m-%d"),
            "trip_type": random.choice(TRIP_TYPES),
            "timestamp": datetime.utcnow().isoformat(),
            "is_negative": True,
        }
        for _ in range(100)
    ]

    # Save to a JSON file
    with open(data_file, "w") as file:
        json.dump(customer_remarks, file, indent=4)

    return data_file  # Return the path for confirmation

# Example usage:
if __name__ == "__main__":
    generated_file = generate_rafting_feedback()
    print(f"Generated rafting feedback file: {generated_file}")
