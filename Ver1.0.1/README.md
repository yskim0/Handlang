# DSC Solution Challenge

## Handlang - ASL(American Sign Language) Education by using deep learning model

<br>


## Before introducing our solution...


We wanted to make a model suitable for my country(South of Korea), but I am sorry that we used American Sign Language (asl) because there is no proper dataset of Korean Sign Language(KSL).

<br>

## Demo

Watch a short demo video!

[demo video](https://youtu.be/LaTwFHh8_48)

<br>

## Purpose(our target to challenge)

In our society (at least in Korea), sign language education is very poor.
For the Deaf and those in need of sign language, sign language is a tool that allows them to express their world like the any languages of the world.


However, the education currently being provided does not correspond to that expectation.

**Through technology, we can break down social barriers by providing sign language education for the deaf and those in need of sign language.**

Also, It is limited to ASL now, but if we have enough time with other countries' sign language datasets, we will create models that fit many countries. This will be available to users in the wider world.

It is our challenge to create sign language education that everyone can use, free of any restrictions such as money, environment, etc.

Our solution may not fall short of human education, but it reminds us of the need for innovation in sign language education.

We wanted to show that technology can change the world into a better place.

We hope this project will help people become interested in sign language education and further develop our ideas.

<br>

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

Datasets we used in the deep learning model.

In addition, we exclude `j,z` since they require movement.

- https://www.kaggle.com/grassknoted/asl-alphabet
    - It was used in our best model.

<br>

also, we used ... (in other models)
- https://www.kaggle.com/rajarshighoshal/asltestimages
- https://www.kaggle.com/muhammadkhalid/sign-language-for-alphabets
- https://www.kaggle.com/ayuraj/asl-dataset


## What Google technology we used

1. Google Cloud Platform(GCP)
: Computer Engine - GPU

- GPU required to train the model
    - GPU of GCP was very helpful when training our deep learning model.
    - In GCP, we can customize the number of GPU and what GPU device(e.g. Tesla k-80) be used.
    - Moreover, GCP helped us plan by calculating the expected cost.


- Cloud services that are good for a team to manage
    - It was easy to manage as a team because GCP computer engine can be shared with team members, unlike what is managed by local server.

2. Tensorflow
: deep learning model

- The best of machine learning platform
- All the team members had studied together before Solution Challenge.
- Provide many APIs related to deep learning model
    - We were able to do a lot of experiments. (inception-v3, fast-rcnn, custom CNN model)

<br>

## How to run

1. Download this repository

`git clone https://github.com/yskim0/GoogleSolutionChallenge_Handlang.git`

2. Install requirements

We proceeded under the *Anaconda environment*. We recommend to proceed in the *virtual environment.*

- Go to the downloaded folder(by step1)

`cd GoogleSolutionChallenge_Handlang`

- install requirements

`pip install -r requirements.txt`

3. Run!

Run `python app.py` or `python3 app.py`

Installation is just finished!
You can enjoy our project in `http://0.0.0.0:5000/`

+) In addition, you can choose 'English' or 'Korean(한국어)' translation through the navigation bar.



![homepage](/img/homepage.png)


<br>

<br>


## Our Challenges Before User Feedback

The feedback we received was mainly related to the  accuracy of the model, so we prioritized improving the model's performance.

There have been many attempts related to the deep learning model, which can be seen in following link.

[our attempts before & after feedback](https://github.com/yskim0/GoogleSolutionChallenge_Handlang/blob/master/before_usr_feedback.md)

<br>

## Plan for future extension 

Any advice would be welcome.

- Deep learning model
    - Improve performance by preprocessing and learning various datasets
    - Add (0~9) labels to model
    - Add essential words / expressions
    - Create KSL model if conditions (e.g. dataset) are met

- Web page
    - Make UI/UX better
    - Deploy ! (not local service)


<br>

## Team Handlang

- Yonsoo, Kim (김연수) : Ewha w.univ.
    - [Github](https://github.com/yskim0)
- Jiyoung, Shin (신지영) : Ewha w.univ.
    - [Github](https://github.com/Turtlefromocean)
- Hyunju, Seo (서현주) : Ewha w.univ.
    - [Github](https://github.com/seohsj)
- Suhyune, Son (손수현) : Ewha w.univ.
    - [Github](https://github.com/sonsuhyune)


----

**We want the world to see our impact.**
