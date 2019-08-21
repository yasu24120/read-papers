# Textual Explanations for Self-Driving Vehicles
http://openaccess.thecvf.com/content_ECCV_2018/papers/Jinkyu_Kim_Textual_Explanations_for_ECCV_2018_paper.pdf  
(コード (tensorflow)) https://github.com/JinkyuKimUCB/explainable-deep-driving  

## 概要 
Dashcam imagesから、加速度、車両の信仰角度の変化を推定。  
また、車両の挙動の説明文とその理由を生成。  
生成のために、attentionを２種類用いて生成する。  
文章生成自体は、seq2seqのように、LSTMを使用。  

## Contributions  
1.Introspective textual explanation modelの提案。  
　自動運転車を対象とし、deep vehicle control networkの（解釈が容易な）説明文を出力する。  
  
2.Explanation generatorの実装。また、generator内の手法の比較。  
　A.Attention-aligned explanations  
　B.Non-aligned rationalizations  
  
3.Berkeley DeepDrive eXplanation (BDD-X) datasetの作成。  
　6984ビデオに、説明文がアノテーションされている。  
　e.g. “The car slows down”, “because it is about to merge with the busy highway”  

## 本文メモ
### 前提知識
#### 説明文について
Explainable modelは下記の理由により重要：  
i. ユーザの受容性  
ii. ユーザによる車両の挙動（とその理由）の把握  
iii. ユーザと車両間のコミュニケーション促進  

Explanation は以下に大別できる：  
・Rationalizations: システムの動作が事後にわかる(post-hoc manner)  
・Introspective explanations: システムの内部状態に基づく説明。システムのinput/behavior/goalについて記述される。  
　Visual attentionを用いて生成することがひとつの手法としてあげられるが、特定のアクションと特定のinput regionを結びつけない。  

#### self-driving carの実現方法について
ふたつの実現方法に大別できる:  
・Mediated perception based approach  
　人間が定義した特徴(レーン、信号機、歩行者、車両など)に基づいて、自動運転を行う。  
  
・End-to-end learning approach  
　ニューラルネットワーク(behavioral cloning)を用いて自動運転を行う。  
Behavioral cloning: 人間の運転から、driving policyを学ぶ。　（逆強化学習？***要サーベイ***）  
[3]: dashcam imagesからsteering controlsへマッピングするNN  
[26]: raw pixelを入力として自車の次の動きを推定するNN  
↓  
ポテンシャルは高いが、何がおこっているか説明できない。  
↓
本研究では、end-to-end trainable systemを提案。  
・NNの推論を、attention mapと自然言語で確認できるようにする。  

### 問題設定  
・ビデオから、テキストで、説明文（状況とその理由）を生成することを目的とする  
e.g. “vehicle slows down” / “because it is approaching an intersection and the light is red”  
・データセットは、既存のデータセットにアドオンする形で説明文を人手で付与した。  

