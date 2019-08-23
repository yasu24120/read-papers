# Improving Generalization via Scalable Neighborhood Component Analysis  
https://arxiv.org/pdf/1808.04699.pdf  
https://github.com/Microsoft/snca.pytorch  

## 概要

## Contributions  
1. Large scale datasetとdeep neural networkに適用できるように、NCAをスケールアップ  
　・augmented memoryを使用  
　　・https://www.anlp.jp/proceedings/annual_meeting/2018/pdf_dir/D3-6.pdf  
　・空間は、ノンパラメトリック  
2. ImageNet classificationに対して、kNNでも良い結果が出ることを示した  
3. この手法で学習したembedding空間が、新しいカテゴリへの対応力が高いことを示した  
　・i.e. few-shot learning  
  
## 本文メモ  

### 問題設定  
・新しいカテゴリが出てきた場合、どうするか？  
↓  
・image classification　に対して、neighbourhood approachをとる。  
　・metric learning based on Neighbourhood Componrnent Analysis (NCA) をする。  
　　・NCA: http://www.cs.toronto.edu/~fritz/absps/nca.pdf  
　　・Metric learning: https://copypaste-ds.hatenablog.com/entry/2019/03/01/164155  
　　　・Kaggleのwhale identification challengeにsiamese networkのkeras実装があったはず  
  
ざっくりというと、  
・NCAで、training imageを、class labelを利用して、embedding空間に埋め込む  
・kNN classifierで画像分類  
  
### Approach  
・image x をクエリとして投げ、embeddingに埋め込む i.e. v = f<sub>θ</sub>(x)  
　・f<sub>θ</sub>(・)はパラメータθを持つdeep neural network, データDで学習される。  
・Embedding v は search database D' にクエリとして投げられる  
・Similarity score が一番高い画像が検索される  
  
・ノンパラメトリックな手法を使えば、fine-tuningなしで新しい画像のカテゴリに拡張できる：  
　1. D'=Dの場合 : closed-set recognition. e.g. ImageNet challenge  
　2. D'のアノテーションラベルがDと違う場合 : open-set recognition. sub-category discoveryやfew-shot recognition  
　3. D'にアノテーションがない場合 : 一般的なcontent-based な画像検索に適用できる  
 
#### Neighborhood Content Analysis

##### Non-parametric formulation of classification
・dataset n,  x<sub>1</sub>,x<sub>2</sub>,...,x<sub>n</sub>とラベルy<sub>1</sub>,y<sub>2</sub>,...,y<sub>n</sub>がある  
・x<sub>i</sub>はv<sub>i</sub> = f<sub>θ</sub>(x<sub>i</sub>) でembedされる  

![image](https://user-images.githubusercontent.com/30098187/63350109-c428d880-c397-11e9-88b9-51851e615a9f.png)  

s<sub>ij</sub> : cosine similarity  
v<sub>i</sub>はl<sub>2</sub>normalizedされている  
Φ : v<sub>i</sub>とv<sub>j</sub>のangle  
  
x<sub>i</sub>がx<sub>j</sub>のneighborになる確率は  
![image](https://user-images.githubusercontent.com/30098187/63350200-ee7a9600-c397-11e9-8ef9-d558a8a0a7e0.png)  
σ : scaleを調整するパラメータ  

Ω<sub>i</sub> = { j | y<sub>j</sub> = y<sub>i</sub> }をx<sub>i</sub>と同じラベルのtraining images の indexとしたときに、 
x<sub>i</sub>が正しく分類される確率は、  
![image](https://user-images.githubusercontent.com/30098187/63350368-43b6a780-c398-11e9-940e-175f0aec3219.png)  
  
目的関数は、negative log likelihoodをminimizeすること  
![image](https://user-images.githubusercontent.com/30098187/63350749-f555d880-c398-11e9-969d-fa52e93f57d5.png)  
  
学習は、embeddingを直接最適化することで行われる(parameterを追加しない)。勾配は、  
![image](https://user-images.githubusercontent.com/30098187/63350810-128aa700-c399-11e9-8550-927cb784af41.png)  
  
j≠iのときは  
![image](https://user-images.githubusercontent.com/30098187/63350841-20402c80-c399-11e9-94f5-5dfb6c1b5f9e.png)  
p^<sub>ik</sub> = p<sub>ik</sub>/Σ<sub>j∈Ω<sub>i</sub></sub>  
p<sub>ij</sub> : 正解カテゴリを正規化した分布  

##### Differences from parametric softmax  
普通のparametric softmaxは以下  
  
![image](https://user-images.githubusercontent.com/30098187/63351065-80cf6980-c399-11e9-9bcb-33532445dda4.png)  
  
各カテゴリc∈{1,2,...,C}はparametrized prototype　ω<sub>c</sub>をもつ。  
non-parametricな手法では、単一のprototypeを仮定しないため、柔軟性が高い  

##### Computational challenges for learning
NCAを学習すると、リソースが足りない(データ・セット全体からembedding/勾配を計算する必要がある)ため、以下の対策を行った  
1. Eqn5に対してのみ勾配降下法を適用した  
2. Augmented memory をembeddingに適用した　←こっちがメイン  

![image](https://user-images.githubusercontent.com/30098187/63351563-706bbe80-c39a-11e9-8448-d003cfc79e0f.png)  

#### Learning with Augmented Memory  
[48]によく似ている。  
　・https://github.com/yasu24120/read-papers/blob/master/Unsupervised%20Feature%20Learning%20via%20Non-Parametric%20Instance%20Discrimination/summary.md  
　・違いは、supervisedにして、ラベル毎にmini batchにしている？？  
  
embedding空間を確率的勾配降下法で学習する  
  
・t+1回目のイテレーションでは、パラメータはθ<sup>(t)</sup>を持つ  
・non-parametric memory は M<sup>(t)</sup> = { v<sup>(t)</sup><sub>1</sub>, v<sup>(t)</sup><sub>2</sub>,..., v<sup>(t)</sup><sub>n</sub> }　をもつ  
・イテレーションt終了時に、メモリはパラメータθ<sup>(t)</sup>によって最新とする  
　→non-parametric memory は以下のように近い    
![image](https://user-images.githubusercontent.com/30098187/63557366-678a1100-c583-11e9-9254-fad3fb56255f.png)  
  
・i+1番目の学習では、v<sub>i</sub> = f<sub>θ<sup>(t)</sup></sub>(x<sub>i</sub>)を計算し、Eqn5で勾配を計算する  
![image](https://user-images.githubusercontent.com/30098187/63557523-0e6ead00-c584-11e9-9542-5f50f5c386e5.png)  

・back propagate が可能  
![image](https://user-images.githubusercontent.com/30098187/63557551-2c3c1200-c584-11e9-8eec-be2c5d6673a1.png)  
  
・x<sub>i</sub>に対応するメモリを、empirical weighted averageで更新する  
![image](https://user-images.githubusercontent.com/30098187/63557642-863cd780-c584-11e9-8883-05debeffc270.png)  
　・http://openaccess.thecvf.com/content_cvpr_2017/papers/Xiao_Joint_Detection_and_CVPR_2017_paper.pdf  
  
注: learning rateは低くしておく必要がある  
  
#### Discussion on Compexity
メモリの削減度合いについて  

### Experiments
・ImageNetを用いて評価した  
1. kNN classifierで分類  
2. 荒いアノテーションで、どこまで分類できるかを検証  
3. few-shot recognition  
  
#### Image Clasification 
Parametric softmax classification networkをbaselineとした  
  
#### Network Configuration  

