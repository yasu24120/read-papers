# A Tutorial on Graph-Based SLAM  
http://www2.informatik.uni-freiburg.de/~stachnis/pdf/grisetti10titsmag.pdf

## 概要
SLAMのTutorial論文  

## Contributions  
  
## 本分メモ
  
### I. INTRODUCTION  
・問題意識：GPS等が届かない場所でどう自己位置推定するか？   
・SLAMは大別すると2種類ある  
　・Filter-based: カルマンフィルタ、パーティクルフィルタなど  
　・Smoothing  
  
・応用先  
![image](https://user-images.githubusercontent.com/30098187/81770885-80c15c00-951c-11ea-9cc1-4939f0b4f3d3.png)  
  
・生成される地図（いわゆる特徴点マップ）  
![image](https://user-images.githubusercontent.com/30098187/81770977-bf571680-951c-11ea-8b8d-1a9214bde342.png)  
  
### II. PROBABILISTIC FORMULATION OF SLAM  
・ロボットは、よくわからない環境を、走ること仮定する  
　・環境変数(カメラポーズなど)：x<sub>1:T</sub> = {x<sub>1</sub>, . . . , x<sub>T</sub> }  
　・観測したオドメトリ：u<sub>1:T</sub> = {u<sub>1</sub>, . . . , u<sub>T</sub> }  
　・観測した環境：z<sub>1:T</sub> = {z<sub>1</sub>, . . . , z<sub>T</sub> }  
・SLAMは下記を求める:  
![image](https://user-images.githubusercontent.com/30098187/81771423-e235fa80-951d-11ea-970e-719f34d293e3.png)  
  
・マップは複数の表現が可能。下記が例  
　・a set of spatially located landmarks  
　・dense representations like occupancy grids  
　・surface maps  
　・raw sensor measurements  
・2Dマップの例  
![image](https://user-images.githubusercontent.com/30098187/81771883-2970bb00-951f-11ea-96c4-cee7dd3fbbf7.png)  
  
・(1)を求めるために、Markov性を仮定して、ベイジアンネットワークで表現することが多い  
![image](https://user-images.githubusercontent.com/30098187/81771912-50c78800-951f-11ea-8702-fbe99f582b51.png)  
　・Transition model p(x<sub>t</sub> | x<sub>t−1</sub>, u<sub>t</sub>)  
　・Observation model p(z<sub>t</sub> | x<sub>t</sub>, m<sub>t</sub>)  
　　・m : map  
  
・'graph-based' や 'network-based' と呼ばれるらしい  
  
### III. RELATED WORK  
・カルマンフィルタとの組み合わせや、フレームワーク、OSSが紹介されている  
  
### IV. GRAPH BASED SLAM
・  
