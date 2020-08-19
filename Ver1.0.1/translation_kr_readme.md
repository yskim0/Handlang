**It is a Korean translation of readme.md**

-----
# DSC Solution Challenge

## Handlang - ASL(American Sign Language) Education by using deep learning model

<br>

## 앞서...

우리 나라에 맞는 모델을 만들고 싶었으나, 데이터셋이 없어서 영어 수화(asl)을 사용했다는 점에 대해 미리 사과드립니다.

우리는 이 프로젝트를 향후 추진해나갈 의지가 있으며, 한국어 수어의 데이터 셋 확보를 최우선 목표로 할 것입니다.

## 프로젝트 목적

우리 사회는(적어도 대한민국은) 수어 교육이 매우 열악한 상태입니다.

청각 장애인들을 비롯하여 수화가 필요한 이들에게, 수화는 세계 보통의 언어처럼 자신의 세계를 세상을 표현할 수 있게 만들어주는 도구입니다.
하지만 현재 제공되고 있는 교육은 그 기대에 상응하지 않습니다.


우리는 기술을 통해 청각 장애인들을 비롯하여 수화가 필요한 이들에게 수화 교육을 제공함으로써 사회적 장벽을 허물 수 있습니다.

또한 지금은 ASL(영어 수어)에만 제한되어 있지만, 다른 나라의 수화 데이터셋과 충분한 시간을 가지게 된다면 여러 나라에 맞는 모델을 만들 것입니다. 이를 통해 세계의 더 많은 사람들이 사용할 수 있을 것입니다. 

**돈, 환경 등 어떠한 제약도 받지 않는, 모든 사람들이 사용할 수 있는 수화 교육을 만드는 것이 우리가 고른 challenge입니다.**

우리의 모델은 사람의 교육에 미치지는 못하겠지만 수화 교육 분야에서의 발전 필요성을 상기시킬 것입니다.

또한 우리는 기술을 통해 세상을 좋은 곳으로 바꿀 수 있다는 것을 보여주고 싶습니다.

우리의 프로젝트로 사람들이 수화 교육에 관심을 가지게 되어 우리 아이디어를 더 발전시킬 수 있는 계기가 되면 좋겠습니다.


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

## 우리가 선택한 구글의 기술

1. Google Cloud Platform(GCP)
: Computer Engine - GPU

- 모델을 트레이닝시킬 때 필요한 GPU
    - GCP GPU는 우리 딥러닝 모델을 트레이닝 할 때 큰 도움이 됐음.
    - Gcp에서 우리는 gpu 수와 무슨 gpu를 사용할지 커스터마이즈 할 수 있었음.
    - 게다가, gcp가 예상 비용을 계산해주어 우리가 계획하는 데에 도움을 줌.

- 팀적으로 관리하기 좋은 클라우드 서버
    - 팀 안에서 공유할 수 있는 서버이기 때문에 로컬 서버에서 관리할 때 보다 팀적으로 용이했음.

2. Tensorflow
: 딥러닝 모델에 사용했음.

- 머신러닝 플랫폼 중 최고라고 생각하기때문
- 솔루션 챌린지 이전에 팀원들이 다같이 공부했음.
- 딥러닝에 관련된 여러 API 제공됨
    - 이를 통해 여러 실험들을 할 수 있었음. (inception-v3, fast-rcnn, custom CNN model)

<br>

## 실행 방법

1. 이 저장소를 다운로드 받는다.

`git clone https://github.com/yskim0/DSC_Solution_Challenge.git`

2. requirements를 설치한다.

저희 팀은 아나콘다 가상환경 하에 모든 과정을 진행했습니다. 따라서 가상 환경 아래에 진행하기를 추천합니다.

- 첫 번째 step에서 저장했던 폴더로 이동한다.

`cd GoogleSolutionChallenge_Handlang`

- install requirements

`pip install -r requirements.txt`

3. Run!

Run `python app.py` or `python3 app.py`

설치가 완료되었습니다.
이제 `http://0.0.0.0:5000/` 를 가셔서 프로젝트를 즐겨 보세요!

![homepage](/img/homepage.png)


<br>

## 유저 피드백 받기 전 딥러닝 모델들

유저로부터 받은 피드백은 주로 모델의 예측 정확도에 관련한 것들이었기 때문에 모델 성능 향상을 우선으로 했습니다.

딥러닝 모델 관련하여 여러가지 시도를 했는데 이는 링크를 타고 들어가면 볼 수 있습니다.


[피드백 받기 전후 시도들](https://github.com/yskim0/GoogleSolutionChallenge_Handlang/blob/master/before_usr_feedback.md)

<br>


## 향후 계획

어떤 조언이든 환영합니다.

- 딥러닝 모델 
    - 전처리와 다양한 데이터셋을 학습시켜 성능을 향상 시킬 것
    - 숫자(0~9) 라벨 추가
    - 여건(e.g dataset)이 된다면 KSL 모델 생성

- web page
    - UI/UX를 더 깔끔하게 만들 것


<br>

## Team Handlang

- 김연수 : 이화여자대학교
- 
- 
- 


