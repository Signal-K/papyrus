from flask import Flask, jsonify
from supabase_py import create_client

app = Flask(__name__)

# app.config["SQLALCHEMY_DATABASE_URI"] = ""
# db.init_app(app)

# Create Supabase client

SUPABASE_URL = ''
SUPABASE_KEY = ''
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

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

# Route to fetch items from inventoryITEMS table
@app.route('/items')
def get_items():
    # Query items from inventoryITEMS table
    items = supabase.table('inventoryITEMS').select('*').execute()
    return jsonify(items['data'])

# Route to fetch user inventory from inventoryUSERS table
@app.route('/inventory/<user_id>')
def get_user_inventory(user_id):
    # Query user inventory from inventoryUSERS table
    user_inventory = supabase.table('inventoryUSERS').select('*').eq('owner', user_id).execute()
    return jsonify(user_inventory['data'])

# Main function to run the Flask app
if __name__ == '__main__':
    app.run(debug=True)