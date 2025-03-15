# 사전 설치 : pip install flask pymysql
from flask import Flask, render_template, request, redirect, url_for
from score import scoreCalculator
from db import Database
import atexit

app = Flask(__name__)
db = Database()

# 애플리케이션 종료 시 DB 연결 종료
atexit.register(db.close)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        gender  = int(request.form['gender'])
        age  = int(request.form['age'])
        content  = request.form.get('content','')
        question1 = int(request.form.get('question1',0))
        question2 = int(request.form.get('question2',0))
        question3 = int(request.form.get('question3',0))
        question4 = int(request.form.get('question4',0))
        question5 = int(request.form.get('question5',0))
        
        # score 계산
        calculator = scoreCalculator(question1, question2, question3, question4, question5)
        result = calculator.get_result()
        
        # 데이터베이스에 저장
        db.save_score_record(gender,age, question1,question2,question3,question4,question5,content,result["score"])
        
        return render_template('result.html', 
                              gender=gender,
                              age=age,
                              score=result["score"],
                              question1=result["question1"],
                              question2=result["question2"],
                              question3=result["question3"],
                              question4=result["question4"],
                              question5=result["question5"],
                              )
    except ValueError:
        return render_template('index.html', error="유효한 정보를 입력해주세요.")

@app.route('/delete', methods=['POST'])
def delete():
    try:
        # 선택된 설문 번호 가져오기
        selected_nos = request.form.getlist('no')  # 체크박스의 선택된 값들
        if not selected_nos:
            return render_template('history.html', error="삭제할 설문 기록을 선택하세요.")
        
        # 삭제 처리
        for no in selected_nos:
            db.delete_score_record(int(no))  # 각 번호에 대해 삭제

        # 삭제 후 데이터 조회
        records = db.get_survey_records()  # get_survey_records()는 모든 설문 데이터를 가져오는 함수
        
        return render_template('history.html', message="선택된 설문 기록이 성공적으로 삭제되었습니다.", records=records)
    except Exception as e:
        return render_template('history.html', error=f"삭제 중 오류 발생: {e}")


@app.route('/history')
def history():
    # 최근 survey_records 기록 10개 가져오기
    records = db.get_survey_records(10)
    return render_template('history.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)