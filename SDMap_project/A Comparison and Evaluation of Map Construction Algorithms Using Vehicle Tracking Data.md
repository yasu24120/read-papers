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

