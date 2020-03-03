# Handlang

## DSC Ewha

- training시 사용한 데이터
  
- 0-9/a-z: https://www.kaggle.com/ayuraj/american-sign-language-dataset
  
  - 위의 data 中 각 label당 200개씩을 training시 사용
  
- test시 사용한 데이터 -->**test_data/Test_Data**

   - 0~9 : https://github.com/ardamavi/Sign-Language-Digits-Dataset

     ​        : 위의 data 中 각 label당 100개씩을 training시 사용

   - a~z  : https://www.kaggle.com/ayuraj/american-sign-language-dataset
   
     ​        (american sign language data에서 200개는 training data로, 100개는 test data로 사용)



* a-z test 결과

  : 총 2600개 data 중 1312개만 잘 detect함..!![img_readme/"test result"](C:\Users\user\Desktop\Handlang\ML\img_readme\test result.png)

​       : 아무런 전처리를 하지 않은 상태에서 50%정도의 정확도가 나옴