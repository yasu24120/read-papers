# Can Spatiotemporal 3D CNNs Retrace the History of 2D CNNs and ImageNet?
http://openaccess.thecvf.com/content_cvpr_2018/papers/Hara_Can_Spatiotemporal_3D_CVPR_2018_paper.pdf  
https://github.com/kenshohara/3D-ResNets-PyTorch  

## 概要  
3D CNNのベンチーマーキング。  
(i) ResNet-18はUCF-101, HMDB-51, ActivityNetにoverfittingしたが、Kineticsにはしなかった。  
(ii) Kinectics dataset は152 ResNet layerを学習させるだけのデータ量があった  
(iii) Kinetics において、simple 3D architectureの方が、complex 2D architectureよりも性能が良かった。  
  
![image](https://user-images.githubusercontent.com/30098187/64217890-2e925a80-cefa-11e9-89b0-877d4c2b3c9f.png)

## Contribution  

## 本文メモ  

### Introduction  
以下のようなaction recognitionの動画データセットがあるらしい  
- 10K程度のサイズ
  - UCF-101  
  - HMDB-51  
- もう少し大きめのサイズ
  - ActivityNet  
  - Kinetics ←　デファクトスタンダード。300Kくらい。Imagenetの対として扱われるらしい  
  
精度が2D CNN > 3D CNNの理由は、3D CNNのパラメータを最適化しきるほどのデータ量がないと筆者らは言っている  
  
#### 問題設定  
- ImageNetにおける2D CNNの隆盛を、3D CNNでも同じことがいえるか？  
- いろいろな3D CNNアーキテクチャを、いろいろなデータセットに対して適用した  




 
