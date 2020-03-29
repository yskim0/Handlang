from flask import Flask, url_for, render_template, Response, request, redirect, g, session
from darkflow.net.build import TFNet
import cv2
import tensorflow as tf
import json
import random
from flask_babel import Babel, gettext


app = Flask(__name__)
babel = Babel(app)

options = {"model": "cfg/yolo.cfg", "load": "bin/yolo.weights", "threshold": 0.4}

tfnet = TFNet(options)
app.config['lang_code'] = ['en', 'ko']


# ** 전역변수 대신 클래스 객체 사용
class PredictLabel(object):
    def __init__(self, label):
        self.label = label

    def set_label(self, label):
        self.label = label

    def get_label(self):
        return self.label


predict_label = PredictLabel('')

# **


@app.before_request
def before_request():
    g.total_q = 10


@babel.localeselector
def get_locale():
    try:
        language = session['language']
    except KeyError:
        language = None
    if language is not None:
        return language
    return request.accept_languages.best_match(['en', 'ko'])


def get_alphabet_list():
    alphabet_list = ['person', 'teddybear', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                     'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    return alphabet_list


def alphabet_list_idx(element):
    next_topic = ""
    previous_topic = ""

    alphabet_list = get_alphabet_list()

    list_idx_end = len(alphabet_list) - 1  # 마지막 인덱스
    idx_now = alphabet_list.index(element)

    if idx_now == list_idx_end:
        next_topic = alphabet_list[0]
    else:
        next_topic = alphabet_list[idx_now + 1]

    if idx_now != 0:
        previous_topic = alphabet_list[idx_now - 1]

    return next_topic, previous_topic


def gen(camera):
    if not camera.isOpened():
        raise RuntimeError("Could not start camera")

    sess = tf.Session()

    with sess.as_default():

        while True:

            success, img = camera.read()

            if success:
                try:
                    results = tfnet.return_predict(img)

                    for result in results:
                        tl = (result['topleft']['x'], result['topleft']['y'])
                        br = (result['bottomright']['x'], result['bottomright']['y'])
                        label = result['label']
                        confidence = result['confidence']

                        cv2.rectangle(img, tl, br, (0, 255, 0), 3)
                        cv2.putText(img, label, br, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)

                        predict_label.set_label(label)

                    ret, jpeg = cv2.imencode('.jpg', img)
                    frame = jpeg.tobytes()

                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                except:
                    print("An exception occurred")

            else:
                print("Status of camera.read()\n", success, "\n=======================")


def make_quiz():
    question_list = {}
    img_list = []
    for i in range(g.total_q):
        question, examples, img = make_random_quiz(question_list)
        question_list[question] = examples
        img_list.append(img)
    return question_list, img_list


def make_random_quiz(question_list):
    alphabet_list = get_alphabet_list()
    examples = []  # 보기
    while True:
        answer = alphabet_list[random.randint(0, len(alphabet_list) - 1)]
        if is_valid_quiz(answer, question_list):
            break
    examples.append(answer)
    while len(examples) != 4:
        randomIndex = random.randint(0, len(alphabet_list) - 1)
        if alphabet_list[randomIndex] not in examples:
            examples.append(alphabet_list[randomIndex])
    random.shuffle(examples)
    img = []
    for i in examples:
        img.append('../static/img/asl_' + i + ".png")

    return answer, examples, img


# 이전에 낸 문제인지 확인
def is_valid_quiz(answer, question_list):
    if answer in question_list:
        return False
    else:
        return True


# for ajax
@app.route('/return_label', methods=['POST', 'GET'])
def return_label():
    value = request.form.get("target", False)

    label = predict_label.get_label()
    label = " " + label.upper() + " "  # ajax 에서 값 받아올때 공백이 앞뒤로 붙는데 python strip() 함수가 안먹어서 일단 임시방편으로

    if label == '':
        predict_result = {
            'status': 0,
            'info': 'not detected',
            'label': ''
        }
    elif label != value:
        predict_result = {
            'status': 0,
            'info': gettext('predict_incorrect'),
            'label': label
        }
        print("틀림!")
    else:
        predict_result = {
            'status': 1,
            'info': gettext('predict_correct'),
            'label': label
        }

    # result 의 status 값이 1이면 참 -> main.js 에서 correct 값 증가

    json_data = json.dumps(predict_result)  # json 형태로 바꿔줘야 에러 안남
    return json_data


# for ajax
@app.route('/english')
def english():
    session['language'] = 'en'
    link = request.args.get('link')
    if link:
        return redirect(link)
    else:
        return redirect('/')


# for ajax
@app.route('/korean')
def korean():
    session['language'] = 'ko'
    link = request.args.get('link')
    if link:
        return redirect(link)
    else:
        return redirect('/')


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'GET':
        question_list, img_list = make_quiz()
        return render_template('quiz.html', str=str, enumerate=enumerate, question_list=question_list,
                               img_list=img_list, total_q=g.total_q, link=request.full_path)

    if request.method == 'POST':
        user_answers = {}
        for i in range(g.total_q):
            question = "question" + str(i)
            answer = "answer" + str(i)
            q = request.form[question]
            a = request.form[answer]
            user_answers[q] = a
            print(user_answers)
        user_answers = json.dumps(user_answers)

        return redirect(url_for('.quiz_result', user_answers=user_answers))


# 퀴즈 결과
@app.route('/quiz/result')
def quiz_result():
    try:
        user_answers = json.loads(request.args['user_answers'])
        items = user_answers.items()
    except:
        user_answers = {}
    items = user_answers.items()
    correct_num = 0
    incorrect_questions = []
    for q, a in items:
        if (q == a):
            correct_num += 1
        else:
            incorrect_questions.append(q.upper())
    if correct_num == g.total_q:
        img_path = "../static/img/score_100.png"
    elif correct_num >= (g.total_q // 2):
        img_path = "../static/img/score_50.png"
    else:
        img_path = "../static/img/score_0.png"
    return render_template('result.html', correct_num=correct_num, incorrect_questions=incorrect_questions,
                           total_q=g.total_q, img_path=img_path, link=request.full_path)


@app.route('/aboutUs')
def aboutUs():
    return render_template('aboutUs.html', link=request.full_path)


@app.route('/practice_asl')
def practice_asl():
    alphabet_list = get_alphabet_list()
    return render_template('practice_asl.html', alphabet_list=alphabet_list, link=request.full_path)


# video streaming
@app.route('/video_feed')
def video_feed():
    camera = cv2.VideoCapture(0)
    return Response(gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/practice', methods=['GET', 'POST'])
def practice():
    element = request.args.get('element')
    alphabet = element.upper()
    img = "../static/img/asl_" + element + ".png"

    next_topic, previous_topic = alphabet_list_idx(element)

    return render_template('practice.html', img=img, alphabet=alphabet, previous_topic=previous_topic,
                           next_topic=next_topic, link=request.full_path)


@app.route('/')
def index():
    return render_template('index.html', link=request.full_path)


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port=5000, debug=True)