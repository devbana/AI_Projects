from flask import Flask,request,jsonify, render_template
import spacy
import os
app = Flask(__name__)
nlp_new = spacy.load(os.getcwd())
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/getdata',methods=['POST'])
def getdata():
    vari = [ x for x in request.form.values()]
    resul = [str(i) for i in nlp_new(vari[0]).ents]
    res = ' '.join(resul)
    res1 = 'The tweet "{}", important keywords are "{}"'.format(str(vari[0]),res)
    print(os.getcwd())
    return render_template("index.html",prediction_text=res1)


if  __name__ == "__main__":
    app.run(debug=False)

