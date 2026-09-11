"""
Mock upstream services providing data for local development and offline execution.
"""
from typing import Dict, Any
from app.models.domain import UserProfile, KundliData, HoroscopeData, PanchangData


MOCK_USERS: Dict[str, Dict[str, Any]] = {
    "user_101": {
        "id": "user_101",
        "name": "Aarav Sharma",
        "language": "en",
        "subscription": "premium",
        "tonePreference": "motivational",
        "birthDetails": {
            "date": "1997-08-15",
            "time": "09:35",
            "place": "Delhi"
        }
    },
    "user_102": {
        "id": "user_102",
        "name": "Priya Patel",
        "language": "hi",
        "subscription": "free",
        "tonePreference": "compassionate",
        "birthDetails": {
            "date": "1999-03-22",
            "time": "14:20",
            "place": "Mumbai"
        }
    },
    "user_103": {
        "id": "user_103",
        "name": "Rohan Verma",
        "language": "en",
        "subscription": "standard",
        "tonePreference": "direct",
        "birthDetails": {
            "date": "1992-11-05",
            "time": "06:10",
            "place": "Bengaluru"
        }
    }
}

MOCK_KUNDLI: Dict[str, Dict[str, Any]] = {
    "user_101": {
        "lagna": "Libra",
        "moonSign": "Scorpio",
        "currentDasha": {
            "mahadasha": "Rahu",
            "antardasha": "Mars"
        },
        "houses": {
            "6": {
                "lord": "Jupiter",
                "strength": "Average"
            },
            "7": {
                "lord": "Mars",
                "strength": "Weak"
            },
            "10": {
                "lord": "Moon",
                "strength": "Strong"
            }
        }
    },
    "user_102": {
        "lagna": "Cancer",
        "moonSign": "Taurus",
        "currentDasha": {
            "mahadasha": "Jupiter",
            "antardasha": "Venus"
        },
        "houses": {
            "6": {
                "lord": "Saturn",
                "strength": "Strong"
            },
            "7": {
                "lord": "Saturn",
                "strength": "Strong"
            },
            "10": {
                "lord": "Mars",
                "strength": "Average"
            }
        }
    },
    "user_103": {
        "lagna": "Aries",
        "moonSign": "Leo",
        "currentDasha": {
            "mahadasha": "Saturn",
            "antardasha": "Rahu"
        },
        "houses": {
            "6": {
                "lord": "Mercury",
                "strength": "Weak"
            },
            "7": {
                "lord": "Venus",
                "strength": "Strong"
            },
            "10": {
                "lord": "Saturn",
                "strength": "Strong"
            }
        }
    }
}

MOCK_HOROSCOPE: Dict[str, Dict[str, Any]] = {
    "user_101": {
        "career": "Networking may bring new opportunities.",
        "finance": "Avoid risky investments.",
        "health": "Prioritize proper sleep.",
        "relationship": "Communication with your partner improves."
    },
    "user_102": {
        "career": "Patience is key at work this week.",
        "finance": "Good time for saving and budgeting.",
        "health": "Incorporate light yoga and hydration.",
        "relationship": "Harmonious time for family bonding."
    },
    "user_103": {
        "career": "A major leadership project is taking shape.",
        "finance": "Unexpected expenses might arise.",
        "health": "Keep stress levels in check.",
        "relationship": "Clear misunderstandings early."
    }
}

MOCK_PANCHANG: Dict[str, Any] = {
    "date": "2026-08-01",
    "tithi": "Shukla Panchami",
    "nakshatra": "Rohini",
    "yoga": "Siddhi",
    "karana": "Bava"
}


def get_mock_user(user_id: str) -> Dict[str, Any]:
    if user_id in MOCK_USERS:
        return MOCK_USERS[user_id]
    # Default fallback profile for unknown user IDs
    return {
        "id": user_id,
        "name": f"User {user_id}",
        "language": "en",
        "subscription": "free",
        "tonePreference": "motivational",
        "birthDetails": {"date": "2000-01-01", "time": "12:00", "place": "Delhi"}
    }


def get_mock_kundli(user_id: str) -> Dict[str, Any]:
    if user_id in MOCK_KUNDLI:
        return MOCK_KUNDLI[user_id]
    return MOCK_KUNDLI["user_101"]


def get_mock_horoscope(user_id: str) -> Dict[str, Any]:
    if user_id in MOCK_HOROSCOPE:
        return MOCK_HOROSCOPE[user_id]
    return MOCK_HOROSCOPE["user_101"]


def get_mock_panchang() -> Dict[str, Any]:
    return MOCK_PANCHANG
