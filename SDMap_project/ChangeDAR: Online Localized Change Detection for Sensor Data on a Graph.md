# ChangeDAR: Online Localized Change Detection for Sensor Data on a Graph  
https://bhooi.github.io/changedar/paper.pdf  
https://bhooi.github.io/changedar/  
  
# 概要
グラフ上で、ノードかエッジ上の変化点検出方法を提案。  
contributionは以下の通り:  
1) アルゴリズムの提案。ChangeDAR-S / ChangeDAR-D  
2) Theoretical Guarantees : 上記ふたつのアルゴリズムの理論的な証明  
3) Effectiveness : ChangeDAR は　車両事故/送電線が落ちたことの検出率を、既存手法より75%高くできた(F-measure)  
4) Scalability : ChangeDARは、グラフサイズとサンプル数に応じて、near-linear    

# Contributions

# 本文メモ
## Introduction  
・変化点はとてもlocalized  
・onlineで検出したい  
  
・Informal Problem 1 (Online Localized Change Detection)  
　・Given  
　　・fixed-topology graph G (e.g. road network or power grid)  
　　・時系列なセンサ情報が、nodes と edgesのサブセット情報としてある  
　　・streaming manner で受信している  
　・Find  
　　・change points  
　　・time t　と localized regionが検出される  
  
・検出結果例は以下 (車両事故の検出) :  
![image](https://user-images.githubusercontent.com/30098187/69528963-a2507a80-0fb2-11ea-9309-9f0cba467f3d.png)  
  
