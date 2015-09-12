# Script for messing around with mysql databases with python
# will need: pip install mysql-connector-python --allow-external mysql-connector-python
from datetime import date, datetime, timedelta
import mysql.connector

DATABASE = ''
USER = ''
PASS = ''

# MySQL connector
db = mysql.connector.connect(user=USER, password=PASS, host='127.0.0.1', database=DATABASE)

cursor = db.cursor()

# Set up prepared statement
add_temp = ("INSERT INTO temp "
               "(value, date, id) "
               "VALUES (%s, %s, %s)")

# Set up data to be inserted
data_temp = ('20', date(2015, 9, 17),  1)

# Insert new temp by binding the statement and the data
cursor.execute(add_temp, data_temp)

# Get the last auto_increment value
last_temp = cursor.lastrowid

# Prepare another query
add_next = ("INSERT INTO next "
              "(Value, Date, Id, last) "
              "VALUES (%(value)s, %(date)s, %(id)s, %(last_temp)s)")

# Insert next data 'key':value
data_next = {
  'Value': '25',
  'date': date(2015, 9, 17),
  'id': 1,
  'last_temp': last_temp,
}
# Execute the statement, which is another insert
cursor.execute(add_next, data_next)

# Make sure data is committed to the database
db.commit()

cursor.close()
db.close()
