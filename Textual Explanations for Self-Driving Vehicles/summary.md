# Textual Explanations for Self-Driving Vehicles
http://openaccess.thecvf.com/content_ECCV_2018/papers/Jinkyu_Kim_Textual_Explanations_for_ECCV_2018_paper.pdf
(コード (tensorflow))
https://github.com/JinkyuKimUCB/explainable-deep-driving

## 概要 

User acceptance is likely to benefit from easyto-interpret textual explanations which allow end-users to understand what triggered a particular behavior. Explanations may be triggered by the neural controller, namely introspective explanations, or informed by the neural controller’s
output, namely rationalizations. We propose a new approach to introspective explanations which consists of two parts. First, we use a visual (spatial) attention
model to train a convolutional network end-to-end from images to the vehicle
control commands, i.e., acceleration and change of course. The controller’s attention identifies image regions that potentially influence the network’s output.
Second, we use an attention-based video-to-text model to produce textual explanations of model actions. The attention maps of controller and explanation
model are aligned so that explanations are grounded in the parts of the scene that
mattered to the controller. We explore two approaches to attention alignment,
strong- and weak-alignment. Finally, we explore a version of our model that
generates rationalizations, and compare with introspective explanations on the
same video segments

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


### Attention Alignments
