from flask import Flask, jsonify, request
from supabase_py import create_client
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize Supabase client
SUPABASE_URL = 'https://qwbufbmxkjfaikoloudl.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3YnVmYm14a2pmYWlrb2xvdWRsIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njk5NDE3NTksImV4cCI6MTk4NTUxNzc1OX0.RNz5bvsVwLvfYpZtUjy0vBPcho53_VS2AIVzT8Fm-lk'
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Define item list
item_list = {
    11: {"name": "Coal", "type": "Minerals"},
    13: {"name": "Silicates", "type": "Minerals"},
    15: {"name": "Iron", "type": "Minerals"},
    17: {"name": "Alloy", "type": "Minerals"},
    18: {"name": "Fuel", "type": "Minerals"},
    19: {"name": "Copper", "type": "Minerals"},
    20: {"name": "Chromium", "type": "Minerals"},
    16: {"name": "Nickel", "type": "Minerals"},
    21: {"name": "Water", "type": "Minerals"},
    14: {"name": "Transiting Telescope", "type": "Structure"},
    12: {"name": "Telescope Signal Receiver", "type": "Structure"},
}

# Define crafting recipes
crafting_recipes = [
    {"input": [(11, 1), (13, 1)], "output": (14, 1)},  # Coal + Silicates = Transiting Telescope
]

# Route to fetch items from inventoryITEMS table
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(item_list)

# Route to fetch user inventory from inventoryUSERS table
@app.route('/inventory/<user_id>', methods=['GET'])
def get_user_inventory(user_id):
    user_inventory = supabase.table('inventoryUSERS').select('*').eq('owner', user_id).execute()
    return jsonify(user_inventory['data'])

# Route to craft structure
@app.route('/craft_structure', methods=['POST'])
def craft_structure():
    data = request.json
    user_id = data.get('user_id')
    structure_id = data.get('structure_id')

    # Retrieve the crafting recipe for the specified structure
    recipe = next((recipe for recipe in crafting_recipes if recipe['output'][0] == structure_id), None)

    if recipe is None:
        return jsonify({'status': 'fail', 'message': 'Invalid structure ID'}), 400

    # Check if the user has the required items in their inventory
    user_inventory = supabase.table('inventoryUSERS').select('item', 'quantity').eq('owner', user_id).execute()
    items_needed = recipe['input']
    items_available = {item['item']: item['quantity'] for item in user_inventory['data']}

    for item_id, quantity_needed in items_needed:
        if item_id not in items_available or items_available[item_id] < quantity_needed:
            return jsonify({'status': 'fail', 'message': f'Insufficient {item_list[item_id]["name"]}'}), 400

    # Add the crafted structure to the user's inventory
    supabase.table('inventoryUSERS').insert({'item': structure_id, 'owner': user_id, 'quantity': 1}).execute()

    return jsonify({'status': 'proceed', 'message': 'Structure crafted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)