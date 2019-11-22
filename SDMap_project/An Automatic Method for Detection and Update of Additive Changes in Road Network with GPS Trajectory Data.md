# An Automatic Method for Detection and Update of Additive Changes in Road Network with GPS Trajectory Data
https://www.mdpi.com/2220-9964/8/9/411/htm

## 概要
Low quality trajectory data (GPS) から変化点を検出する。  
以下のステップで検出を行う。  
1. Point-to-segment matching algorithmで新規道路を検出する。  
2. Decomposition-combination map generation algorithm で、新規道路のgeometric structureで構築する。  
3. 新規道路をrefineしてmergeする。 

![image](https://user-images.githubusercontent.com/30098187/69318641-f391fe80-0c80-11ea-9b93-80a766494272.png)  
  
## 本文メモ
### Related work  
・Map updating は以下のふたつの種類にわけられる:  
　(1) global reconstruction methods  
 　　・道路ネットワーク全体が、raw GPS trajectoryから作られて、差分を逐次検出しながらアップデートをかけていく  
 　　・さらに、以下の4カテゴリにわけられる：  
　　　　・I. Density image skeleton extraction  
　　　　　・1. raw GPS trajectoryをdensity imageに変換  
　　　　　・2. skeleton extractionを使って、中心線を検出する。  
　　　　　　・Voronoi partitioning / mathematical morphology / Morse theory を用いて中心線を検出  
　　　　　・処理速度が高いけど、local informationが落ちるらしい  
　　　　・II. Point clustering  
　　　　　・1. K-meansやらでGPSサンプルをクラスタリング  
　　　　　・2. クラスタ中心を求めて、それをつなぐことでネットワークを生成する  
　　　　　・クラスタ数がハイパーパラメータなので、その辺のチューニングが難しいらしい  
　　　　・III. Incremental track insertion  
　　　　　・道路ネットワークをグラフとして定義して、GPS軌跡を逐次マージしていく  
　　　　　・表現するアルゴリズムはいろいろある  
　　　　　・複雑な道路形状を生成できるが、ノイズに弱く、間違ったネットワークを生成する可能性がある  
　　　　・IV. Intersection linking  
　　　　　・1. 交差点を検出する  
　　　　　・2. 交差点をつなぐような、road segmentを生成する  
　　　　　・CellNetなるものがあるらしい  
  
　(2) local additive update methods  
　　・既存道路との差分を検出して、既存道路に情報を足していく  
　　　・Zhao et al. : 既存道路にバッファを設けて、バッファ外のGPS情報をadditive roadと定義→binary image化→skeletonを抽出  
　　　・Tang et al. : traffic direction, topology, geometry relationship constraint rulesから  
　　　　　　　　　　　　新しい道路を検出　→ polynomial curve fitting algorithmで中心線を推定する  
　　　・CrowdAtlas : 隠れマルコフモデルを用いたマップマッチングアルゴリズム  
　　　　　　　　　　　 → unmatchedな軌跡をクラスタリングして、中心線を検出する  
　　　　・なお、ノイズにゲロ弱らしい  
　　　・COBWEB : unmatched trajectoryをinputとして、 ‘graph generalization,’ ‘merging,’ and ‘refinement’ を通じて道路を生成  
  
・本論文での手法（ざっくりと）  
　・additive updateな手法  
　・以下を使用:  
　　・efficient partial map matching algorithm based on flexible spatial and direction constraint rules  
　　・adopts a decomposition-combination strategy that has no restrictions or assumptions on the road network changes  
　　・adaptive graph-based clustering algorithm  
  
### Methodology  
・ざっくりとしたフローは以下のとおり（再掲）:  
  
![image](https://user-images.githubusercontent.com/30098187/69318641-f391fe80-0c80-11ea-9b93-80a766494272.png)   
  
#### 3.1 Data preprocessing
・道路ネットワークGを、有向グラフとする  
　・直線を繋げたものとする {e1, e2, ..., em}  
　・ vehicle ID, latitude, longitude, timestamp, vehicle heading, and vehicle speedを用いる  
　　・V < 5 km/h or V > 100 km/h　のみを使用  
　　・piecewise-linear interpolationを用いてGPS trajectories (polylines)をset of dense sampling points {p1, p2, …, pn}に変換  
  　　・各samping pointはlatitude, longitude, and heading directionを含む  
　　・本研究では、sampling distance for the interpolation = 50 meters とした  
  
#### 3.2 Detection of Additive Changes  
・road buffers や HMM (隠れマルコフモデル)-based map matching algorithm が道路ネットワーク検出としてよく使われるらしい  
　・この研究では、point-to-segment map matching algorithmを用いる  
　・efficiency and accuracy が良いらしい  
・処理は以下の通り:  
　・(a) sampling pointとroad segmentの距離をすべて計算。thr以上の距離のroad segmentを候補から落とす。  
　・(b) road segmentの角度と、車両の方位角を計算。差がthr以上のroad segmentを候補から落とす。  
　・(c) 候補となるroad segmentのうち、最短距離にマッチングする。候補がなければ、unmatched sampleとする。  
  
![image](https://user-images.githubusercontent.com/30098187/69323850-ca766b80-0c8a-11ea-8e56-03cd46258239.png)  
  
・本研究では、thrを50m, 15°とした  
  
 #### 3.3. Construction of New Roads: A Decomposition-Combination Map Generation Algorithm  
・道路は細かい直線をつなぎ合わせたもの  
　→　decomposition-combination strategyで新規道路の形状を構築する  
・1. unmatched sampling pointsをlinear shapeな cluster化する  
・2. piecewise linear curve fittingでroad segmentの中心線を推定する  
・3. 新規道路をmergeする  
  
 ##### 3.3.1. Decomposition of Complex New Roads
 ・クラスタリングに、k-means, PAM, DBSCANを使うことができるが、本研究では別の方法を使う  
 　・k-means / PAM : パラメータ設定が必要、四角形なクラスタリングに向いていない  
 　・DBSCAN: サンプリングポイントがすくない情報がなくなってしまう  
    
 ・本研究では別のアルゴリズムを使う  
   
 ![image](https://user-images.githubusercontent.com/30098187/69397068-fc89db00-0d27-11ea-971c-92ec71634497.png)  
   
　・Delaunay triangulation (DT)を用いる  
 　・spatial neighbourhood graphをsampling pointから作成する  
  
・GT: unmatched pointsのDT graph  
・
  
