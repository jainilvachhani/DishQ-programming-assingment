from flask import Flask, request, render_template
import sqlite3
app = Flask(__name__)

'''
	Helper function to get all entries from the database
'''
def selectAll():
	conn = sqlite3.connect('database.db')
	c = conn.cursor()
	data = []
	for row in c.execute('SELECT * FROM food'):
		data.append(row)
	conn.commit()
	conn.close()
	return data


'''
	The function to get data and render it on HTML
'''
@app.route("/")
def main():
    data = []
    data = selectAll()
    return render_template("index.html",row=data)
if __name__ == "__main__":
    app.run()
    

    