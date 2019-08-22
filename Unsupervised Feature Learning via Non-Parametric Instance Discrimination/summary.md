# Unsupervised Feature Learning via Non-Parametric Instance Discrimination
http://openaccess.thecvf.com/content_cvpr_2018/CameraReady/0801.pdf  
https://github.com/zhirongw/lemniscate.pytorch  

## 概要  
画像分類を、各画像1クラスとして解く。  
上記問題を解く上で、似た特徴を持つクラス同士が、embedding空間上で近くなることが期待できる。  
このembedding空間を学習することを目的とする。  
実際の画像分類は、kNNとSVMで評価した。  

![image](https://user-images.githubusercontent.com/30098187/63408330-b754c500-c429-11e9-8532-e7015d80ea2b.png)  


## Contributions  

## 本文メモ  

### Approach
ゴールは、教師なしでembedding function v = f<sub>θ</sub>(x)　を学習すること  
f<sub>θ</sub> : パラメータθのニューラルネットワーク  
x : image  
v : feature  
  
このembeddingは画像空間上でのmetricを作成する  
i.e. インスタンスx,yに対して、 d<sub>θ</sub>(x,y) = ||f<sub>θ</sub>(x) - f<sub>θ</sub>(y)||  
embeddingよけば、似ている画像同士は近いはず  
  
本論文で提案する方法は、instance-level discriminationで、各画像を個別のクラスとして扱い、学習させる  

#### Non-Parametric Softmax Classifier
##### Parametric Classifier  
いわゆる普通のsoftmax  
![image](https://user-images.githubusercontent.com/30098187/63476272-4a8a0b00-c4bb-11e9-8e84-dadf0e64f92d.png)  
v : 特徴ベクタ、画像x<sub>i</sub>としたときに、v<sub>i</sub>=f<sub>θ</sub>(x<sub>i</sub>)  
w<sub>j</sub> : クラスjの weight vector  
w<sup>T</sup><sub>j</sub>vはどの程度vがj番目のクラスに属するかを表す  
  
#### Non-Parametric Classifier
Parametric classifierだと、wはclass prototypeを示すため、インスタンス間の比較が出来ない  
↓  
w<sup>T</sup><sub>j</sub>vをv<sup>T</sup><sub>j</sub>vに置き換えて、  
L2-normalization layer を用いて、||v||=1とする  
![image](https://user-images.githubusercontent.com/30098187/63479180-15d08080-c4c8-11e9-992a-9a726b127292.png)  
τ : temperature parameter（増加させると確率分布がflatになり、減少させると確率分布がpeakyになる）  
　・参考 : https://www.quora.com/What-is-the-temperature-parameter-in-deep-learning  
  
学習の目的は、joint probability Π<sup>n</sup><sub>i=1</sub>P<sub>θ</sub>(i｜f<sub>θ</sub>(x<sub>i</sub>))の最大化  
i.e. ![image](https://user-images.githubusercontent.com/30098187/63479804-91333180-c4ca-11e9-82af-c089386dbe81.png) の最小化  
  
#### Learning with A Memory bank  
