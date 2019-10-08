# End-to-end Learning of Driving Models from Large-scale Video Datasets
http://zpascal.net/cvpr2017/Xu_End-To-End_Learning_of_CVPR_2017_paper.pdf  
Pre-trained modelもあり  
https://github.com/gy20073/BDD_Driving_Model  

## 概要  
画像と、ego vehicle の前の状態から、 straight, stop, left-turn, right-turn の4種類の行動を推定する 

![image](https://user-images.githubusercontent.com/30098187/64085973-96b53500-cd70-11e9-8cda-8a52d4b28eb2.png)  

## Contributions  
1. 画像と、ego vechileの前の状態から、action policyを推定する方法の提案  
2. demonstration lossとsegmentation loss　から、推定モデルを構築できFCN LSTMの提案  
3. データセットを収集・公開した  
4. side task (semantic segmentation)を行うことで、egomotion predictionが早く収束することを発見した  
  
## 本文メモ  

### Related Work
・ALVINN: autonomas vehicle navigationにneural networkを初めて使った  
・その他、visual informationからegovehicle motionを推定する研究がまとめられている  
　・NVIDIAがdriving framesから特徴を抽出する  
  
・別のinformationを与えて、学習をエンハンスするようなフレームワークの紹介  
　・Learning under privileged information (LUPI)  
 　　・A new learning paradigm: Learning using privileged information  
　・bound-box、image tags、attributesを、DPM frameworkに導入した例  
　　・Learning　to rank using privileged information  

### Deep Geberuc Driving Networks
#### Generic Driving Models
Driving model Fを下記の通り定義する  
![image](https://user-images.githubusercontent.com/30098187/66361385-92a4b480-e9b9-11e9-965e-fb85f31a8f91.png)  
  
F(s, a) : feasibility score of operating motion action a under the state s  
  
本研究では、raw pixelとcurrent / prior vehicle state signal を inputとして、future motionの確率を求める  
motion action set Aの例は以下の通り:  
![image](https://user-images.githubusercontent.com/30098187/66361510-fcbd5980-e9b9-11e9-8304-914ff4d5fa57.png)  
  
egomotionを、未来の進行方向とすることもできる。その場合は  
![image](https://user-images.githubusercontent.com/30098187/66361544-1c548200-e9ba-11e9-9693-3e5ea531fce8.png)  
  
ここで、v<sup>→</sup>は未来のegomotion  
  
F(s, a)を、NLPにおけるN-gram language modelぽく解釈する  
  
#### FCN-LSTM Architecture  
・画像から得られる特徴量と、時系列な特徴量を反映させたいため、FCNとLSTMを組み合わせた  
  
##### Visual Encoder  
・ImageNet pre-trained AlexNetを使用  
・POOL2　と　POOL5 layer を削除  
・conv3からfc7において、dilated convolutionを使用  
  
#### Temporal Fusion
・本研究では、過去のground truth sensor information (speed, angular velocity) を画像からの特徴量とconcatenateした。  
・各time stepにおいて、visual と sensor stateをLSTMを用いて、ひとつのstateとして表現した  
・LSTMの代わりに、temporal convolutionを用いた場合も実施した  
　・tcn: https://github.com/philipperemy/keras-tcn  
  
#### Driving Perplexity
・Evaluation metric (perplexity) の提案  
  
・NLPを参考にする  
・bigram modelは下記の確率を出力する  
![image](https://user-images.githubusercontent.com/30098187/66363261-a6074e00-e9c0-11e9-991d-15e9040b9b98.png)  
・一方で、本研究では下記の通り  
![image](https://user-images.githubusercontent.com/30098187/66363296-c33c1c80-e9c0-11e9-971f-fbe0cf6cb9d1.png)  
  
・perplexityを下記の通り定義する  
![image](https://user-images.githubusercontent.com/30098187/66363342-f2eb2480-e9c0-11e9-9437-5c4f3365ff2c.png)  

・以下のようにしてもよい  
　・a<sub>pred</sub> = argmax<sub>a</sub>F(s, a)　として、a<sub>real</sub>と比較  
 
#### Discrete and Continuous Action Prediction
・２種類の推定を行う  
  
・Discrete actions: 進行方向(4方向+stop)を推定する。cross entropy lossを最小化する  
  
・Continuous actions: 進行方向(1度刻み)を推定する。分類問題として解く。  
　・回帰問題として解くのもあり  

#### Driving with Privileged Information (privileged information: 特権情報)
・Privileged learningで学習した  
　・task loss と side loss を最小化する  
　・本研究では、semantic segmentationを extra supervisionとして学習させた  
　・アプローチの違いを説明する図は以下の通り:  

![image](https://user-images.githubusercontent.com/30098187/66367031-7448b400-e9cd-11e9-8edc-530e851f1435.png)  
　・Motion Reflex approach : fully end-to-end  
　・Mediated perception approach : rely fully on predicted intermediate semantic segmentation labels  
　・Privileged training approach : semantic segmentationをサイドタスク  
   
 ・本研究では、fc7の後ろにsegmentation lossを導入  
 　・fc7に意味のある情報を学ばせる  
  
### Dataset
