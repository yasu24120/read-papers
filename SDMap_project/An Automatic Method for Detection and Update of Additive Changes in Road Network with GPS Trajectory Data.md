# An Automatic Method for Detection and Update of Additive Changes in Road Network with GPS Trajectory Data
https://www.mdpi.com/2220-9964/8/9/411/htm  
ISPRS Int. J. Geo-Inf. 2019  

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
　　・https://note.nkmk.me/python-scipy-matplotlib-delaunay-voronoi/  
  
・GT: unmatched points in DT graph {p1, p2, p3, …, pK}  
・global_mean(GT): mean value of the length of all edges in GT  
・global_std(GT) : standard deviation of the length of all edges in GT  
・local_mean(pi) :  mean value of the length of edges linking to the vertex pi directly  
・cut-off value for long edges linking to pi  
![image](https://user-images.githubusercontent.com/30098187/69513908-f5173b80-0f8c-11ea-969d-3c36df72a83f.png)  
  
・cut_off_value(pi)より、edgeの長さがながければ、piを削除する　(Figure 3b)  
  
・以下のステップでクラスタリングを行う(k-means的な感じ)  
　・Step 1: sampling points are sorted and denoted as L = {p(1), p(2), p(3), …, p(K)}  
　　・N(p(1)) ≥ N(p(2)) ≥ N(p(K))  
　　・n: number of sampling points  
　　・N(•): the number of spatial neighbors of a sampling point  
　・Step 2: sampling point p(1)　をnew point clusterの初期値とする。C = {p(1)}  
　　・p(1)に隣接する点を、以下の条件を満たせば、ひとつずつクラスタCに追加していく  
　　　・条件1: p(k) connects to a sampling point in C by a path of three or fewer edges of the pruned DT graph  
　　　・条件2: the angle between the heading direction of p(k) and the direction of cluster C is less than a threshold Λ (Λ = 15°)  
　　　　・direction of cluster C : median value of the heading directions of all the sampling points in C  
　・Step 3: The point cluster C grows until no neighboring points can be combined  
　　・残りのGPS点について、 maximum number of spatial neighbors を新規クラスタの初期値とする  
　　・全sampling pointsがどこかのクラスタに所属するまで繰り返す  
　　・sampling points 5個未満のクラスタは捨てる  
　・ハイパーパラメータ的なものは Λ のみ (今回は15°)  
  
#### 3.3.2. Road Centerline Extraction  
・piecewise linear curve fitting algorithmを用いて道路中心線を推定する  
https://github.com/cjekel/piecewise_linear_fit_py  
  
### 3.4. Topology Refinement of the Road Network
・トポロジーを修正する。間があいていたりした場合、それを埋める。  
![image](https://user-images.githubusercontent.com/30098187/69517112-18df7f00-0f97-11ea-91ad-644cf26874f4.png)  
  
・mathematical morphology based method を用いる (他にもいろいろある)  
![image](https://user-images.githubusercontent.com/30098187/69517143-37457a80-0f97-11ea-8840-c90f6b974e04.png)  
  
・以下の４ステップで処理を行う  
　・(a) road segmentの始点と終点を、それぞれ thr m伸ばす。  
　　・今回はthr=30  
　　・途中で、他のroad segmentと交差したら、それまで  
　　・他のroad segmentとの距離が20m未満であれば、合体させる(?)   
　・(b) binary imageに変換する。  
　・(c) mathematical thinning operations (Lam et al.) で中心線を検出  
　・(d) 交差点を検出する。  
　　・point connects three or more road segmentsを交差点とする  
　　・Douglas–Peucker algorithm(param = 3 m)を適用して、余分な点を削除する  

### 4. Experimental Results  
#### 4.1. Experiment I: Performance on the Construction of New Roads  
・7つの都市のGPSデータを用いて評価  
  
![image](https://user-images.githubusercontent.com/30098187/69518412-d1f38880-0f9a-11ea-8a26-da9dca49ad03.png)  
・four public GPS trajectory datasets  
　・http://mapconstruction.org/  
　・http://cs.uef.fi/mopsi/routes/network  
・three low-quality taxi GPS trajectory datasets from Wuhan, China.  
![image](https://user-images.githubusercontent.com/30098187/69518915-16cbef00-0f9c-11ea-9a12-457580d1dee4.png)  
　・正解はhttps://www.openstreetmap.org/　のデータを用いた  
  
・6つのアルゴリズムを比較対象とする  
![image](https://user-images.githubusercontent.com/30098187/69518997-4a0e7e00-0f9c-11ea-9e08-89ed5ea5e799.png)  
・実装は以下にある  
　・http://mapconstruction.org/  
  
・評価指標は以下の通り:  
![image](https://user-images.githubusercontent.com/30098187/69519088-7de9a380-0f9c-11ea-8050-22398888c6c8.png)  
  
・シカゴでのデータセットがベンチマーキングとしてよく用いられるらしい  
・結果  
  
![image](https://user-images.githubusercontent.com/30098187/69525528-a200b100-0fab-11ea-8b3f-1918f6187191.png)  
  
![image](https://user-images.githubusercontent.com/30098187/69525583-c52b6080-0fab-11ea-89d7-18ef20598fab.png)  
  
![image](https://user-images.githubusercontent.com/30098187/69525655-f0ae4b00-0fab-11ea-877a-a9ee37408b3a.png)  
  
・シカゴとJoensuuのサンプリングレートを高くしてみた結果  
![image](https://user-images.githubusercontent.com/30098187/69525920-7b8f4580-0fac-11ea-8e46-56e4667cd3f1.png)  
  
![image](https://user-images.githubusercontent.com/30098187/69526049-b6917900-0fac-11ea-8321-b592f3d71b75.png)  
  
#### 4.1.1. Time Complexity
・この研究はOctaveで実装されている  
・速度のベンチマーキング  
　・Intel Core i3 CPUs @3.0 GHz  
　・8 GB of RAM  
　・Windows 7 operating system  
  
![image](https://user-images.githubusercontent.com/30098187/69526260-27389580-0fad-11ea-87c4-a2327de4f026.png)  
  
・CellNetはここ http://cs.uef.fi/mopsi/routes/network/  
  
#### 4.1.2. Parameter Sensitivity  
・パラメータΛをふって、どれくらい影響があるかを検証  
  
![image](https://user-images.githubusercontent.com/30098187/69526433-84cce200-0fad-11ea-86e4-5048d8375194.png)  
  
#### 4.2. Experiment II: Application of the Proposed Method for the Update of the Road Network
・open street mapのupdateに使用してみた  
　・もともとの地図: 2014年版  
　・GPS trajectory data from 6150 taxis on May 1, 2015　を使用  
　　・10,662 trajectories, and the sampling rate varied from 10 to 180 seconds  
  
・検出したクラスタは下記  
![image](https://user-images.githubusercontent.com/30098187/69526670-14729080-0fae-11ea-8227-d0c2a1841aaa.png)  
  
・road networkをアップデートしてみた結果は以下の通り  
![image](https://user-images.githubusercontent.com/30098187/69526880-7df29f00-0fae-11ea-906a-9da03f8fc0ef.png)　
  
・2018年のOSMと比較したら、F-scoreは 0.725  
　・matching distance threshold は 20 m  
　・衛星写真と比較すると、OSMにはない道も、本研究では検出できたらしい  
 
