### tf.train.import_meta_graph.retore에서 Error

​      

일단 처음에 난 에러는

```
OSError: File ./ckpt/handlang-small-109495.meta does not exist.
```

 : default.py 에서 arg값을 정해줄때 모든 path를 ./밑으로 정해져있었다. 

   하지만 우리의 모든 data는 ~/ 밑 특정 폴더 아래에 있었기 때문에 적절한 위치로 path를 다시 지정해줬다

   (default.py에서 변경 or 명령어에 "--backup [path]" )



그래도 위의 에러가 해결되지 않았다.

원인이 됐던 코드는 크게 두가지

1. loader.py의 

   **saver = tf.train.import_meta_graph(meta)**

2. loader.py와 help.py의

   **self.saver.restore(self.sess, load_point)**



위 두가지 에러를 확인하기 위해 아래의 코드를 활용했다.

```python
import tensorflow as tf
saver = tf.train.import_meta_graph("ckpttt/handlang-small-109795.meta") 
sess = tf.Session()
saver.restore(sess, "ckpttt/handlang-small-109795")
```

일단 서버내에서 하다보니, path가 자꾸 헷갈려서 os.listdir([path])로 해당 path내에 있는 파일을 계속 확인하면서 진행했다.



**-import_meta_graph함수에는 확장자까지 써줘야한다**

: 만약 여기서 확장자나, 올바른 path가 아니면

 ValueError: The passed save_path is not a valid checkpoint 에러가 발생한다.



**-restore에서는 확장자를 제외해야한다.**

:여기서 만약 확장자도 함께 넣어주게되면

 아래와 같은 Dataloss 에러가 뜬다.

 DataLossError (see above for traceback): Unable to open table file ckpt/handlang-small-105435.meta: Data loss: not an sstable (bad magic number): perhaps your file is in a different file format and you need to use a different restore operator?



---------------------------------------------------

**darkflow 이미 학습된 checkpoint ( .meta 확장자)를 다시 load해서 추가 training 시킬 때 사용한 명령어**

```
python3 flow --model cfg/handlang-small.cfg --backup 'ckpttt/' --train --dataset "Data/handlang-data-1-400/dataset/" --annotation "Data/handlang-data-1-400/annotations/" --batch 20 --epoch 2000 --save 200 --keep 200 --lr 1e-05 --load 109795
```

: default.py에서 이미 지정해준 부분도 있지만 혹시 몰라 다시 한번 지정해주었고

 전체 코드 중간중간 print(ckpt), print(meta) 등을 넣어서 계속 path를 확인해주었다.!



​      