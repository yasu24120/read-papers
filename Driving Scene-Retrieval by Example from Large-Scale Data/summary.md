# Driving Scene-Retrieval by Example from Large-Scale Data
http://openaccess.thecvf.com/content_CVPRW_2019/papers/Vision_Meets_Cognition_Camera_Ready/Hornauer_Driving_Scene_Retrieval_by_Example_from_Large-Scale_Data_CVPRW_2019_paper.pdf
  
## 概要  
  
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
　・100Kの非連続なシーンは、weather, scene, timeof day でアノテーション  
　　・subsetの10Kはimage segmentationsとobjectsが含まれている  
  
ただし、アノテーション情報は、学習時に使わない  

#### Driving Scene Definition  
・データセットを、40秒ごとに分割  
・6 sampled frames  
・hop with 4-frame spacing in between cosecutive frames  
  
最終的なドライビングシーンは、(x<sub>i</sub>, a<sub>i</sub>)  
x<sub>i</sub> : images  
a<sub>i</sub> : action vectors  

#### Neighborhood Metric Learning
[4]を参考にした 。要リンク  
・上記手法を、拡張子、BDD-Vに適用した  
  
・Resnet18 を使用  
・instance-based learningをした  
・128 dunetuibak feature vector  
・non-parametctic Softmax classification [5]  
  
・resnetに合わせるために、video size を 224x224に修正  
・top-Kで評価  
・action probability vecotorは、 go straight, stop or slow, turn left, turn right  
・action probability vecotorは、Resnet-backboneのsecond layer outputにconcatenate  
　・vectorは、28x28に拡張される
