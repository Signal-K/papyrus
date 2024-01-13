from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = ""
db.init_app(app)

class InventoryUsers(db.Model):
    __tablename__ = 'inventoryUSERS'

    id = db.Column(db.BigInteger, primary_key=True)
    item = db.Column(db.BigInteger, db.ForeignKey('inventoryITEMS.id'))
    owner = db.Column(db.String, db.ForeignKey('profiles.id'))
    quantity = db.Column(db.Float)
    location = db.Column(db.BigInteger, db.ForeignKey('inventoryPLANETS.id'))
    sector = db.Column(db.BigInteger, db.ForeignKey('basePlanetSectors.id'))
    planetSector = db.Column(db.BigInteger, db.ForeignKey('basePlanetSectors.id'))

class InventoryItems(db.Model):
    __tablename__ = 'inventoryITEMS'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)
    cost = db.Column(db.Integer)
    icon_url = db.Column(db.String)
    ItemCategory = db.Column(db.String)
    parentItem = db.Column(db.BigInteger)
    itemLevel = db.Column(db.Float, default=1.0)
    oldAssets = db.Column(db.ARRAY(db.Text))

@app.route('/inventory_items', methods=['GET'])
def get_inventory_items():
    items = InventoryItems.query.all()
    items_dict = [{"id": item.id, "name": item.name, "description": item.description, 
                   "cost": item.cost, "icon_url": item.icon_url, "ItemCategory": item.ItemCategory,
                   "parentItem": item.parentItem, "itemLevel": item.itemLevel, "oldAssets": item.oldAssets}
                  for item in items]
    return jsonify(items_dict)

if __name__ == "__main__":
    app.run(debug=True)