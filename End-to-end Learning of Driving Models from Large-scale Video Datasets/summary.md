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
  
ここで、v<sup>→</sup>は  
