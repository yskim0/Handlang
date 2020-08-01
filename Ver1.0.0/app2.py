from flask import Flask, url_for, render_template, Response, request, redirect, g, session
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model
import numpy as np
import cv2
import json
import random
from flask_babel import Babel, gettext
from datetime import datetime
import os

app = Flask(__name__)
babel = Babel(app)


app.config['lang_code'] = ['en', 'ko']

model = load_model('model/handlang_model_4.h5')
model2 = load_model('model/su_adamax.h5')
print("Loaded model from disk")


# crop_img 엉키지 않게
class Microsecond(object):
    def __init__(self):
        dt = datetime.now()
        self.microsecond = dt.microsecond

    
    def get_path_name(self):
        return 'model/' + str(self.microsecond)

crop_img_origin_path = Microsecond()
default_img = cv2.imread('model/crop_img.jpg')

# 새로운 폴더 만들기!
try:
    if not(os.path.isdir(crop_img_origin_path.get_path_name())):
        os.makedirs(os.path.join(crop_img_origin_path.get_path_name()))
except OSError as e:
    if e.errno != errno.EEXIST:
        print("Failed to create directory!!!!!")
        raise

# make directory
origin_path = crop_img_origin_path.get_path_name() + '/crop_img.jpg'
cv2.imwrite(origin_path, default_img)


class Models:
    def __init__(self,label,letter_list):
        self.__label=label
        self.__letter_list=letter_list
    
    def get_label(self,idx):
        # label = ["A", "B", "C", "D", "E", "F", "G",
        #     "H", "I", "K", "L", "M", "N", "O", "P", "Q",
        #     "R", "S", "T", "U", "V", "W", "X", "Y",
        #     "del", "nothing", "space"]
        return self.__label[idx]
    def get_letter_list(self):
        # alphabet_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o',
        #              'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y']
        return self.__letter_list
    def letter_list_idx(self,element):
        next_topic = ""
        previous_topic = ""
        letter_list=self.__letter_list
        list_idx_end = len(letter_list) - 1  # 마지막 인덱스
        idx_now = letter_list.index(element)
        if idx_now == list_idx_end:
            next_topic = letter_list[0]
        else:
            next_topic = letter_list[idx_now + 1]
        if idx_now != 0:
            previous_topic = letter_list[idx_now - 1]
        return next_topic, previous_topic
alphabet_label=["A", "B", "C", "D", "E", "F", "G",
             "H", "I", "K", "L", "M", "N", "O", "P", "Q",
            "R", "S", "T", "U", "V", "W", "X", "Y",
            "del", "nothing", "space"]
alphabet_list=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o',
                      'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y']

number_label = ["0","1","2","3","4","5","6","7","8","9","del", "nothing", "space"]
number_list = ['0','1','2','3','4','5','6','7','8','9']
alphabet_model=Models(alphabet_label,alphabet_list)
number_model= Models(number_label, number_list) 


def get_model(language):
    if language=="alphabet":
        return alphabet_model
    if language=="number":
        return number_model

# ** 전역변수 대신 클래스 객체 사용
class PredictLabel(object):
    def __init__(self, label):
        self.label = label

    def set_label(self, label):
        self.label = label

    def get_label(self):
        return self.label

class Target_idx(object):
    def __init__(self, idx):
        self.idx = idx

    def set_idx(self, idx):
        self.idx = idx

    def get_idx(self):
        return self.idx

target_idx = Target_idx(0)
predict_label = PredictLabel('')

# YS ==> number SL
target_idx2 = Target_idx(0)

@app.before_request
def before_request():
    g.total_q = 5

@babel.localeselector
def get_locale():
    try:
        language = session['language']
    except KeyError:
        language = None
    if language is not None:
        return language
    session['language']=request.accept_languages.best_match(['en', 'ko'])

    return request.accept_languages.best_match(['en', 'ko'])


