# web/app.py
from flask import Flask, request, render_template
from sklearn import svm
import pickle

app = Flask(__name__)

def detect_lang(text):
    fname = './model/lang.pickle'
    with open(fname, 'rb') as f:
        clf = pickle.load(f)

    text = text.lower()
    cnt = [0 for n in range(0,26)]
    code_a = ord('a') # 97 문자==> 아스키코드
    code_z = ord('z') #
    for ch in text:
        n = ord(ch)
        if code_a <= n <= code_z:
            cnt[n - code_a] += 1 # 98 - 97
        #print(cnt)
    total = sum(cnt)
    freq = list(map(lambda n: n/total, cnt)) # 정규화,scale

    res = clf.predict([freq])
    lang_dic = {
    'en':'영어','fr':'프랑스어',
    'id':'인도네시아','tl':'타갈로어'
    }
    return lang_dic[res[0]]

@app.route('/')
def index():
    return render_template('result.html')

@app.route('/result', methods=['post'])
def result():
    data = request.form['data']
    lang = detect_lang(data)
    return render_template('result.html',result=lang)

if __name__ == '__main__':
    app.run(debug=True)