![image](https://user-images.githubusercontent.com/30098187/62769543-2817eb00-bad4-11e9-8a4a-18d0b35fd3d7.png)
  
### 手法 (Explainable Driving Model)  
・以下を出力するモデルを提案  
(i) Decision makerが注視したimage regionを可視化  
(ii) 説明文(動作とその理由)  
  
モデルの中身は２つにわけられる:  
(1) Vehicle controller  
　　運転挙動を学習。加速度と車線変更。  
　　Visual (spacial) attentionを用いて、重要そうな部分を注視する。  
  
(2) Textual explanation generator  
　　動作文と理由文を出力する。  
　　Attention mapを揃えることで、vehicle controllerと対応付ける。
  
![image](https://user-images.githubusercontent.com/30098187/62769627-55fd2f80-bad4-11e9-97d4-c3c499754a46.png)

##### Preprocessing
車両挙動のデータ：  
・加速度 a<sub>t</sub>　：車速の微分値  
・車線変更 c<sub>t</sub>　：現在の車線とsimple exponential smoothingによって得られた値との差  
・10Hz  
    
画像:    
　・90x160x3、nearest-neighborでダウンサンプリング  
　・各画像は正規化（平均を引いて、標準偏差で割る）される。  
・4フレーム文に適用して、スタックしてneural networkに渡される  

##### Convolutional Feature Encoder
CNNをエンコーダとして利用  
・５層  
・max poolingなし (spacial information lossを防ぐ)  
・出力は3次元特徴量、wxhxt  

### Vehicle Controller  
・dashcam images　から、加速度とレーンチェンジを推定  
・Soft attentionを使用  

![image](https://user-images.githubusercontent.com/30098187/63161114-447ad100-c05a-11e9-8343-68943b6a5516.png)  
y<sup>c</sup><sub>t</sub> : 特徴ベクタ  
π<sup>c</sup> : mapping function  
α<sup>c</sup><sub>t,i</sub> : attention weight (softmax)  
i={1,2,...,l}  
l : convolutional feature vectorの番号  
  
attention model f<sup>c</sup><sub>attn</sub>(X<sub>t</sub>, h<sup>c</sup><sub>t-1</sub>)  
　・LSTMの隠れ層と、現在のベクタから算出される  
　・FC層とsoftmaxを含む  
  
Vehicle controllerのアウトプット  
　・加速度a^と<sub>t</sub>  
　・レーンチェンジc^<sub>t</sub>  
　・それぞれ、y<sup>c</sup><sub>t</sub>とh<sup>c</sup><sub>t</sub>をFC層+ReLuに代入し、値を推定する(f<sub>a</sub> , f<sub>c</sub>)  
  
#### 目的関数
![image](https://user-images.githubusercontent.com/30098187/63167968-ccb6a180-c06d-11e9-8c74-86e3f304bfb8.png)  
H: attentionのエントロピー  
λ<sub>c</sub>: ハイパーパラメータ  

### Attention Alignments
内省的な説明文を生成するためのattentionが2種類ある  

#### Strongly Aligned Attention (SAA)  
・y<sup>c</sup><sub>t</sub> (特徴ベクトル)　から直にattentionする  
・fig2の右上部分  

#### Weakly Aligned Attention (WAA)
・fig2の右下の部分  
・f<sub>a</sub>, f<sub>c</sub>, X<sub>t</sub>　からattentionする  
・KL-divergenceをlossとして扱う  
![image](https://user-images.githubusercontent.com/30098187/63171487-a812f780-c076-11e9-959e-46872443c2c6.png)  
α<sup>c</sup> : vehicle controllerのattention map  
α<sup>j</sup> : explanation generatorのattention map  
λ<sub>a</sub> : ハイパーパラメータ  

### Textual explanation generator
・データセットとして、descriptionとexplanationは一つの文章だが、<sep> tokenで分けられている  
・WAAでは、t毎にattention map α<sup>j</sup> を生成する。  
　・context vector y<sup>j</sup><sub>i</sub>に適用される。  
　・y<sup>j</sup><sub>i</sub>は、CNNから出力されるcontext vector (多分、X<sub>t</sub>と一緒)  
  
・tuple (a^<sub>t</sub>, c^<sub>t</sub>) を、それぞれのcontext vectorにconcatenateして、generatorに渡す  
　・spatially-attended context vector y<sup>i</sup><sub>t</sub>　→　WAAで使用  
  ・spatially-attended context vector y<sup>c</sup><sub>t</sub>　→　SAAで使用  
　・concatenated vectorはLSTMに渡される  
   
・explanation module は、seq2seqと同様  
　・temporal attention　βを適用  
　・βは、controller context vector (y<sup>c</sup><sub>t</sub>, SAA) か explanation vector (y<sup>j</sup><sub>t</sub>, WAA)　に適用  
![image](https://user-images.githubusercontent.com/30098187/63206026-6327a900-c0e8-11e9-80cc-e50a8a16d08b.png)  
Σ<sub>t</sub>β<sub>k,t</sub> = 1  
β<sub>k,t</sub>はattention model f<sup>e</sup><sub>attn</sub>({y<sub>t</sub>}, h<sup>e</sup><sub>k-1</sub>)から算出  
  
  
#### overallな損失は以下の通り  
![image](https://user-images.githubusercontent.com/30098187/63206062-de895a80-c0e8-11e9-8571-29274879ebcd.png)  
  
## Berkeley DeepDrive eXplanation Dataset (BDD-X)  
BDDに説明文を追加したもの  
![image](https://user-images.githubusercontent.com/30098187/63206103-4e97e080-c0e9-11e9-94da-26802fd5e029.png)  
・driving instructerによるアノテーション（whatとwhy）  
  
## Results and Discussions  
### Training and Evaluation Details
・Convolutional feature encoder  
　・5-layer  
　・12 x 20 x 64 がlast layer  
・Contoller  
　・CNN の後ろに5-FC  
　・隠れ層は 1164, 100, 50, 10  
・Controllerを学習後、explanation generator (single layer LSTM)を学習  
・Adam optimizer  
・dropout (0.5) @ hidden state connections  
・Xavier initialization  
  
・評価指標  
　・vehicle controller : mean absolute error, distance correlation  
　・justifier : BLEU, METEOR, CIDEr-D, human evaluation  
  
### Vehicle controller の結果
![image](https://user-images.githubusercontent.com/30098187/63206648-a9ced080-c0f3-11e9-9588-b5984748d57d.png)  
  
![image](https://user-images.githubusercontent.com/30098187/63206655-c408ae80-c0f3-11e9-9a5e-f18e071d723a.png)  

エントロピー正則化とattention mapのわかりやすさはトレードオフになっている  
  
### Textual Explanations の結果  
![image](https://user-images.githubusercontent.com/30098187/63206688-4a24f500-c0f4-11e9-8794-f7d551d90ae9.png)  

![image](https://user-images.githubusercontent.com/30098187/63206709-9bcd7f80-c0f4-11e9-8649-e5944ada44e3.png)  
  
![image](https://user-images.githubusercontent.com/30098187/63206718-b56ec700-c0f4-11e9-9c4e-51c367f8122f.png)  
  
λ<sub>a</sub>=10 , λ<sub>c</sub>=100　としておくのが一番良い気がする  
