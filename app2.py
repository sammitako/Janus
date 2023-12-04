from flask import Flask
app = Flask(__name__)
 
@app.route('/')
def hello_name():
   print("asdfsaf")
   return 'Hello !'
 
if __name__ == '__main__':
   app.run(port=3000)