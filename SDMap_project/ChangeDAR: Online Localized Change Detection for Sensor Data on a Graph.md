# ChangeDAR: Online Localized Change Detection for Sensor Data on a Graph  
https://bhooi.github.io/changedar/paper.pdf  
https://bhooi.github.io/changedar/  
  
## 概要
グラフ上で、ノードかエッジ上の変化点検出方法を提案。  
contributionは以下の通り:  
1) アルゴリズムの提案。ChangeDAR-S / ChangeDAR-D  
2) Theoretical Guarantees : 上記ふたつのアルゴリズムの理論的な証明  
3) Effectiveness : ChangeDAR は　車両事故/送電線が落ちたことの検出率を、既存手法より75%高くできた(F-measure)  
4) Scalability : ChangeDARは、グラフサイズとサンプル数に応じて、near-linear    

## Contributions

## 本文メモ
### 1 Introduction  
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
  
### 2 RELATED WORK  
・Multivariate change detection  
　・狙いは、時系列情報を２つ以上の領域に分けること  
　　・greedy binary segmentation  
　　・slower but exact dynamic programming(DP)  
　　　・PELT: do pruning step to perform DP in linear time  
　　・他にも、下記があるが、グラフ構造を前提としていないため、localな情報を得ることが出来ない  
　　　・Group Fused Lasso (GFL)  
　　　・Bayesian change detection  
　　　・nonparametric methods  
　　　・information-theoretic methods  
　　　・support vector machines  
　　　・neural networks  
  
・Change Detection in Dynamic Graphs  
　・ Bayesian methods [31], and
distance-based methods, which define a distance metric on graphs:
based on diameter [15], node or edge weights [30, 32], connectivity [24], or subgraphs [
