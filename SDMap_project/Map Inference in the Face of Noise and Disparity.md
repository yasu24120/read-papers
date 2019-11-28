# Map Inference in the Face of Noise and Disparity
https://www.cs.uic.edu/~jakob/papers/biagioni-gis12.pdf  
SIGSPATIAL GIS ’12  
https://www.cs.uic.edu/pub/Bits/Software/gis12_mapinference.tar.gz  

## 概要  
雑なデータから、地図を生成する方法を提案する。  
・雑なデータ: GPS誤差が大きい、通行密度にムラがある etc  

## Contribution  
・hybrid map inference pipelineの提案。雑なデータにも対応できる  
・中心線をグレースケール画像(密度推定結果)から検出する方法の提案  
・軌跡ベースのトポロジ修正方法の提案(edge pruningとintersection merging)  
・軌跡ベースのgeometric refinement technique(交差点の位置補正のため)  
・先行研究との比較  

## 本文メモ  
### 2. A HYBRID MAP INFERENCE PIPELINE
・ざっくりとしたアルゴリズムの説明  

1. Density Estimation  
　・全GPS軌跡をKDE(with Gaussian kernel)する。  
2. Initial Map Generation  
　・提案する、gray-scale skeletonization algorithmを用いて中心線を検出する  
3. Trace Map Matching  
　・Viterbi map matchingを使って、GPS sample point をinitial mapのedgeに対応付ける  
　　・weighted by the mean density beneath each edge  
4. Topology Refinement  
　・マップマッチング結果に応じて、low-confidence edgesを削除 / merge redundant nodes / infer alloable edge transitions  
5. Geometry Refinement  
　・交差点の位置調整/ turn-lanes の反映 / fits road segments  
  
### 3. DENSITY ESTIMATION  
・各GPSデータから、２次元KDEを行う  
　・地図を、1x1メートルのセルで離散化  
　・GPSの誤差は、N(0, σ<sup>2</sup>)で、σ=8.5と仮定  
  
### 4. GRAY-SCALE SKELETONIZATION FOR ROAD CENTERLINE FINDING 
・KDEの結果から、thrを用いるとうまくいかない  
・提案手法  
　・binary skeletonization algorithmを繰り返す  
　　・once per integer density level  
　　・maximum density から始める  
　　・density毎に、枝を追加していくイメージ  
  
![image](https://user-images.githubusercontent.com/30098187/69609795-b60ce700-106d-11ea-8b38-e663390dbf5e.png)  
![image](https://user-images.githubusercontent.com/30098187/69609834-cae97a80-106d-11ea-833a-9b4d4354c7c8.png)  
![image](https://user-images.githubusercontent.com/30098187/69609863-dd63b400-106d-11ea-946b-2ea91c3567ac.png)  
  
#### 4.1 Algorithm Description
・D(x, y) : x, y における密度  
・l ∈ 1 . . . l<sub>max</sub>:レベル  
・T<sub>l</sub> : lにおけるbinary image  
　・T<sub>l</sub>(x, y) = 1 if D(x, y) ≥ l  
・再帰的にskelton images S<sub>l</sub> for level l を生成する  
　・S<sub>l</sub> = skeletonize(T<sub>l</sub> +S<sub>l+1</sub>)  
　・where S<sub>l<sub>max</sub></sub> = skeletonize(T<sub>l<sub>max</sub></sub> )  
・各レベルごとに、フィルタをかけて、線を細くしていく  
　・この部分に関しては、論文の説明よりソースコードのほうがわかりやすい  
 ![image](https://user-images.githubusercontent.com/30098187/69613712-5fa3a680-1075-11ea-8deb-37a2b9b7a494.png)  
   
#### 4.2 Algorithm Intuition  
・直感的にわかりやすく説明してくれているけどよくわからん。コードみたほうが早い  
  
#### 4.3 Performance Optimizations
・並列化できるよ。処理速度があがるよ。  

#### 4.4 Edge Extraction from Skeleton Image
・combustion techniqueを用いてpixelとedgeを対応付ける  
・Douglas-Puecker algorithmを用いて道路を検出する  
  
### 5. DENSITY-AWARE MAP MATCHING  
・initial mapにsampling pointsをマッチングさせる  
　・目的1. nodesとedgeに上限を設けることができる。  
　　・pruningとshift nodes/edgesをしたときに、あやしいedgesの発生を予防できるらしい  
　・目的2. 予めマップマッチングしておくことで、後段の処理が高速化できるらしい  
　・Viterbi’s algorithmを用いてマップマッチングする  
  
### 6. TOPOLOGY REFINEMENT  
・pruningする : マップマッチング結果が1個未満のエッジを消す  
・交差点をマージする  
・edge内でどう移動できるかを検出するための統計情報を付与する  
  
#### 6.1 Pruning Spurious Edges
・マップマッチング結果が1個未満のエッジを消す  
  
・t : 軌跡  
・e : edge  
・n<sup>t</sup><sub>e</sub> : number of traversals τ  of e  
・RMSD(τ, e) < RMSD<sub>max</sub>  
![image](https://user-images.githubusercontent.com/30098187/69617680-e52a5500-107b-11ea-8352-6ca49df49bfb.png)  
・p ∈ τ : GPS points  
・dist : the distance between p and the nearest point on e  
・RMSD(τ, e) < RMSD<sub>max</sub>　をgood matchと定義  
   
・n<sub>e</sub> = Σ<sub>t</sub>n<sup>t</sup><sub>e</sub>がthr未満だったらpruneする  
  
![image](https://user-images.githubusercontent.com/30098187/69618745-bdd48780-107d-11ea-97aa-d2c3980bad61.png)  
  
#### 6.2 Collapsing Nodes into Intersections
・変な形の交差点を補正する  
![image](https://user-images.githubusercontent.com/30098187/69618804-d8a6fc00-107d-11ea-84d1-dcb5284e5d1b.png)  
・ノードを近い順にソートして、(多分)thr未満であれば、平均座標でマージする  
  
#### 6.3 Map Matching Do-Over
・もっかいマップマッチングする  
  
#### 6.4 Detecting Allowable Edge Transitions  
・車両の進行方向を元に、有向グラフ的にしていく  
  
### 7. GEOMETRY REFINEMENT  
・オリジナルの軌跡と矛盾しないように、ジオメトリを修正する  
・k-meansをベースとした手法で修正する  
　・(a) creating an initial guess based on the input map  
　・(b) restricting clustering eligibility  
  
・Initialization  
　・Intersection means と segment meansを作る  
　 ・各intersectionとendpointに、intersection meanをひとつ対応付ける  
　・各road segmentにおいて、[L/m - 2]の数のmeanを作成する。  
　　・L : length of the segment  
　　・m : maximum distance between means  
　　・始点と終点のmeanは削除(intesection meanとして定義済みのため)  
　　・残りはuniformely distributed  
   
・Assignment  
　・各GPS sample を最近傍の eligile mean に割り当てる。  
  
・Update  
　・各meanをずらす  
　・文章からだとよくわからん  


### 9. EVALUATION
#### 9.1 Dataset
・シャトルバスの通行記録  
　・7ヶ月分  
　・13大学  
