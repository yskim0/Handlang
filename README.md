# Handlang - ASL(American Sign Language) Education by using deep learning model

## DSC Ewha

<br>

딥러닝으로 학습된 수화 인식 모델을 바탕으로 알파벳, 숫자에 해당되는 수화를 학습 및 연습 할 수 있는 웹 어플리케이션입니다.


## Requirements

```
flask
numpy
matplotlib
tensorflow==1.15.2
opencv-python-headless
cython
Pillow
flask_babel
keras
```

## Datasets

아래 데이터 셋들은 모델 트레이닝에 사용되었습니다.

참고로, 우리 모델에서는 알파벳 `i,z` 제외했습니다. (손동작이 포함되었기 때문에)

- https://www.kaggle.com/grassknoted/asl-alphabet
    - 가장 성능이 좋은 모델에 사용된 데이터 셋입니다.

<br>

다른 모델에서는 아래의 데이터셋들을 사용했습니다.

- https://www.kaggle.com/rajarshighoshal/asltestimages
- https://www.kaggle.com/muhammadkhalid/sign-language-for-alphabets
- https://www.kaggle.com/ayuraj/asl-dataset


## 실행 방법

1. 이 저장소를 다운로드 받는다.

`git clone https://github.com/yskim0/Handlang.git`

2. requirements를 설치한다.

저희 팀은 아나콘다 가상환경 하에 모든 과정을 진행했습니다. 따라서 가상 환경 아래에 진행하기를 추천합니다.

- 첫 번째 step에서 저장했던 폴더로 이동한다.

`cd Handlang/Ver1.0.1`

- install requirements

`pip install -r requirements.txt`

3. Run!

Run `python app.py` or `python3 app.py`

설치가 완료되었습니다.
이제 `http://0.0.0.0:5000/` 를 가셔서 프로젝트를 즐겨 보세요!

![home-page](https://user-images.githubusercontent.com/48315997/90604151-60015480-e237-11ea-8092-65387889b31d.png)



<br>

### 유저 피드백 받기 전 딥러닝 모델들

유저로부터 받은 피드백은 주로 모델의 예측 정확도에 관련한 것들이었기 때문에 모델 성능 향상을 우선으로 했습니다.

딥러닝 모델 관련하여 여러가지 시도를 했는데 이는 링크를 타고 들어가면 볼 수 있습니다.


[피드백 받기 전후 시도들](https://github.com/yskim0/GoogleSolutionChallenge_Handlang/blob/master/before_usr_feedback.md)

<br>




## Team Handlang

- 김연수 : Ewha w.univ.
    - [Github](https://github.com/yskim0)
- 신지영 : Ewha w.univ.
    - [Github](https://github.com/Turtlefromocean)
- 서현주 : Ewha w.univ.
    - [Github](https://github.com/seohsj)
- 손수현 : Ewha w.univ.
    - [Github](https://github.com/sonsuhyune)

