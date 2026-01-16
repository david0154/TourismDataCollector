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
    "Rajasthan": ["Jaipur", "Udaipur", "Jaisalmer", "Jodhpur", "Pushkar", "Mount Abu", "Bikaner", "Ajmer"],
    "Kerala": ["Munnar", "Alleppey", "Kochi", "Kovalam", "Wayanad", "Thekkady", "Varkala", "Kumarakom"],
    "Goa": ["Panaji", "Calangute", "Baga", "Anjuna", "Palolem", "Vagator", "Candolim", "Old Goa"],
    "Himachal Pradesh": ["Shimla", "Manali", "Dharamshala", "Kullu", "Kasol", "Dalhousie", "Spiti Valley", "Mcleodganj"],
    "Uttarakhand": ["Nainital", "Mussoorie", "Rishikesh", "Haridwar", "Dehradun", "Auli", "Jim Corbett", "Kedarnath"],
    "Tamil Nadu": ["Chennai", "Ooty", "Kodaikanal", "Mahabalipuram", "Madurai", "Rameswaram", "Kanyakumari", "Pondicherry"],
    "Karnataka": ["Bangalore", "Mysore", "Coorg", "Hampi", "Chikmagalur", "Gokarna", "Badami", "Udupi"],
    "Maharashtra": ["Mumbai", "Pune", "Lonavala", "Mahabaleshwar", "Nashik", "Aurangabad", "Alibaug", "Matheran"],
    "West Bengal": ["Kolkata", "Darjeeling", "Digha", "Sundarbans", "Kalimpong", "Dooars", "Mandarmani", "Shantiniketan"],
    "Uttar Pradesh": ["Agra", "Varanasi", "Lucknow", "Mathura", "Vrindavan", "Allahabad", "Ayodhya", "Sarnath"],
    "Gujarat": ["Ahmedabad", "Gir National Park", "Dwarka", "Somnath", "Rann of Kutch", "Saputara", "Diu", "Statue of Unity"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Khajuraho", "Gwalior", "Ujjain", "Pachmarhi", "Sanchi", "Omkareshwar"],
    "Delhi": ["India Gate", "Red Fort", "Qutub Minar", "Lotus Temple", "Humayun's Tomb", "Akshardham", "Chandni Chowk"],
    "Jammu and Kashmir": ["Srinagar", "Gulmarg", "Pahalgam", "Sonamarg", "Leh", "Kargil", "Patnitop"],
    "Andhra Pradesh": ["Tirupati", "Visakhapatnam", "Araku Valley", "Vijayawada", "Hyderabad"],
    "Telangana": ["Hyderabad", "Warangal", "Ramoji Film City", "Khammam"],
    "Assam": ["Guwahati", "Kaziranga", "Majuli", "Sivasagar", "Tezpur"],
    "Punjab": ["Amritsar", "Chandigarh", "Ludhiana", "Patiala", "Anandpur Sahib"],
    "Odisha": ["Puri", "Bhubaneswar", "Konark", "Chilika Lake", "Cuttack"]
}

def get_tourist_places(state: str):
    """Get popular tourist places for a state"""
    return TOURIST_PLACES.get(state, [])
