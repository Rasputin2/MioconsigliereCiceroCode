from flask import Flask, render_template, url_for, flash, redirect, request
from .forms import getSection
from .forms import proceedNowTo86
from .forms import proceed86to39
from .forms import proceed39toPrior
from .forms import proceedToNewSearch
from .ciceroFunctions import*

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aaa'

@app.route('/')
def test():
    return 'Hello World!'
    
@app.route('/getsec/', methods = ['GET', 'POST'])
def getsec():
    form = getSection()
    if form.validate_on_submit():
        formsection = request.form['codesection']
        return redirect(url_for('text', userInput = formsection))
    return render_template('getSection.html', title = 'getsec', form = form)

@app.route('/text/<userInput>', methods = ['GET', 'POST'])
def text(userInput):
    textOfsection = ciceroFunctions.getText(userInput) 
    if textOfsection == "Error":
        textOfSection = "We didn't find your section.  Please check your entry and try again."
    form = proceedNowTo86()
    if form.validate_on_submit():
        return redirect(url_for('to86', userInput = userInput))
    return render_template('text.html', sectionText = textOfsection, form=form)

@app.route('/to86/<userInput>', methods = ['GET', 'POST'])
def to86(userInput):
    analysis = userInput
    form = proceed86to39()
    if form.validate_on_submit():
        return redirect(url_for('to39', userInput = userInput))
    return render_template('to86.html', analysis = analysis, form = form)

@app.route('/to39/<userInput>', methods = ['GET', 'POST'])
def to39(userInput):
    analysis = MapTo39(userInput)
    newform = proceed39toPrior()
    if newform.validate_on_submit():
        return redirect(url_for('toPrior', userInput = userInput))
    return render_template('from86to39.html', analysis = analysis, form = newform) 

@app.route('/toPrior/<userInput>', methods = ['GET', 'POST'])
def toPrior(userInput):
    analysis = Map39toPrior(userInput)
    returnform = proceedToNewSearch()
    if returnform.validate_on_submit():
        return redirect(url_for('getsec'))
    return render_template('toPrior.html', analysis = analysis, form = returnform)


