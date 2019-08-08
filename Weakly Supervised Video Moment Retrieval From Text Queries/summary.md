# Weakly Supervised Video Moment Retrieval From Text Queries
https://arxiv.org/pdf/1904.03282.pdf

## 概要
テキストからビデオシーン検索において、training時にfull supervisionが必要となる。
(i.e. ビデオシーンを分割して、アノテーションなど)  
→とてもコストが高い。  
そこで、weak labelsを用いた学習を行う。(i.e. ビデオ+ビデオの説明文複数。テキストはビデオシーンと紐づいていない)  
Text-Guided Attention(TGA)とjoing embeddingを用いて、テキストの潜在空間と、ビデオの潜在空間をマッチさせる。  
  
## Contributions
・時間的境界に基づくアノテーションを必要としない、  
　テキストクエリからのビデオ（シーン）検索手法の提案。  
　(ビデオレベルのアノテーションを使用)  
・joint visual-semantic embedding frameworkの提案。  
　joint embedding networkはビデオの潜在空間とテキストの潜在空間の距離を最小にするように学習する。  
　ビデオの潜在空間は、Text-Guided Attentionによって与えられる。  
・DiDeMoとCharades-STAを用いて評価したところ、supervisedな手法よりもおおむねよかった。
  
## 本文メモ
### 問題設定
ビデオと、時系列で対応してないテキストから、  
ビデオのシーンを抽出できるか？  
  
