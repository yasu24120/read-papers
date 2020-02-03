# UcoSLAM: Simultaneous Localization and Mapping by Fusion of KeyPoints and　Squared Planar Markers　　
https://arxiv.org/pdf/1902.03729.pdf  
2019/02  

## 概要
UcoSLAMの提案  
Kitti, Euroc-MAV, TUM and SPM でベンチマーキング。他SLAMより性能が良かったらしい。  
ちなみに、Open Visual SLAM (aist)に実装されているらしい。  
  
## Contributions  
・UcoSLAMの良い点  
1. スケールが自動的にわかる  
2. SLAMをonly markers, only keypoints, or a combination of themで使える  
3. ドリフト軽減のためにマーカを使える  

## 本分メモ
  
### 1. Introduction  
・ORB-SLAMなどなどの問題点  
1. スケールがわからん -> ナビゲーションに使いづらい  
2. Rotational movementに弱い  
3. ある程度richなtextureが必要  
4. relocallizationが、 repetitive patterns　や　changes over timeに弱い  
  
なお、Marker系は、Markerが大量に必要なので、Large scale problemsに適用しづらいらしい  
  
・UcoSLAMの良い点  
1. スケールが自動的にわかる  
2. SLAMをonly markers, only keypoints, or a combination of themで使える  
3. ドリフト軽減のためにマーカを使える  
4.   
  
### 3. System Overview  
#### 3.1. System map and notation employed
  
**f = {t, T, δ}**
  
f : A frame captured in time t  
T ∈ SE(3) is the pose from which it was acquired,
which is the transform moving points from the global reference system (grs) to the camera reference system (crs),
and δ is the set of intrinsic camera parameters, comprised
by the focal length, optical centre, and distortion coefficients. The camera intrinsic parameters should be estimated before using the system.
