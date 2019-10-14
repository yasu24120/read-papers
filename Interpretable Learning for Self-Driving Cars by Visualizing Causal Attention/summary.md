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
　・Max-poolingをomit (Lee[17]ら)  
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

#### 3.4 Fine-Grained Decoder : Causality Test  
・Attentionのマッピングをrefineする  
  
・attention weights {α<sub>t,i</sub>}  
・input raw images {I<sub>t</sub>}  
・map of attention M<sub>t</sub> = f<sub>map</sub>({α<sub>t,i</sub>})  
・本研究では、5x5 と 3x3 CNNをpoolingなし  
　・80x160が 10x 20x64、アスペクト比変更なし  
・なので、f<sub>map</sub>({α<sub>t,i</sub>})を8倍のupsampling functionとして使う  
・ガウシアンフィルタリングがそれに続く  

・Local visual saliency抽出のため、以下を行う  
　・attention mapで調整されたinput raw image上で、2D N particles をランダムに抽出し、置換する(?)  
　　・spatio-temporal 3D paticles P←P∪{P<sub>t</sub>, t}を保存する  
　・クラスタリングを行う  
　　・DBSCANを用いた  
　　・grouping 3D particles P into clusters {C}  
　　・各クラスタcのテント、time frame tごとに、convex hull H(c)を計算する  
　　　・local regionを探すため  
　・各 c と t において、精度の低下度合いを検証する  
　　・H(c)で計算された領域を、0でマスキングすることで検証(?)  
  
![image](https://user-images.githubusercontent.com/30098187/66732886-9f814680-ee98-11e9-885f-646d7fb95bd4.png)  
  
### 4. Resulet and Discussion
#### 4.1 Datasets
・以下のデータセットを用いた  
　・Comma.ai  
　・Udacity  
　・Hyundai Center of Excellence in Integrated Vehicle Safety Systems and Control (HCE)  
  
・下記を含む  
　・front video data  
　・車速、加速度、ステアリング角度、GPS、角速度（ジャイロ）  
　・高速道路がメイン  
![image](https://user-images.githubusercontent.com/30098187/66733024-1cacbb80-ee99-11e9-8b81-ea5c14de3c73.png)  
  
#### 4.2 Training and Evaluation Details  
・x<sub>t</sub>の学習のために、5 layer CNNを学習  
　・5 layer fully connected layersを足している (hid_dimは1164, 100, 50, 10)  
　・u<sub>t</sub>を推定する  
・10x20x64の特徴量を抽出した後に、200x64にflattenされる  
　・これはcoarse-grained decoderに入力される  
  
・LSTMは、1～5層で実験したが、劇的な精度向上は得られなかった  
　・よって、1層にした  
・Adam optimizerを使用  
・0.5dropout　をhidden state  
・Xavier initialization  
・batch size 128  
・フレームTは20  
  
・データオーギュメンテーションはなし  
　・難しいらしい  

#### 4.3 Effect of Choosing Penalty Coefficient λ  
・λ∈{0, 10, 20}で実験した  
![image](https://user-images.githubusercontent.com/30098187/66738794-43272280-eeaa-11e9-9513-d4c7658179b1.png)  

・λを大きくすると、より広い範囲でattentionしていることがvisualizeできる  
  
#### 4.4 Effect of Varying Smoothing Factors
・ステリング角度と車速のスムージング  
　・αの値を変えて、精度がどう変わるかを検証  
![image](https://user-images.githubusercontent.com/30098187/66739022-c8aad280-eeaa-11e9-88dd-29434e7a8098.png)  
  
#### 4.5 Quantitative Analysis  
・FCNでも検証した  
![image](https://user-images.githubusercontent.com/30098187/66739144-07d92380-eeab-11e9-83ff-03c8a0d76794.png)  
  
・Attentionによって、大きな精度の低下はなかった  
  
#### 4.6 Effect of Causal Visual Saliences

・もやもやがどれくらいシンプルにできたのかを検証した  

![image](https://user-images.githubusercontent.com/30098187/66739382-83d36b80-eeab-11e9-8314-7bfe677c2f33.png)  

