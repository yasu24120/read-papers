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
  
![image](https://user-images.githubusercontent.com/30098187/71135031-c9157000-2243-11ea-9352-57da33338130.png)  
  
・ちなみに、この論文上でのembedding dim は512  
  
## Contribution  

## 本分メモ  
### 1. Introduction
・DCNNのface recognitionには２種類あるが、問題点がある  
　・softmax classifierを用いる系  
　　・(1) 変換行列 W ∈ R<sup>d×n</sup>が nに応じて線形に増加する  
　　・(2) close-set classificationでは、空間上で離れているが、open setに対しては十分でない  
　・embeddingする系(triplet loss)  
　　・(1) large data だと negative samplingの回数が増えて、iterationが増えちゃう  
　　・(2) semi-hard sample mining はそもそも結構難しい  
  
・ArcFaceの概要  
　・DCNNの特徴量と最後の全結合層の内積はcosine距離を表す  
　・arc-cosine functionを用いて、featureとtarget weightの角度を求める  
　・angular marginをtarget angleに足して、target logit をcosine functionを用いて再計算する  
　・全logitを fixed feature normでre-scaleする。  
　・その後はsoftmaxと同様  
  
・利点は以下の通り:  
　・Engaging  
　　・geodestic distance marginを直接最適化できる  
　・Easy  
　　・実装が簡単  
　　・他のloss functionと組み合わせなくても、学習が安定する  
　・Efficient  
　　・コンピュテーショナルコストが、既存手法と比較して増大しない  
  
### 2. Proposed Approach  
#### 2.1. ArcFace  
・softmax functionは以下:  
  
![image](https://user-images.githubusercontent.com/30098187/71137146-74292800-224a-11ea-8c81-19029f2004c5.png)  
  
・下記のとおりとする:  
　・bias b<sub>j</sub> = 0  
　・logit W<sup>T</sup><sub>j</sub> x<sub>i</sub> = ||W<sub>j</sub>|| ||x<sub>i</sub>|| cosθ<sub>j</sub>  
　　・θ<sub>j</sub>: W<sub>j</sub> と feature x<sub>i</sub>のなす角  
　・Individual weight　を l2-normalize　する。i.e. ||W<sub>j</sub>|| = 1  
　・Embedding feature ||x<sub>i</sub>|| を l2 normalizeして s にre-scaleする    
・normalizationはclassificationをangleに基づくものに落とし込める  
・embedding featureは半径sのhypersphere上にマッピングされる  
  
![image](https://user-images.githubusercontent.com/30098187/71137796-a3d92f80-224c-11ea-8112-011a08e41103.png)  
  
・angular margin penalty m を x<sub>i</sub> と W<sub>yi</sub>に加える  
  
![image](https://user-images.githubusercontent.com/30098187/71137882-f4e92380-224c-11ea-989b-7ce17b57d4b4.png)  
  
