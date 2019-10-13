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
