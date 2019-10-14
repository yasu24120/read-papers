# Interpretable Learning for Self-Driving Cars by Visualizing Causal Attention 
https://arxiv.org/pdf/1703.10631.pdf  

## 概要　　 
・Imageからsteering angleを推定する問題設定において、vehicle controller が、どこに着目しているのかを示すモデルの提案   
・ネットワーク構造は以下の3ステップ：   
　・Encoder : 画像から特徴抽出   
　・Visual attentionを含む Coarse-grained (荒い) decoder   
　・Fine-grained decoder: casual visual saliency detection と attention mapの復元を行う   
![image](https://user-images.githubusercontent.com/30098187/66712753-4e138180-eddc-11e9-8d3c-7fd9f7845f62.png)   

## Contributions 
・Visual attention heatmapはdeep neural vehicle controllerの説明をすることに適していることを示した   
・”blobs”(もやもや)を含むattention mapは、セグメンテーションとフィルタリングによって、よりシンプルで確かなmapに再構築できる   
・本研究でのモデルを、1,200,000ビデオ（約16時間分の走行）に適用した   
   
## 本文メモ   
### Related Works   
#### 2.1 End-to-End Learning for Self-driving Cars   
・Self driving carsの学習には以下の2通りがある:   
　・Inter mediate approach : 地物などを検出して、if-then-else rulesで車両をコントロールする   
　・End-to-end approach: 人間が録画したビデオから、コントローラを予測する   
・中間のアプローチも提案されたが、以下のような問題点があった:   
　・i. intermediate layerを用いたらcontrol accuracyが低下した(40%以上)   
　・ii. Intermediate feature extractors は限定された説明しか与えなかった   
　・iii. 著者らは間違ったinput featureがあっても、除去できないと論じた   
・上記に対して、本論文では、精度を落とすことなく、interpretableなモデルを構築した   
   
#### 2.2 Visual Explanation   
・Deconvolution: 離散的な特徴量が、どのように出力に影響を与えているか示せないらしい   
・Attention-based-approach : ネットワークの出力に影響をしない部分を抽出できる(マスクするため)   
　・DenseCap   

### Method   
#### 3.1 Preprocessing   
・モデルは input raw pixels から、 continuous steering angle commands を推定する   
　・inverse turning radius u<sup>^</sup><sub>t</sub> (=r<sup>-1</sup><sub>t</sub>, r<sub>t</sub>はturning radius)を推定する   
　・t : timestep   
　・steering angle commandは車両のステリングジオメトリと零点付近で不安点のため(?)    
  
・Inverse turning radius u<sub>t</sub>  と steering angle command θ<sub>t</sub>はアッカーマンステアリングジオメトリで以下の通りに近似できる:    
![image](https://user-images.githubusercontent.com/30098187/66717725-3dccc800-ee17-11e9-87cf-9381cf554a54.png)  
　・θ<sub>t</sub> : steering angle (degrees)   
　・v<sub>t</sub> : velocity at time t (m/s)    
　・K<sub>s</sub> : ステアリングとホイールの回転の比(ステアリング比?)   
　・K<sub>slip</sub> : ホイールと道路面の相対的な運動を示す   
　・d<sub>w</sub> : フロントとリアホイール間の距離   
・本研究のモデルは、車速とステアリングコマンドが学習に必要   
   
・computational costの削減のために、以下を行った:   
　・80x160x3に画像を、nearest neighbourでダウンサンプル   
　・アスペクト比が違うものについては、高さ方向をcropした   
　・画素をHSV colorspaceに変換   
　　・[0,1]となるように正規化した   
  
・single exponential smoothing methodを適用し、人間によるブレとノイズを低減   
・smoothing factor 0 ≦ α<sub>s</sub> ≦ 1 としたときに、simple smoothig exponential は下記の通り定義できる:   
![image](https://user-images.githubusercontent.com/30098187/66717738-56d57900-ee17-11e9-9a2e-418ccde28bf0.png)  
　・θ<sup>^</sup><sub>t</sub>、 v<sup>^</sup><sub>t</sub>はそれぞれθ<sub>t</sub>とv<sub>t</sub>をスムージングしたものを示す   
　・α<sub>s</sub>=1の時、スムージングなしと同じで、α <sub>s</sub>が0に近づくほど、強くスムージングされる。   

#### 3.2 Encoder  
・Fig.1を参照  
・CNNを用いてconvolutional feature cube x<sub>t</sub> を抽出  
　・5 layered CNNを用いた。　モデルは先行研究(Bojarski [3])より。  
　・Max-poolingをomit (Lee[17]らが論売るように。)  　
　・3個の特徴量をCNNより抽出し、LSTMへの入力とした  
  
・Convolutional feature cubeは WxHxDがt毎に作られる  
・その後、 x<sub>t</sub> (a set of L=WxH features) を回収する  
　・それぞれは D-dimentional feature slice  
![image](https://user-images.githubusercontent.com/30098187/66730017-ddc33980-ee89-11e9-9ab1-482e8cb04f19.png)  
　・x<sub>t,i</sub> ∈ R<sup>D</sup>  
　・i ∈ {1, 2, ..., L}  
　・要は、tensorのdim=0 , 1のもの  
  
#### 3.3 Coarse-Grained Decoder : Visual Attention  
・Attention π({x<sub>t,1</sub>, x<sub>t,2</sub>, ..., x<sub>t,L</sub>}) のゴールは、良いコンテキストvector y<sub>t</sub> を探すこと  
・この部分では、deterministic soft attentionを適用  
  
・モデルはαを用いて y<sub>t</sub>を抽出する  
![image](https://user-images.githubusercontent.com/30098187/66730258-75755780-ee8b-11e9-9aa6-47653904c35a.png)  
　・α<sub>t,i</sub> : scalar attention weight  
　　・Σ<sub>i</sub>α<sub>t,i</sub> = 1  
　・f<sub>flatten</sub>: flatten function  
　・y<sub>t</sub>: DxL-dimentional vectorで、attentionで重みづけされたconvolutional feature vector  
  
・注意：本件k通のattention mechanism π({α<sub>t,i</sub>}, {x<sub>t,i</sub>})は先行研究のものとは違う  
　・先行研究は、y<sub>t</sub> = Σ<sup>L</sup><sub>i=1</sub>α<sub>t,i</sub>x<sub>t,i</sub>  
  
・本研究では、LSTMを用いて、inverse turning radius u<sup>^</sup><sub>t</sub>推定し、attentionを出力する  
　・下記より推定  
　　・previous hidden state h<sub>t</sub>  
　　・current convolutional feature cube x<sub>t</sub>  
  
・Attentionは下記  
![image](https://user-images.githubusercontent.com/30098187/66730461-e49f7b80-ee8c-11e9-85cf-4ae7c0d48597.png)  
　・multinomial logistic regression (i.e. softmax regression)で計算  
  
・同時に、u<sup>^</sup><sub>t</sub> と f<sub>out</sub>(y<sub>t</sub>, h<sub>t</sub>)も出力する  
  
・LSTMの初期値は以下の通り(Xu [26]らに準ずる)  
![image](https://user-images.githubusercontent.com/30098187/66730622-e0c02900-ee8d-11e9-87fb-49cd366a133b.png)  
　・CNNの最初の出力の平均をとったもの。cもhも同じ  
  
・Double stochastic regularizationはattentionの別々のところをよしなにしてくれるようにできるらしい  
・今回は、additional hidden layer f<sub>β</sub>を導入し、 scalar β = sigm(f<sub>β</sub>(h<sub>t-1</sub>))を推定  
![image](https://user-images.githubusercontent.com/30098187/66730844-0d287500-ee8f-11e9-9c42-795159e5e7d1.png)  
  
・Penalized Loss function L<sub>1</sub>を用いる:  
![image](https://user-images.githubusercontent.com/30098187/66730865-2df0ca80-ee8f-11e9-9f71-a6a3e0c9613e.png)  
　・T: Length of time step  
　・λ: penalty coefficient  
