## Handlang-contour image+original image로 training

- 투빅스의 [DeepKSL (YOLO를 이용한 한국 수화 번역)](http://www.datamarket.kr/xe/44513)에서 model을 training 시킬때 사용한 방법처럼 우리도 hand contour img를 함께 트레이닝 시켜본다면?
- ![DeepKSL_ 최종-10.jpg](C:\Users\user\Desktop\new_2020study\Handlang\img\투빅스.JPG)

현재 우리의 모델

![image-20200322135139793](C:\Users\user\Desktop\new_2020study\Handlang\img\model.jpg)



우리는 Web상에서 hand를 detect하고 들어오기 때문에 투빅스처럼 모델을 2개를 training시킬 필요가 없음

우리가 집중하는 모델은 **지문자를 detect하는 모델**!



- 현재까지 트레이닝왼 weight는 그대로 두고, 추가 학습을 contour이미지와 함께 학습시켜본다면?
- 관련 논문을 리뷰해보고 확실히 성능 개선의 여지가 있을때 contour이미지와 함께 학습을 진행시켜보기로 함



##### 전처리 과정은 어떻게 되나 (contour를 어떻게 따나)

- 잡영제거 과정을 따르면 된다

- https://d2.naver.com/helloworld/8344782

  이미지 --> 흑백처리 --> Morph Gradient --> Morph Close --> detection에 방해되는 요소 제거 --> Contour 추출

- 위 과정 중 우리의 이미지로 흑백처리만 하고 contour 추출했을 때

  <img src="C:\Users\user\Desktop\new_2020study\Handlang\img\contoured img_1.png" alt="image-20200322140157039" style="zoom: 80%;" /> 

​       <img src="C:\Users\user\Desktop\new_2020study\Handlang\img\contoured img_2.png" alt="image-20200322140209553" style="zoom:25%;" /> 



- **위에 말한 것처럼 성능 개선의 가능성이 보면 추가적인 잡영처리 후 contour 추출한 이미지와 original 이미지를 함께 training 시켜볼 예정이다.**

