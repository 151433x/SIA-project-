# import things
from flask_table import Table, Col
from SIA_helper import resources
# Declare your table
class ItemTable(Table):
    name = Col('Name')
    description = Col('service')
    location=Col('location')
    phone_number=Col('phonenumber')
    

# Populate the table
table = ItemTable(resources)

# Print the html
print(table.__html__())
# or just {{ table }} from within a Jinja template