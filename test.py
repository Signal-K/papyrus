from flask import Flask, jsonify, request
from supabase_py import create_client
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://postgres.qw"
# db.init_app(app)

# Create Supabase client
SUPABASE_URL = 'https://qwbufbmxkjfaikoloudl.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3YnVmYm14a2pmYWlrb2xvdWRsIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njk5NDE3NTksImV4cCI6MTk4NTUxNzc1OX0.RNz5bvsVwLvfYpZtUjy0vBPcho53_VS2AIVzT8Fm-lk'
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

itemList = { # This should be automated in the `/items` route later
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

crafting_recipes = [
    {"input": [(11, 1), (13, 1)], "output": (14, 1)},  # Coal + Silicates = Transiting Telescope
]

# Route to fetch items from inventoryITEMS table
@app.route('/items')
def get_items():
    # Query items from inventoryITEMS table
    items = supabase.table('inventoryITEMS').select('*').execute()
    return jsonify(items['data'], itemList)

# Route to fetch user inventory from inventoryUSERS table
@app.route('/inventory/<user_id>')
def get_user_inventory(user_id):
    # Query user inventory from inventoryUSERS table
    user_inventory = supabase.table('inventoryUSERS').select('*').eq('owner', user_id).execute()
    return jsonify(user_inventory['data'] + itemList)

@app.route('/craft_structure', methods=['POST']) # In this method, the actual crafting/removal of items would be done in the `client` repo
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
            return jsonify({'status': 'fail', 'message': f'Insufficient {itemList[item_id]["name"]}'}), 400

    """
    # If the user has the required items, deduct them from the inventory
    for item_id, quantity_needed in items_needed:
    # Reduce the quantity of the item in the inventory
        for item in user_inventory['data']:
            if item['item'] == item_id:
                remaining_quantity = item['quantity'] - quantity_needed
                supabase.table('inventoryUSERS').update({'quantity': remaining_quantity}).eq('owner', user_id).eq('item', item_id).execute()
                break
    """
    
    # Add the crafted structure to the user's inventory
    supabase.table('inventoryUSERS').insert({'item': structure_id, 'owner': user_id, 'quantity': 1}).execute()
    
    return jsonify({'status': 'proceed', 'message': 'Structure crafted successfully'}), 200
    # Get user id and structure id from the request
    data = request.get_json()
    user_id = data.get('user_id')
    structure_id = data.get('structure_id')

    # Find the crafting recipe for the specified structure
    recipe = None
    for crafting_recipe in crafting_recipes:
        if crafting_recipe['output'][0] == structure_id:
            recipe = crafting_recipe
            break

    if not recipe:
        return jsonify({'status': 'fail', 'message': 'Structure not found'})

    # Check if the user has enough of each required item
    for item_id, quantity in recipe['input']:
        user_items = supabase.table('inventoryUSERS').select('quantity').eq('owner', user_id).eq('item', item_id).execute()
        total_quantity = sum([item['quantity'] for item in user_items['data']])
        if total_quantity < quantity:
            return jsonify({'status': 'fail', 'message': f'Insufficient {itemList[item_id]["name"]}'})
    
    # Calculate quantities to be deducted from the inventory
    deductions = []
    for item_id, quantity in recipe['input']:
        quantity_to_deduct = quantity
        user_items = supabase.table('inventoryUSERS').select('id', 'quantity').eq('owner', user_id).eq('item', item_id).execute()
        for item in user_items['data']:
            if item['quantity'] >= quantity_to_deduct:
                deductions.append({'id': item['id'], 'quantity': quantity_to_deduct})
                break
            else:
                quantity_to_deduct -= item['quantity']
                deductions.append({'id': item['id'], 'quantity': item['quantity']})
    
    # Construct the response
    response = {
        'status': 'proceed',
        'message': 'User can craft the structure',
        'deductions': deductions
    }
    return jsonify(response)

"""
# class InventoryUsers(db.Model):
#     __tablename__ = 'inventoryUSERS'

#     id = db.Column(db.BigInteger, primary_key=True)
#     item = db.Column(db.BigInteger, db.ForeignKey('inventoryITEMS.id'))
#     owner = db.Column(db.String, db.ForeignKey('profiles.id'))
#     quantity = db.Column(db.Float)
#     location = db.Column(db.BigInteger, db.ForeignKey('inventoryPLANETS.id'))
#     sector = db.Column(db.BigInteger, db.ForeignKey('basePlanetSectors.id'))
#     planetSector = db.Column(db.BigInteger, db.ForeignKey('basePlanetSectors.id'))

# class InventoryItems(db.Model):
#     __tablename__ = 'inventoryITEMS'

#     id = db.Column(db.BigInteger, primary_key=True)
#     name = db.Column(db.String)
#     description = db.Column(db.Text)
#     cost = db.Column(db.Integer)
#     icon_url = db.Column(db.String)
#     ItemCategory = db.Column(db.String)
#     parentItem = db.Column(db.BigInteger)
#     itemLevel = db.Column(db.Float, default=1.0)
#     oldAssets = db.Column(db.ARRAY(db.Text))
"""

# Main function to run the Flask app
if __name__ == '__main__':
    app.run(debug=True)