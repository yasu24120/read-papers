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
T ∈ SE(3) : ポーズ。transform moving points from the global reference system (grs) to the camera reference system (crs)  
δ : set of intrinsic camera parameters  
　・focal length / optical centrer / distortion coefficients  
　・システム動作前にこれらは知っておく必要がある  
  
F = {f} を set of framesとする。  
f ∈ F　は scale factor η ∈ (1, ∞) でsubsampledされる。image pyramid  
images は keypoint detector と feature extractor でkeypointなどが抽出される。  
  
**g = {l, u, d}**　　
g : keypoint  
l =∈ N<sub>0</sub> : pyramid level, scale factor η<sup>l</sup>に対応  
u ∈ R<sup>2</sup> : pixel coordinates upsampled to the first pyramid level, l = 0  
d = (d1, . . . , dn) | di ∈ [0, 1] :  keypoint vector  
  
下記セットを持つmapを作成する  
**W = {K,P,M, G, D}**  
K = {k} ⊂ F : keyframe set  
  
P = {p} はset of map pointで  
**p = {x, v, dˆ}**  
x ∈ R<sup>3</sup> : threedimensional position obtained by triangulation from multiple keyframes  
v ∈ R<sup>3</sup> : viewing direction  
d: representative descriptor  
  
各 map point p はいくつかの keyframes kによって観測される  
point p に対応するkeypoints g は複数ある  
  
