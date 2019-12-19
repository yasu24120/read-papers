# ArcFace: Additive Angular Margin Loss for Deep Face Recognition
https://arxiv.org/pdf/1801.07698.pdf    
便利?なページ https://qiita.com/yu4u/items/078054dfb5592cbb80cc  
torch実装 https://github.com/ronghuaiyang/arcface-pytorch/blob/master/models/metrics.py  
  
## 概要  
Face recognition用、metric learning用のloss functionのAdditive Angular Margin Loss (ArcFace)を提案  
・特徴量をl2-normalize  
・列ごとにl2-normalizeしたweightを掛ける  
・特徴量cosθ<sub>i</sub>を作る  
　・要素数:予測クラス数と同じ
　・GTのラベルに対応する要素: cos(θ + m)  
  
![image](https://user-images.githubusercontent.com/30098187/71134475-cfa2e800-2241-11ea-8a6e-d8b0d3cd1297.png)  
  
## Contribution  

## 本分メモ  

