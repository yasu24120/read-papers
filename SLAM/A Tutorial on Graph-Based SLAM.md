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
　・環境変数：x<sub>1:T</sub> = {x<sub>1</sub>, . . . , x<sub>T</sub> }  
　・観測したオドメトリ：u<sub>1:T</sub> = {u<sub>1</sub>, . . . , u<sub>T</sub> }  
　・観測した環境：z<sub>1:T</sub> = {z<sub>1</sub>, . . . , z<sub>T</sub> }  
・SLAMは下記を求める:  
![image](https://user-images.githubusercontent.com/30098187/81771423-e235fa80-951d-11ea-970e-719f34d293e3.png)  
