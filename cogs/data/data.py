from cogs.utils import pyson

guild_resources = pyson.Pyson('cogs/data/resources.json')
player_resources = pyson.Pyson('cogs/data/player_resources.json')

resource_emoji = {
    "Food": "🍎",
    "Iron": "⛏️",
    "Wood": "🌲",
    "Stone": "🧱",
    "Livestock": "🐄",
    "Coal": "🔥",
    "Gems": "💎",
    "Gold": "💰",
    "Herbs": "🌿",
    "Grain": "🌽",
    "Workers": "👷",
    "Water": "💧"}

resource_list = {
    "Food": 0,
    "Iron": 0,
    "Wood": 0,
    "Stone": 0,
    "Livestock": 0,
    "Coal": 0,
    "Gems": 0,
    "Gold": 0,
    "Herbs": 0,
    "Grain": 0,
    "Workers": 0,
    "Water": 0
}
