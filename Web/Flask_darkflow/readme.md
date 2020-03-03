[실행순서]

1. 가상환경 실행
    `pipenv shell` 

2. templates 폴더, server.py, requirements.txt 파일 다운
    `git clone https://github.com/yskim0/Handlang/tree/master/Web/Flask_darkflow`

3.  `pip install -r requirements.txt`

4. darkflow git clone
    `git clone https://github.com/thtrieu/darkflow`

5.  `cd darkflow`

6.  `python3 setup.py build_ext --inplace`
    또는
    `pip install -e .`

7. cd darkflow/cfg 에 custom 한 cfg 파일 다운받기

8. cd darkflow/darkflow에 built_graph 폴더 생성 후 안에 pb파일, meta 다운받기

9. cd Flask_darkflow (기본폴더)

10. server.py 실행
    `python3 server.py`

11.  0.0.0.0:5000 

2020.02.28 (수정)
