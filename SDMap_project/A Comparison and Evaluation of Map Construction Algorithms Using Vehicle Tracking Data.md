# A Comparison and Evaluation of Map Construction Algorithms Using Vehicle Tracking Data
https://arxiv.org/pdf/1402.5138.pdf  
2014  

## 概要
・サーベイ論文  
・7つの手法を4つのデータセットでベンチマーキングした  
　・mapconstruction.org  
  
## 本分メモ  

### 1 Introduction  
・こんな感じで、車両データから地図をつくる取り組みがいろいろされている  
![image](https://user-images.githubusercontent.com/30098187/69790955-d02dfd00-1206-11ea-8696-b5785e18b8bc.png)  
  
・下記の観点でベンチマーキングした  
　・アルゴリズム  
　・評価指標(4種類の距離)  
　　・Directed Hausdorff distance  
　　・Path-based distance measure  
　　・distance measure based on shortest paths  
　　・graph-samplingbased distance  
　・データセット  
　　・Chicago / Athens / Berlin  
　　・GTはopen street mapから取得可能らしい  
  
・本論文でのmain goalは各アルゴリズムをベンチマーキングできるような、common platform を作ること  
　・基本的に、アルゴリズムは用いているデータに最適化される  
　　・KDE-based　なアルゴリズムの場合、spatial distance的に良い結果がでるが、coverageには対応しづらい　など  
　　　・ノイズっぽいデータをなめらかにしてしまうため  
  
### 2 Map Construction Algorithms  
・input: set of tracks  
　・track: sequence of measurements  
　・measurements : points(x,y座標、緯度経度), timestamp, opt(heading, velocity)を含む  
・output: street map  
  
・どうやってモデル化していくか？  
　・交差点: pointの頂点  
　・edge : 頂点を結ぶpologonal curve  
  
#### 2.1 Related work  
・地図生成は３種類にわけられる  
　・point clustering: k-means, KDEに基づくアルゴリズム  
　・Incremental track insertion  
　・Insertion linking  
  
##### 2.1.1 Point Clustering
・基本的に、クラスタリングして、その結果から線分を求めて、道を推定する  
・Edelkamp and Schr¨odl (17)  
　・input points(+ vehicle measurements)に対してk-meansを行う  
　　・seedsを定義する  
・Guo etal.  
　・GPS tracksを統計分析。2Dガウス分布に従うと仮定。  
　　・error-prone environmentsでは上手く行かない  
・Worrall et al. (42)  
　・位置と方位角に基づいてクラスタリングし、non-linear least-squares fittingでつなげる  
・Agamennoni et al. (2)  
　・machine-learning method for dynamic enviroments (e.g. open-pit mines)  
　・input traces からprinciple curvesを推定する  
・Liu et al. (29)  
　・cluster line segments based on proximity and direction  
　・then use the resulting point clusters and fit polylines  
・KDEもいろいろある  
  
##### 2.1.2 Incremetal Track Insersion  
・逐次、地図にtracksを足していくイメージ  
　・マップマッチングの考え方が使われる  
・Cao and Krumm (11)  
　・distance と directionを用いて地図を更新する  
・Bruntrup et al. (10)  
　・spatial-clustering based algorithm(DBSCAN?)  
・Ahmed and Wenk(4)  
　・Fr´echet distanceを用いてtrackをmapにマッチさせる  
  
##### 2.1.3 Intersection Linking  
・交差点を探して、適当な道路でつなげる  
・Fathi and Krumm (19)  
　・既存の地図から、交差点を検出するdetectorを作成して、交差点を見つけている  
　・大量のデータを用いるが、最終的な性能は良かったらしい  
・Karagiorgou and Pfoser (27)  
　・角度の変化から交差点を検出して、map edgeを軌跡をbundlingすることで作成  
  
#### 2.2 Compared Algorithms 
・比較の対応表  
![image](https://user-images.githubusercontent.com/30098187/69946203-8c046a80-152e-11ea-869e-02ec988c8e86.png)  
  
##### 2.2.1 Ahmed and Wenk (4)
・1. partial map matchingをする。pointsをmatched と unmatchdedに振り分け  
　・variant of the Fr´echet distanceに基づく  
  
![image](https://user-images.githubusercontent.com/30098187/69946913-ddf9c000-152f-11ea-8734-0c679146e255.png)  
  
・2. unmatched pointsを新規道路として定義  
・3. minimum-link algorithmを用いて統合する  
  
##### 2.2.2 Biagioni and Eriksson (8)  
・KDEの出力からskeleton mapを作成する  
  
![image](https://user-images.githubusercontent.com/30098187/69947252-a0496700-1530-11ea-9c64-6a5e0e7ccb7e.png)  
  
##### 2.2.3 Cao and Krumm (11)
・1. simulation of physical attractionを用いて、似ているtracksをひとまとめにする  
　・データが綺麗になるらしい  
・2. 距離と方角に基づいて、edgeやvertexをinsert、merge、addをする  
  
![image](https://user-images.githubusercontent.com/30098187/69947586-47c69980-1531-11ea-80a1-58489a68d6a0.png)  
  
##### 2.2.4 Davies et al. (16)  
・1. セル毎にKDEをする  
・2. bit mapから輪郭を検出する  
・3. Voronoi diagramを用いて輪郭から中心線を求める  
  
![image](https://user-images.githubusercontent.com/30098187/69947874-ece17200-1531-11ea-8764-7b0fac1792b3.png)  
  
##### 2.2.5 Edelkamp and Schr¨odl (17)
