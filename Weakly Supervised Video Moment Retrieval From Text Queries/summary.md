# Weakly Supervised Video Moment Retrieval From Text Queries
https://arxiv.org/pdf/1904.03282.pdf

## 概要
テキストからビデオシーン検索において、training時にfull supervisionが必要となる。  
→とてもコストが高い。  
そこで、weak labelsを用いた学習を行う。(i.e. ビデオの時間範囲でなく、スナップショット的なラベルを用いる)  
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

Network Structure. The joint embedding model is
trained using a two-branch deep neural network model, as
shown in Fig. 2. The two branches consist of different ex-
pert neural networks to extract modality-specific represen-
tations from the given input. The expert networks are fol-
lowed by fully connected embedding layers which focus on
transforming the modality-specific representations to joint
representations. In this work, we keep the pre-trained im-
age encoder fixed as we have limited training data. The
fully-connected embedding layers, the word embedding, the
GRU are trained end-to-end. We set the dimensionality (D)
of the joint embedding space to 1024.

Text Representation. We use Gated Recurrent Units
(GRU) [4] for encoding the sentences. GRU has been very
popular for generating a representation for sentences in re-
cent works [6, 15]. The word embeddings are input to the
GRU. The dimensionality of the word embeddings is 300.

Video Representation. We utilize pre-trained convolu-
tional neural network models as the expert network for en-
coding videos. Specifically, following [8] we utilize C3D
model [33] for feature extraction from every 16 frames of
video for the Charades-STA dataset. A 16 layer VGG model
[30] is used for frame-level feature extraction in experi-
ments on DiDeMo dataset following [9]. We extract fea-
tures from the penultimate fully connected layer. For both
the C3D and VGG16 model, the dimension of the represen-
tation from the penultimate fully connected layer is 4096.

### Text Guided Attention (TGA)
we have a training
set D = {{wi
j}nwi
j=1, {vi
k}nvi
k=1}nd
i=1, where nd is the num-
ber of training pairs, wi
j represents the jth sentence feature
of ith video, vi
k represent the video feature at the kth time
instant of the ith video, nwi and nvi are the number of sen-
tences in the text description and video time instants for the
ith video in the dataset. Please note that we do not consider
any ordering in the text descriptions.

Each of the sentences provides us information about a
certain part of the given video. In a fully supervised setting,
where we have access to the temporal boundaries associ-
ated with each sentence, we can apply a pooling technique
to first pool the relevant portion of the video features and
then use a similarity measure to learn a joint video segment-
text embedding. However, in our case of weakly supervised
moment retrieval, we do not have access to the temporal
boundaries associated with the sentences. Thus, we need to
first obtain the portions of the video which are relevant to a
given sentence query.

If some portion of the video frames corresponds to a
particular sentence, we would expect them to have simi-
lar features. Thus, the cosine similarity between text and
video features should be higher in the temporally relevant
portions and low in the irrelevant ones. Moreover, as the
sentence described a part of the video rather than individual
temporal segments, the video feature obtained after pooling
the relevant portions should be very similar to the sentence
description feature. We employ this idea to learn the joint
video-text embedding via an attention mechanism based on
the sentence descriptions, which we name Text-Guided At-
tention (TGA).

We first apply a Fully Connected (FC) layer with ReLU
[18] and Dropout [32] on the video features at each time in-
stance to transform them into the same dimensional space as
the text features. We denote these features as ¯vi
k. In order to
obtain the sentence specific attention over the temporal di-
mension, we first obtain the cosine similarity between each
temporal feature and sentence descriptions. The similarity
between the jth sentence and the kth temporal feature of
the ith training video can be represented as follows,
si
kj =
wi
j
T
vi
k
||wi
j ||2||vi
k||2
(1)
Once we obtain the similarity values for all the temporal
locations, we apply a softmax operation along the temporal
dimension to obtain an attention vector for the ith video as
follows,
ai
kj =
exp(si
kj)
Pnvi
k=1 exp(si
kj)
These should have high values at temporal locations
which are relevant to the given sentence vector wi
j. We
consider this as local similarity because the individual tem-
poral features may correspond to different aspects of a sen-
tence and thus each of the temporal features might be a bit
scattered away from the sentence feature. However, the fea-
ture obtained after pooling the video temporal features cor-
responding to the relevant locations should be quite similar
to the entire sentence feature. We consider this global sim-
ilarity. We use the attention in Eqn. 2 to obtain the pooled
video feature for the sentence description wi
j as follows,
fi
j =
nvi
X
k=1
ai
kjvi
k (3)

### 学習
For the sake of notational simplicity, we drop the index
i, j, k denoting the video number, sentence index and time
instant. Given a text-specific video feature vector based on
TGA, f (! RV ) and paired text feature vector w (! RT ),
the projection for the video feature on the joint space can
be derived as vp = W(v)f (vp ! RD). Similarly, the pro-
jection of paired text vector in the embedding space can be
expressed as tp = W(t)w(tp ! RD). Here,W(v) ! RD×V
is the transformation matrix that projects the video content
into the joint embedding and D is the dimensionality of
the joint space. Similarly, W(t) ! RD×T maps input sen-
tence/caption embedding to the joint space.

Using these pairs of feature representation of both videos
and corresponding sentence, the goal is to learn a joint em-
bedding such that the positive pairs are closer than the neg-
ative pairs in the feature space. Now, the video-text loss
function LV T can be expressed as follows,
LV T = X
(vp,tp)
nX
t−
p
max⇥0,! − S(vp, tp) + S(vp, t−
p )⇤
+ X
v−
p
max⇥0,! − S(tp, vp) + S(tp, v−
p )⇤o
where t−
p is a non-matching text embedding for video em-
bedding vp, and tp is the matching text embedding. This
is similar for video embedding vp and non-matching im-
age embedding v−
p . ! is the margin value for the ranking
loss. The scoring function S(vp, tp) measures the similar-
ity between the image embedding and text embedding in the
joint space. We utilize cosine similarity in the representa-
tion space to compute similarity.

### Batch-wise training
We train our network using Stochastic Gradient Descent
(SGD) by dividing the dataset into batches. For a video
with multiple sentences, we create multiple video-sentence
pairs, with the same video, but different sentences in the
corresponding video’s text description. During training, our
method learns to automatically identify the relevant por-
tions for each sentence using the Text-Guided Attention.
The negative instances v−
p and t−
p correspond to all the in-
stances which are not positive in the current batch of data.


