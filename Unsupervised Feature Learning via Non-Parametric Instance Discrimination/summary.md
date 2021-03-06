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
Eqn.2 の P(i│v) を計算するには、全画像の{v<sub>j</sub>}が必要。  
↓  
Memory bank V を導入  
  
V = {v<sub>j</sub>}: メモリバンク  
f<sub>i</sub> = f<sub>θ</sub>(x<sub>i</sub>) : x<sub>i</sub>の特徴  
・イテレーション毎に、SGDでf<sub>i</sub>とθが最適化される  
・f<sub>i</sub> は V　の、関連するインスタンスにアップデートされる i.e. f<sub>i</sub> → v<sub>i</sub>  
・V の初期値は、unit random vectors  
  
#### Discussions
{w<sub>j</sub>} はfixed classに対応。non-parametric にすることにより、クラスに依存しない学習ができる  
  
### Noise-Contrastive Estimation  
non-parametric softmaxを計算する際に、クラスnが大きいとコストがかかる → NCEを用いた  
  
basic idea : multiclass classification を複数のbinary classification に分割  
　・data samples と noise samples を分類する  

メモリバンク内の v　が i番目のexample に対応する確率は :  
![image](https://user-images.githubusercontent.com/30098187/63486006-98fdd080-c4e0-11e9-886f-d7475ab27889.png)  
Z<sub>i</sub> : normalizing constant  
noise distributionは、一様分布とした i.e. P<sub>n</sub> = 1/n  
  
・noise sample が、data sample よりも m倍頻出すると仮定。  
・feature v　を持つ sample iがdata ditribution (D=1)に属する確率は  
![image](https://user-images.githubusercontent.com/30098187/63486528-e4b17980-c4e2-11e9-825a-fe2c24b387d9.png)  
  
この式の元での目的は、data とnoise samplesのnegative log-posterior distributionの最小化  
![image](https://user-images.githubusercontent.com/30098187/63486955-6ce44e80-c4e4-11e9-9e3e-21a52099dcaa.png)  
P<sub>d</sub> : 実際のdataの分布  
P<sub>d</sub>にとって、vはx<sub>i</sub>に対応するfeature  
P<sub>n</sub>にとって、v'は別の画像（noise distribution P<sub>n</sub>からランダムにサンプルされる）に対応するfeature  
vとv'は、ランダムにnon-parametric memory bank V からサンプリングされる  
  
Z<sub>i</sub>をEq.4から求めることは困難　→　定数として扱い、モンテカルロ法で値を推定する  
![image](https://user-images.githubusercontent.com/30098187/63487821-a5d1f280-c4e7-11e9-9379-9cc82c596717.png)  
{j<sub>jk</sub>} : random subset のインデックス  

### Proximal regulation
この手法では、1クラスあたり1インスタンスしかない　→　学習時に、lossが振動する  
↓  
proximal regulationを導入  
  
・イテレーションtでは、 v<sup>(t)</sup><sub>i</sub> = f<sub>θ</sub>(x<sub>i</sub>) で特徴が計算される  
・メモリバンク内は、前のイテレーションの情報が格納されている i.e. V = {v<sup>(t-1)</sup>}  
P<sub>d</sub>からのpositive sample へのpositive loss functionは、  
![image](https://user-images.githubusercontent.com/30098187/63488583-7670b500-c4ea-11e9-96d4-23813dd115a9.png)  
学習が収束すると、v<sup>(t)</sup><sub>i</sub> - v<sup>(t-1)</sup><sub>i</sub>は消え去るはず  
  
最終的な目的関数は  
![image](https://user-images.githubusercontent.com/30098187/63489710-c7ce7380-c4ed-11e9-8157-976f81af7d1d.png)  
λ : ハイパーパラメータ  
  
効果は下図の通り  
![image](https://user-images.githubusercontent.com/30098187/63489745-db79da00-c4ed-11e9-8817-31dad8947ab7.png)  
  
### Weighted k-Nearest Neighbor Classifier
test画像x^の分類時:  
1. 特徴ベクトルを計算 f^ = f<sub>θ</sub>(x^)  
2. memory bank内の全画像のembeddingと比較。 cosine類似度を使用 s<sub>i</sub> = cos(v<sub>i</sub>, f^)  
3. top k nearest neighbors (Ν<sub>k</sub>) によるweighted votingで推論する  
  
クラスcは以下のweightを得る:  
w<sub>c</sub> = Σ<sub>i∈Ν<sub>k</sub></sub>α<sub>i</sub>・1 (c<sub>i</sub> = c)  
α<sub>i</sub> = exp(s<sub>i</sub>/τ) : neighbor x<sub>i</sub> の contributing weight  
  
今回は、 τ=0.07、k=200とした  
  
## Experiments  
4つの実験をした  
1. CIFAR-10を用いてnon-parametric softmaxとparametric softmaxを比較  
2. ImageNetに適用し、他のunsupervided learningと比較  
3. semi-supervisedを試した  
4. object detectionを試した  
  
### Parametric vs. Non-parametric Softmax  
・バックボーンとして ResNet18を使用  
・output featureは128次元  
・embedding後、SVMとkNNで学習  
  
![image](https://user-images.githubusercontent.com/30098187/63493013-98236980-c4f5-11e9-9ba8-64710f994bea.png)  

### Image classification  
・githubのコードはこれ  
  
#### Experimental Settings
・τ=0.07  
・NCE, m=4096  
・SGD, momentum, 200 epochで学習  
・batch size = 256  
・learning rate = 0.03, 40 epoch毎に0.1倍。120epochからは下げない  
  
#### Comparisons
ImageNetへの適用結果  
ふたつの手法で評価  
(1) conv1〜conv5までの中間層に対して、Linear SVMを適用した結果に基づいてclassification  
(2) output featureにkNNを適用してclassification  
  
![image](https://user-images.githubusercontent.com/30098187/63496021-0c610b80-c4fc-11e9-8f7f-b0013971c5b9.png)  
  
・層が深くなるほど精度が向上している→良いembedding  
・一番良い層の出力をメモリバンクに登録する　みたいなことをしようとした際に、本手法は128次元のため、必要な容量が少なくて済む  
  
#### Feature generalization
ImageNetで学習したモデルを、finetuningなしでPlaces datasetに適用した  
  
![image](https://user-images.githubusercontent.com/30098187/63496097-374b5f80-c4fc-11e9-89ec-5646feb140d4.png)  
  
・ImageNetと同様の結果  
  
#### Consistency of training and testing objects

![image](https://user-images.githubusercontent.com/30098187/63496255-84c7cc80-c4fc-11e9-8d5a-8fd06c1cebf1.png)  

・overfittingせずに、学習が進んでいるように見受けられる  
  
#### The embedding feature size
embeddingの次元と精度について検証  
  
![image](https://user-images.githubusercontent.com/30098187/63496473-f273f880-c4fc-11e9-8b53-063f810d1cc1.png)  
  
#### Training set size
Trainingのデータセットサイズと精度について検証した  
![image](https://user-images.githubusercontent.com/30098187/63496657-4383ec80-c4fd-11e9-8aab-5962fc4b7f83.png)  
  
#### Qualitative case study
・画像をクエリとして投入し、検索してみた  
・cosine類似度を使用
![image](https://user-images.githubusercontent.com/30098187/63496855-965da400-c4fd-11e9-91c5-f1b4b6578dee.png)  
  
### Semi-supervised Learning
Unlabelled で学習　→　Labelledでfinetuning  
・top-5 accuracy  
・Finetuning時 70epoch, initial learning rate 0.01, decay rate of 10 every 30 epochs  
・labelled は1％〜20%  
  
![image](https://user-images.githubusercontent.com/30098187/63503066-be530480-c509-11e9-97f2-4f98dbb4f753.png)  
  
### Object detection
PASCAL VOC 2007に転移学習した  

![image](https://user-images.githubusercontent.com/30098187/63503336-3b7e7980-c50a-11e9-9c70-1e99ccf691eb.png)  
  
