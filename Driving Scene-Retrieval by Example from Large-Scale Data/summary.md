# Driving Scene-Retrieval by Example from Large-Scale Data
http://openaccess.thecvf.com/content_CVPRW_2019/papers/Vision_Meets_Cognition_Camera_Ready/Hornauer_Driving_Scene_Retrieval_by_Example_from_Large-Scale_Data_CVPRW_2019_paper.pdf
https://www1.icsi.berkeley.edu/~stellayu/publication/doc/2019driveCVPRWPoster.pdf  
  
## 概要  
ラベル付けされていない類似シーンを、画像+action vectorをクエリとして投げることで検索する方法の提案。  
手法自体は、参考文献[4]をBDD-Xに合わせるために適用した。  
　・Resnetで特徴抽出(classificationをneighbourhood metric learningで解かせる)  
　・action vectorをconcatenate  
　・memory bankを使用  

![image](https://user-images.githubusercontent.com/30098187/63404989-37762d00-c420-11e9-81a9-ef635c8d0494.png)  

  
## Contributions

## 本分メモ  

### 問題設定  
1. ラベル付されていない、特定のシーンをどうやって検索するか？  
2. 検索したいシーンが既に手元にあった場合に、どうやって似ているデータを検索できるか？  

### Method

#### 使用データ 
BDD video-dataset  
　・1.8TB driving scenes  
　・accelerations, angular velocities, GPS information  
　　・Action vectorsに変換される[6]  
  　　・http://zpascal.net/cvpr2017/Xu_End-To-End_Learning_of_CVPR_2017_paper.pdf  
    　・pretrained model is here: https://github.com/gy20073/BDD_Driving_Model  
　・100Kの非連続なシーンは、weather, scene, timeof day でアノテーション  
　　・subsetの10Kはimage segmentationsとobjectsが含まれている  
  　　・ただし、subsetのアノテーション情報は、学習時に使わない  

#### Driving Scene Definition  
・データセットを、40秒ごとに分割  
・6 sampled frames  
・hop with 4-frame spacing in between cosecutive frames  
  
最終的なドライビングシーンは、(x<sub>i</sub>, a<sub>i</sub>)  
x<sub>i</sub> : images  
a<sub>i</sub> : action vectors  

#### Neighborhood Metric Learning
[4]を参考にした 。https://github.com/yasu24120/read-papers/blob/master/Improving%20Generalization%20via%20Scalable%20Neighborhood%20Component%20Analysis/summary.md  
・上記手法を、拡張子、BDD-Vに適用した  
  
・Resnet18 を使用  
・instance-based learningをした(あるシーンから、IDを推定するようにした)  
・128 dimentional feature vector  
・non-parametctic Softmax classification [5]  
  
・resnetに合わせるために、video size を 224x224に修正  
・top-Kで評価  
・action probability vecotorは、 go straight, stop or slow, turn left, turn right  
・action probability vecotorは、Resnet-backboneのsecond layer outputにconcatenate  
　・vectorは、28x28に拡張される

#### 結果  
Single image の結果。  
・time of the day, wearher などはうまくいっている。  
・pedestrian crossings, angle to the streets, colors of head / taillights はうまくいっていない。  
![image](https://user-images.githubusercontent.com/30098187/63306628-5db7a200-c326-11e9-9a02-e6206b5c9c77.png)  
  
Sequence of images 結果  
・pedestrian crossings, angle to the streets, colors of head / taillights　もうまくいくようになった。  
・何フレーム分投入したかは謎。  
![image](https://user-images.githubusercontent.com/30098187/63306805-1c73c200-c327-11e9-824f-bf3fe286475d.png)  
![image](https://user-images.githubusercontent.com/30098187/63306925-80968600-c327-11e9-8361-aba5e10ac8d1.png)  
