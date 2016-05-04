from flask import Flask, render_template, make_response, request, url_for, redirect
import requests
import json
import random
import time
# holds starting and ending time of each problem
# eventually move all timing to client side but this is easier for a prototype
timing_session = []
session_data = []
# *** landing page to start test ***
app = Flask(__name__)
@app.route('/')
def test():
    return render_template('timedtest1.html')
# *** sends 2 numbers back to client in response to json request, writes initial
# start time of each problem to list ***
@app.route('/newNumbers/')
def newNumbers():
    # want to flash message here, correct or incorrect
    timing_session.append(time.clock())
    a = random.randint(1,10)
    b = random.randint(11,99)
    response = make_response('{"1": %d, "2": %d}' % (a,b))
    response.headers['Content-Type'] = 'application/json'
    return response
# *** subtracts current time from start time, recieves problem attempted and
# whether or not it was correct, adds time to this, adds this dict to session_data
# list ***
@app.route('/receiveAnswers/', methods=["POST"])
def receiveAnswers():
    timer = time.clock() - timing_session[-1]
    data = request.json
    data['time'] = timer
    session_data.append(data)
    return ('',204)
# *** after timer in client exits test, this is pinged to write session_data to
# a file, the page is redirected back to test start from the client-side ***
@app.route('/sendAnswers/')
def sendAnswers():
    # write info to file or to sql server
    # flash message test completed, results too eventually
    print 'sendAnswers pinged, writing data to file'
    return ('',204)


if __name__=='__main__':
    app.run(debug=True)