def gen(camera):
    if not camera.isOpened():
        raise RuntimeError("Could not start camera")

    model = load_model('model/handlang_model_4.h5')

    while True:
        success, img = camera.read()
        if success:
            try:
                
                cv2.rectangle(img, (250,250), (600,600), (000,51,51), 2)

                crop_img = img[250:600, 250:600]
                crop_img_path = crop_img_origin_path.get_path_name() + '/crop_img.jpg'
                cv2.imwrite(crop_img_path, crop_img)
                # # print(crop_img)
                # result = model_predict()
                image = load_img(crop_img_path, target_size=(64,64))
                image = img_to_array(image)
                image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))

                prediction = model.predict(image)

                target_idx_for_predict = target_idx.get_idx()
                print("타겟예측: ", prediction[0][target_idx_for_predict])

                if np.argmax(prediction[0]) == 1:
                    result = alphabet_model.get_label(np.argmax(prediction[0]))

                elif prediction[0][target_idx_for_predict] > 0: 
                    result = alphabet_model.get_label(target_idx_for_predict)
                else:
                    result = ''

                predict_label.set_label(result)

                ret, jpeg = cv2.imencode('.jpg', crop_img)
                frame = jpeg.tobytes()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            except:
                print("An exception occurred")

        else:
            print("Status of camera.read()\n", success, "\n=======================")

# YS =====> for number SL
def gen2(camera):
    if not camera.isOpened():
        raise RuntimeError("Could not start camera")

    model2 = load_model('model/su_adamax.h5')

    while True:
        success, img = camera.read()
        # print(success, img)

        if success:
            try:

                cv2.rectangle(img, (250, 250), (600, 600), (000, 51, 51), 2)

                crop_img = img[250:600, 250:600]
                crop_img_path = crop_img_origin_path.get_path_name() + '/crop_img2.jpg'
                cv2.imwrite(crop_img_path, crop_img)
                # print("===============")
                # print(crop_img)
                # result = model_predict()
                image = load_img(crop_img_path, target_size=(64, 64))
                image = img_to_array(image)
                image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
                # print("===============")
                prediction = model2.predict(image)
                # print("===============")
                target_idx_for_predict = target_idx2.get_idx()
                # print("===============")
                print("타겟예측: ", prediction[0][target_idx_for_predict])
                # print("===============")
                if np.argmax(prediction[0]) == 1:
                    result = number_model.get_label(np.argmax(prediction[0]))

                elif prediction[0][target_idx_for_predict] > 0:
                    result = number_model.get_label(target_idx_for_predict)
                else:
                    result = ''
                # print("===============")
                predict_label.set_label(result)
                # print("===============")
                ret, jpeg = cv2.imencode('.jpg', crop_img)
                frame = jpeg.tobytes()
                # print("===============")
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            except:
                print("An exception occurred")

        else:
            print("Status of camera.read()\n", success, "\n=======================")


def make_quiz(group):
    question_list = {}
    img_list = []
    for i in range(g.total_q):
        question, examples, img = make_random_quiz(question_list,group)
        question_list[question] = examples
        img_list.append(img)
    return question_list, img_list


def make_random_quiz(question_list,group):
    #here
    modeltype=get_model(group)
    alphabet_list = modeltype.get_letter_list()
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
    # 띄어쓰기 조심!@!
    label_list = [" A ", " B ", " C ", " D ", " E ", " F ", " G ",
            " H ", " I ", " J ", " K ", " L ", " M ", " N ", " O ", " P ", " Q ", 
            " R ", " S ", " T ", " U ", " V ", " W ", " X ", " Y ", " Z ", 
            " del ", " nothing ", " space "]
    tem = label_list.index(value)
    print(tem)
    idx = target_idx.set_idx(tem)
    print(idx)
    label = " " + predict_label.get_label() + " "

    # ajax 에서 값 받아올때 공백이 앞뒤로 붙는데 python strip() 함수가 안먹어서...

    if label == '':
        predict_result = {
            'status': 0,
            'info': 'not detected',
            'label': '',
            'lang_code': session['language']
        
        }
    elif label != value:
        predict_result = {
            'status': 0,
            'info': gettext('predict_incorrect'),
            'label': label,
            'lang_code': session['language']

        }
        print("틀림!")
    else:
        predict_result = {
            'status': 1,
            'info': gettext('predict_correct'),
            'label': label,
            'lang_code': session['language']
        }

    # result 의 status 값이 1이면 참 -> main.js 에서 correct 값 증가

    json_data = json.dumps(predict_result)  # json 형태로 바꿔줘야 에러 안남
    return json_data


