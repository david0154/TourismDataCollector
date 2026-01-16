"""
Indian states and popular tourist places data
"""

INDIAN_STATES = {
    "Andhra Pradesh": "AP",
    "Arunachal Pradesh": "AR",
    "Assam": "AS",
    "Bihar": "BR",
    "Chhattisgarh": "CG",
    "Goa": "GA",
    "Gujarat": "GJ",
    "Haryana": "HR",
    "Himachal Pradesh": "HP",
    "Jharkhand": "JH",
    "Karnataka": "KA",
    "Kerala": "KL",
    "Madhya Pradesh": "MP",
    "Maharashtra": "MH",
    "Manipur": "MN",
    "Meghalaya": "ML",
    "Mizoram": "MZ",
    "Nagaland": "NL",
    "Odisha": "OR",
    "Punjab": "PB",
    "Rajasthan": "RJ",
    "Sikkim": "SK",
    "Tamil Nadu": "TN",
    "Telangana": "TG",
    "Tripura": "TR",
    "Uttar Pradesh": "UP",
    "Uttarakhand": "UK",
    "West Bengal": "WB",
    "Andaman and Nicobar Islands": "AN",
    "Chandigarh": "CH",
    "Dadra and Nagar Haveli and Daman and Diu": "DD",
    "Delhi": "DL",
    "Jammu and Kashmir": "JK",
    "Ladakh": "LA",
    "Lakshadweep": "LD",
    "Puducherry": "PY"
}

TOURIST_PLACES = {
    "Rajasthan": ["Jaipur", "Udaipur", "Jaisalmer", "Jodhpur", "Pushkar", "Mount Abu"],
    "Kerala": ["Munnar", "Alleppey", "Kochi", "Kovalam", "Wayanad", "Thekkady"],
    "Goa": ["Panaji", "Calangute", "Baga", "Anjuna", "Palolem", "Vagator"],
    "Himachal Pradesh": ["Shimla", "Manali", "Dharamshala", "Kullu", "Kasol", "Dalhousie"],
    "Uttarakhand": ["Nainital", "Mussoorie", "Rishikesh", "Haridwar", "Dehradun", "Auli"],
    "Tamil Nadu": ["Chennai", "Ooty", "Kodaikanal", "Mahabalipuram", "Madurai", "Rameswaram"],
    "Karnataka": ["Bangalore", "Mysore", "Coorg", "Hampi", "Chikmagalur", "Gokarna"],
    "Maharashtra": ["Mumbai", "Pune", "Lonavala", "Mahabaleshwar", "Nashik", "Aurangabad"],
    "West Bengal": ["Kolkata", "Darjeeling", "Digha", "Sundarbans", "Kalimpong", "Dooars"],
    "Uttar Pradesh": ["Agra", "Varanasi", "Lucknow", "Mathura", "Vrindavan", "Allahabad"]
}

def get_tourist_places(state: str):
    """Get popular tourist places for a state"""
    return TOURIST_PLACES.get(state, [])