### 方法(概要)
![figure02](https://user-images.githubusercontent.com/30098187/62625559-6c827a00-b960-11e9-9e7b-8a86806ea082.jpg)
  
ビデオを入力とする。  
frame-wizeな特徴量をpre-trained CNNで抽出。  
テキストの特徴量をRNNで抽出。  
ふたつの特徴空間をjoint embedding（して、ひとつの特徴空間に落とし込む。）  
  
テキストが与えられたときに、対応する可能性のあるビデオの時間が抽出される。  
→ Text Guided Attention  
Attentionを用いて、テキストに対応するビデオのベクタ(text-dependent video feature)を取得する。  
text-dependent video featureとtext vector間の距離を縮めるロスを定義し、学習させる。  
  
テストフェーズでは、テキストをクエリとして投げ、TGAを用いてクエリに対応するビデオの  
一部分をハイライトする。
  
### problem definition
ビデオと、複数の説明文が対応付けられたデータセットを想定。  
各説明文は、ビデオのワンシーンを説明しているが、ビデオの時間的位置は不明。  
テスト時には、テキストからビデオの時間的位置を推定する。
  
### ネットワーク構造
ネットワークは図2のように、ふたつのexpert networkからなる。  
expert networkの最終層は、joint representationsのためにfully connected embedding layersに接続されている。  
★論文では、pre-trained image encoderはfixして、学習しない。  
★fully connected embedding layers, word embedding, GRUはend-to-endで学習される。  
　joint embedding spaceの次元Dを1024とした。  
  
#### テキストの特徴抽出
★GRUを使用。  
★word embeddingの次元は、300とした。(i.e. 単語数→300次元)  

#### ビデオの特徴抽出
Charades-STA：16フレームごと、C3D modelを用いた。
DiDeMo：1フレームごと、16 layer VGG modelを用いた。  
★特徴量は、最終層のひとつ前のFC層から抽出。  
FC層の次元は、両モデルとも4096。  
  
### Text Guided Attention (TGA)
![image](https://user-images.githubusercontent.com/30098187/62668148-ac2f7d00-b9c5-11e9-92b3-95c4681e9464.png)  
D: training set  
n<sub>d</sub> : number of training pairs  
w<sup>i</sup><sub>j</sub> : i<sup>th</sup> 番目のビデオの、 j<sup>th</sup>番目の説明文  
v<sup>i</sup><sub>k</sub> : i番目のビデオの、k番目の時間(time instance)の特徴量  
nw<sub>i</sub> : i番目のビデオの、文章の数  
nv<sub>i</sub> : i番目のビデオの、分割数(time instance)  
注: 文章の並び方は考慮しない  

・各文章は、ビデオのシーンにおいての情報を提供する。  
・fully supervisedの場合：  
　・ビデオのシーンとテキストが、時間的領域に基づいて紐づけられている  
　　→ ビデオをpoolingして、テキストとjoint embedding  
・weakly supervisedの場合：  
　・テキストに対応する、時間的領域が不明  
　　→ テキストクエリに関連するビデオのシーンの抽出が必要  
  
★ ビデオシーンと、テキストの特徴量のjoint embeddingではコサイン類似度を用いた。  
★ 特定のビデオシーンと、対応するテキストの特徴量は特に似ているはず。  
　→ Attentionを用いる。  
  
TGAのために、  
1.ビデオ側のFC層にReLu + Dropout を適用。  
　テキストと同じ特徴空間に落とし込む。 (¯v<sup>i</sup><sub>k</sub>)  
  
2.1.で定義された特徴空間と、テキストの特徴空間のコサイン類似度を計算。  
![image](https://user-images.githubusercontent.com/30098187/62672177-95445700-b9d4-11e9-9b6c-3a99eeaed414.png)  
　j番目の文章とi番目のビデオのk番目のtemporal feature  
  
3.CNNからの特徴空間とテキストの特徴空間の類似度を計算し終えたら、softmaxを用いて、  
　i番目のビデオのattention vectorを計算する。  
![image](https://user-images.githubusercontent.com/30098187/62674936-9333c580-b9df-11e9-9238-e42662b47f03.png)  
　sentence vector w<sup>i</sup><sub>j</sub>に対応するtemporal locationsでは高い値を出力するはず。  
  
4.Attentionの結果を用いて、ビデオの最終的な特徴ベクトルを得る。  
![image](https://user-images.githubusercontent.com/30098187/62682895-2842b880-b9f8-11e9-86a5-22aff049b5d4.png)  

![image](https://user-images.githubusercontent.com/30098187/62687480-d3a43b00-ba01-11e9-845f-f6f118e702b6.png)

### Joint embeddingの学習
i: video number  
j: sentence index  
k: time instant  
ビデオの特徴ベクタf (∈R<sup>V</sup>)とテキストの特徴ベクタw(∈R<sup>T</sup>)とすると、  
fからjoint spaceへの射影は  
v<sub>p</sub> = W<sup>(v)</sup>f (v<sub>p</sub> ∈ R<sup>D</sup>)  
wからjoint spaceへの射影は  
t<sub>p</sub> = W<sup>(t)</sup>w (t<sub>p</sub> ∈ R<sup>D</sup>) 　
ここで、W<sup>(v)</sup>∈ R<sup>DxV</sup>とW<sup>DxT</sup>は、行列  
  
ロスL<sub>VT</sub>は以下の通り:  
![image](https://user-images.githubusercontent.com/30098187/62685394-89b95600-b9fd-11e9-9c80-2609d887e2a8.png)  
t<sup>−</sup><sub>p</sub> : ビデオのembedding v<sub>p</sub>にマッチしない、テキストembedding  
t<sub>p</sub> :マッチするテキストembedding  
v<sup>−</sup><sub>p</sub> : テキストのembedding t<sub>p</sub>にマッチしない、ビデオembedding  
v<sub>p</sub> :マッチするビデオembedding  
Δ : margin value for ranking loss
S(v<sub>p</sub>, t<sub>p</sub>) : joint spaceにおけるvideo embeddingとtext embeddingの類似度を測るscoring function (cosine類似度が良く使われる)  
イメージ  
・第一項：ビデオに対して、マッチするテキストは、マッチしないテキストより近くしたい  
・第二項：テキストに対して、マッチするビデオは、マッチしないビデオより近くしたい  

### Batch-wise training
・SGDを使って学習した  
・元データセット：  
　・ビデオに対して、複数の説明文  
・学習用データセット :  
　・複数の、ビデオ-テキストのペアを作成  
　・同じビデオに対して、違うテキストを付与  
・v<sup>-</sup><sub>p</sub>, t<sup>-</sup><sub>p</sub>は、データバッチで正でないすべてのインスタンスに対応  

### 実験
#### データセットの概要
・Charades-STA  
　・text to video用データセット  
　・16,128 sentence-moment pairs: 12,408 training / 3,720 testing  
　・activity annotation と video-level paragraph description　が含まれている  
・DiDeMo  
　・Flickrからビデオが収集されている。max 30秒にトリミングされている。    
　・アノテーションのため、5秒ごとに裁断されている。  
　・8395 training / 1065 validation / 1004 testing  
　・26892シーンに、複数のテキストがアノテーションされている。  
　・camera movement, temporal transition indicators, activitiesが含まれている  
　・各テキストは、single momentに対応するようにされている。  
  
#### Evaluation metric
・R@K (Recall at K) を使用  
　・クエリが投げられたときに、top-Kに正しい結果が得られる割合  
　・R@1 / R@5 / R@10 を使用  
・temporal intersection over union (tIoU) for Charades-STA  
・mean intersection over union (mIoU) for DiDeMo  

### Implemetation details
・Telsa K80 GPUs  
・PyTorch  
・学習率 0.001  
　・15 epoch分はfixする  
　・15 epochごとに1/10倍する  
・0.1 ≦ Δ ≦ 0.2  
　・Charades-STA: 0.1  
　・DiDeMo: 0.2
・batch-size: 128  
・ADAM optimizer for training joint embedding network  

### 結果
・Charades-STA  
![image](https://user-images.githubusercontent.com/30098187/62689461-d012b300-ba05-11e9-8aae-36cc13377636.png)

・DiDeMo  
![image](https://user-images.githubusercontent.com/30098187/62689518-ecaeeb00-ba05-11e9-8b1c-e195a6ad4756.png)

![image](https://user-images.githubusercontent.com/30098187/62689620-2253d400-ba06-11e9-84a0-9d1ead309347.png)
