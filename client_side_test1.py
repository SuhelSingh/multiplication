from flask import Flask, render_template, make_response, request, url_for, redirect
import random
import time
import multiplication as m

# holds starting and ending time of each problem
timing_session = []
session_data = []
m.initialize()

app = Flask(__name__)
# ***** ANSWER SENDING AND RECEIVING FUNCTIONS FOR ALL TESTS *****
# sends 2 numbers to client
@app.route('/newNumbers/')
def newNumbers():
    timing_session.append(time.clock())
    (a,b) = m.selectNumbers()
    response = make_response('{"1": %d, "2": %d}' % (a,b))
    response.headers['Content-Type'] = 'application/json'
    print 'sent new numbers'
    return response
@app.route('/receiveAnswers/', methods=["POST"])
def receiveAnswers():
    timer = time.clock() - timing_session[-1]
    data = request.json
    data['time'] = timer
    session_data.append(data)
    print 'recieved answers'
    return ('',204)
# writes data for each problem to a dataframe
@app.route('/sendAnswers/')
def sendAnswers():
    # flash message test completed, results too eventually
    # *** m.write_session_to_dataframe() ***
    print session_data
    del session_data[:]
    print 'sendAnswers pinged, writing data to file'
    return ('',204)
# when user is done, send all sessions to server
@app.route('/DataToServer/')
def data_to_server():
    print 'all session datas sent to server'
    return ('',204)
    # m.send_all()
# ***** END SHARED FUNCTIONS *****

# ***** START TIMED TEST ******
@app.route('/timedTest/')
def timed_test():
    return render_template('timedtest1.html')
# ***** END TIMED TEST *****

# ***** START PRACTICE MODE *****
@app.route('/practice/')
def practice():
    return render_template('practicemode1.html')
# ***** END PRACTICE MODE *****

# *** landing page to choose test***
@app.route('/')
def landing():
    # eventually this will have a login page also
    return render_template('landingpage1.html')

if __name__=='__main__':
    app.run(debug=True)
