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
  
![image](https://user-images.githubusercontent.com/30098187/70299622-c6288180-1838-11ea-9f15-6a1c01325876.png)  
  
##### 3.2.2 Clustering Turns  
・ターン種別をクラスタリングする  
　・あらかじめ、ターンの種別を定義しておく i.e. maxで何叉路か？  
・
 
