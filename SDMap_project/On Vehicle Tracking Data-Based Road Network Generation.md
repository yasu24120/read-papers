# On Vehicle Tracking Data-Based Road Network Generation
http://www.dieter.pfoser.org/publications/nwcreation_GIS_2012.pdf  
2012  

## 概要


## Contributions

## 本分メモ
### 3. ROAD NETWORK GENERATION  
・GPSの軌跡から地図を生成する  
　・(i) Identify intersections  
　　・車両の進行方向の変化より、曲がったところを交差点とする  
　・(ii) Connection intersections  
　　・intersection間のlinkを軌跡を元に推定  
　・(iii) Reducing network graph  
　　・リンクをマージ？して綺麗にする  
  
#### 3.1 Data
・前提として、道路を G =(V,E)　の有向グラフとして定義する  
　・V : intersection  
　・E : 道  
・GPS、車速、方位を用いる。サンプリング周期は30s  
  
#### 3.2 Turns and Intersections
##### 3.2.1 Indicators
・曲がるときは、減速 / 進行方向が変わる  
　・40km/h　未満で、　15°以上の角度とした。(データから求めたらしい)  
  
![image](https://user-images.githubusercontent.com/30098187/70299582-a1cca500-1838-11ea-8a2c-c57528e2415a.png)  
 
  
##### 3.2.2 Clustering Turns  
・ターン種別をクラスタリングする  
　・あらかじめ、ターンの種別を定義しておく i.e. maxで何叉路か？  
　　・今回は4叉路を対象、ターンタイプを8種類とする  
　　　(・TMI 地図DB仕様に合わせればいいや・・・)  
  
 ![image](https://user-images.githubusercontent.com/30098187/70771705-5de81b80-1db5-11ea-9f33-7b6cb6b28151.png)  
  
・(i) spatial proximilityと (ii)turn similarityに基づいてターンをクラスタリングする  
・agglomerative hierarchical clustering method でクラスタリングする  
　・Fig 4. Line 12.  
　・distance thr=50mとした。実験的に求めた  
  
![image](https://user-images.githubusercontent.com/30098187/70299622-c6288180-1838-11ea-9f15-6a1c01325876.png)  
  
・検出結果例は以下(Fig. 5(a)):  
  
![image](https://user-images.githubusercontent.com/30098187/70771912-3180cf00-1db6-11ea-829b-b48d094a4d5a.png)  

　・O : odd turn types i.e. 右折  
　・X : even turn types i.e. 左折  
　・黄色, オレンジ, 赤, 黒 : (1,2), (3,4), (5,6), (7,8)  
  
##### 3.2.3 Intersections  
・ターンクラスタを交差点にさらにクラスタリングする  
・agglomerative hierarchical clustering method でクラスタリングする  
　・Fig 4. Line 13.  
　・distance thr=25mとした。実験的に求めた。高くするとクラスタ数が少なくなる。  
  
![image](https://user-images.githubusercontent.com/30098187/70299622-c6288180-1838-11ea-9f15-6a1c01325876.png)  
  
　・交差点毎に、以下の情報を保持:  
　　・weight : 交差点が、何個のturnから構成されているか  
　　・permitted maneuvers : どの方向へ曲がることができるか  
  
・Fig 5(b)における '*'が交差点  
  
 #### 3.3 Connecting Intersection Nodes  
 ・Trajectory dataを用いて、交差点間をつなげていく  
   
 ・アルゴリズムは下記:   
 　・ざっくりというと、trajectoryを元に、intersectionを順番につなぐ。最後にlinkをマージする  
![image](https://user-images.githubusercontent.com/30098187/70778955-d4414980-1dc6-11ea-937c-4cd9e44debf3.png)  
  
![image](https://user-images.githubusercontent.com/30098187/70779108-297d5b00-1dc7-11ea-89c3-64ea5693608a.png)  
  
・マージ(trajectoryがどこのintersectionに対応するか)はsweep-line algorithmを用いる (Fig. 7, Lines 8-13)  
・average positionを計算する  
・計算時に以下を格納しておく  
　・(i) weight : link sampleに、何個のtrajectoryが含まれているか  
　・(ii) width : maximum spatial extent of the trajectories  
  
![image](https://user-images.githubusercontent.com/30098187/71069657-83619480-21bc-11ea-9036-121c5e0de03e.png)  
  
#### 3.4 Compacting Links  
(i) sorting existing link samples  
　・Line 1  
(ii) using a buffer region around link samples to determine relevant trajectory portions  
　・Line 6  
　・buffer regionは3.3で算出した値  
　・direction similarityのthrは45°  
(iii) adjusting the geometry of links based on the trajectories’ geometry  
  
・具体的なアルゴリズム  
![image](https://user-images.githubusercontent.com/30098187/71072691-5a440280-21c2-11ea-81b6-9c027b244f00.png)  
  
・バッファリンクとmergeの例  
![image](https://user-images.githubusercontent.com/30098187/71073021-f241ec00-21c2-11ea-8387-411c40ba3c57.png)  
  
#### 3.5 Post Processing  
・ヒューリスティックな処理  
・triangular intersections(いわゆるT字路)へ対応する。以下を導入  
　・relative weight ρ between the weights w<sub>i</sub>, w<sub>j</sub> of two link samples l<sub>1</sub>, l<sub>2</sub>  
　　・defined as ρ<sub>i,j</sub> = w<sub>i</sub>/w<sub>j</sub>  
　　・目的は、l<sub>1</sub>, l<sub>2</sub>, l<sub>3</sub>があった時に、weightのバランスが悪いところを探すこと  
　　　・i.e., ρ<sub>1,2</sub> >> ρ<sub>1,3</sub> ∧ ρ<sub>1,2</sub> >> ρ<sub>2,3</sub>  
  
・triangular intersectionの例  
![image](https://user-images.githubusercontent.com/30098187/71073799-65982d80-21c4-11ea-84f8-bd2679ec19a5.png)  
  
・また、下記の条件を満たす link sample l<sub>k</sub> を除外する  
　・ρ<sub>i,j</sub> > 0.7 ∧ ρ<sub>i,k</sub> > 0.7 ∧ ρ<sub>j,k</sub> < 0.6  
  
### 4. EVALUATION  
・「道路がどれくらい似ているか？」で評価したい  
・下記のstepで評価を行う  
　・1. Tracking dataに対応する実際の地図ネットワークを抽出  
　・2. 出発地・到着地をランダムに選択し、shortest pathを計算する  
　・3. shortest-pathsのsimilarity計算のために、Distinct Fr`echet distance and Average Vertical distanceを計算する  
`  
#### 4.1 Road Network Extraction  
・
![image](https://user-images.githubusercontent.com/30098187/71075086-d5a7b300-21c6-11ea-8a45-8bcfa1cf38fb.png)  
