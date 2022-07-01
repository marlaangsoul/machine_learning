# app01.py
from flask import Flask, request, render_template
from sklearn import svm
import joblib

app = Flask(__name__)

# 판정하기
def detect_lang(text):
    # 학습 데이터 읽어 들이기
    pklfile = 'data/freq.pkl'
    clf = joblib.load(pklfile)

    # 알파벳 출현 빈도 구하기
    text = text.lower()
    code_a, code_z = (ord("a"), ord("z"))
    cnt = [0 for i in range(26)]
    for ch in text:
        n = ord(ch) - code_a
        if 0 <= n < 26: cnt[n] += 1
    total = sum(cnt)
    if total == 0: return "입력이 없습니다"
    freq = list(map(lambda n: n/total, cnt))
    # 언어 예측하기
    res = clf.predict([freq])
    # 언어 코드를 한국어로 변환하기
    lang_dic = {"en":"영어","fr":"프랑스어",
        "id":"인도네시아어", "tl":"타갈로그어"}
    return lang_dic[res[0]]

@app.route('/')
def index():
    return render_template('lang_result.html')
@app.route('/result',methods=['post'])
def result():
    data = request.form['data']
    lang = detect_lang(data)
    return render_template('lang_result.html',result=lang)


if __name__ == '__main__':
    app.run(debug=True)