from flask import Flask, request
app = Flask(__name__)

@app.route("/inbound", methods=['POST'])
def get_attachment():
    data = request.form['text']
    print data
    of = open('simpredResults.txt', 'w')
    of.write(data)
    of.close()
    return 'OK'


if __name__ == "__main__":
    app.run()
