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
