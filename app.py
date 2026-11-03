from flask import Flask, render_template

app = Flask(__name__)

# 기본 도메인 접속 시 실행될 라우트
@app.route('/')
def home():
    # templates 폴더 안의 index.html 파일을 웹 브라우저에 띄워줍니다.
    return render_template('index.html')

if __name__ == '__main__':
    # debug=True: 코드를 수정하고 저장하면 서버가 자동으로 재시작되어 편리합니다.
    app.run(debug=True, host='0.0.0.0', port=5000)