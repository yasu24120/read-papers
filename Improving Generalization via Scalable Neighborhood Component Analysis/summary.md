# Improving Generalization via Scalable Neighborhood Component Analysis  
https://arxiv.org/pdf/1808.04699.pdf  
https://github.com/Microsoft/snca.pytorch  

## 概要

## Contributions  
1. Large scale datasetとdeep neural networkに適用できるように、NCAをスケールアップ  
　・augmented memoryを使用(MANN的なmemory?)  
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

Ω<sub>i</sub> = {j|y<sub>j</sub> = y<sub>i</sub>}をx<sub>i</sub>と同じラベルのtraining imagesとしたときに、x<sub>i</sub>が正しく分類される確率は、
![image](https://user-images.githubusercontent.com/30098187/63350368-43b6a780-c398-11e9-940e-175f0aec3219.png)  