# YS
@app.route('/return_label2', methods=['POST', 'GET'])
def return_label2():
    value = request.form.get("target", False)
    # 띄어쓰기 조심!@!
    label_list = [" 0 ", " 1 "," 2 ", " 3 ", " 4 ", " 5 ", " 6 ", " 7 ", " 8 ", " 9 ", " del ", " nothing ", " space "]
    tem = label_list.index(value)
    print(tem)
    idx = target_idx2.set_idx(tem)
    print(idx)
    label = " " + predict_label.get_label() + " "

    # ajax 에서 값 받아올때 공백이 앞뒤로 붙는데 python strip() 함수가 안먹어서...

    if label == '':
        predict_result = {
            'status': 0,
            'info': 'not detected',
            'label': '',
            'lang_code': session['language']

        }
    elif label != value:
        predict_result = {
            'status': 0,
            'info': gettext('predict_incorrect'),
            'label': label,
            'lang_code': session['language']

        }
        print("틀림!")
    else:
        predict_result = {
            'status': 1,
            'info': gettext('predict_correct'),
            'label': label,
            'lang_code': session['language']
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


@app.route('/quiz/<group>', methods=['GET', 'POST'])
def quiz(group):
    
    if request.method == 'GET':
        question_list, img_list = make_quiz(group)
        return render_template('quiz.html', group=group,str=str, enumerate=enumerate, question_list=question_list,
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

        return redirect(url_for('.quiz_result',group=group, user_answers=user_answers))


# 퀴즈 결과
@app.route('/quiz/<group>/result')
def quiz_result(group):
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
    return render_template('result.html', group=group, correct_num=correct_num, incorrect_questions=incorrect_questions,
                           total_q=g.total_q, img_path=img_path, link=request.full_path)


@app.route('/practice_asl')
def practice_asl():
    alphabet_list = alphabet_model.get_letter_list()
    return render_template('practice_asl.html', alphabet_list=alphabet_list, link=request.full_path)

# YS
@app.route('/practice_num')
def practice_num():
    number_list = number_model.get_letter_list()
    return render_template('practice_num.html', number_list=number_list, link=request.full_path)
# YS

# video streaming
@app.route('/video_feed')
def video_feed():
    camera = cv2.VideoCapture(0)
    return Response(gen(camera), mimetype='multipart/x-mixed-replace; boundary=frame')

# YS video streaming
@app.route('/video_feed2')
def video_feed2():
    camera = cv2.VideoCapture(0)
    return Response(gen2(camera), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/practice', methods=['GET', 'POST'])
def practice():
    element = request.args.get('element')
    alphabet = element.upper()
    img = "../static/img/asl_" + element + ".png"

    next_topic, previous_topic = alphabet_model.letter_list_idx(element)

    return render_template('practice.html', img=img, alphabet=alphabet, previous_topic=previous_topic,
                           next_topic=next_topic, link=request.full_path)

@app.route('/practice2', methods=['GET', 'POST'])
def practice2():
    element = request.args.get('element')
    number = element
    img = "../static/img/asl_" + element + ".png"

    next_topic, previous_topic = number_model.letter_list_idx(element)

    return render_template('practice2.html', img=img, number=number, previous_topic=previous_topic,
                           next_topic=next_topic, link=request.full_path)

@app.route('/')
def index():
    return render_template('index.html', link=request.full_path)


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port=5000, debug=True)