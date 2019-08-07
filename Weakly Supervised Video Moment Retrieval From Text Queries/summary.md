# Weakly Supervised Video Moment Retrieval From Text Queries

## 概要
テキストからビデオシーン検索において、training時にfull supervisionが必要となる。  
→とてもコストが高い。  
そこで、weak labelsを用いた学習を行う。(i.e. ビデオの時間範囲でなく、スナップショット的なラベルを用いる)  
Text-Guided Attention(TGA)を用いて、テキストの潜在空間と、ビデオの潜在空間をマッチさせる。  

## 本文メモ
### 問題設定
テキストから、ビデオの
is it possible to develop　
a weakly-supervised framework for video moment localiza-
tion from the text, leveraging only video-level textual anno-
tation, without their temporal boundaries?

### 方法(概要)
Given a video, we first extract frame-wise vi-
sual features from pre-trained Convolutional Neural Net-
work (CNN) architectures. We also extract features for
text descriptions using Recurrent Neural Network (RNN)
based models. Similar to several cross-modal video-text re-
trieval models [5, 15], we train a joint embedding network
to project video features and text features into the same joint
space.
  
Given a certain text description, we obtain its similar-
ity with the video features, which gives an indication of
temporal locations which may correspond to the textual de-
scription. We call this Text-Guided Attention as it helps
to highlight the relevant temporal locations, given a text
description. Thereafter, we use this attention to pool the
video features along the temporal direction to obtain a sin-
gle text-dependent feature vector for a video. We then train
the network to minimize a loss which reduces the distance
between the text-dependent video feature vector and the text
vector itself.

During the testing phase, we use TGA for localizing the moments,
given a text query, as it highlights the portion of the video
corresponding to the query.

Contributions: The main contributions of the proposed
approach are as follows.
• We address a novel and practical problem of tempo-
rally localizing video moments from text queries without
requiring temporal boundary annotations of the text descrip-
tions while training but using only the video-level text de-
scriptions.
• We propose a joint visual-semantic embedding frame-
work, that learns the notion of relevant moments from video
using only video-level description. Our joint embedding
network utilizes latent alignment between video frames
and sentence description as Text-Guided Attention for the
videos to learn the embedding.
• Experiments on two benchmark datasets: DiDeMo [9]
and Charades-STA [8] show that our weakly-supervised ap-
proach performs reasonably well compared to supervised
baselines in the task of text to video moment retrieval.

### problem definition
Problem Definition. In this paper, we consider that the
training set consists of videos paired with text descriptions
composed of multiple sentences. Each sentence describes
different temporal regions of the video. However, we do
not have access to the temporal boundaries of the moments
referred to by the sentences. At test time, we use a sentence
to retrieve relevant portions of the video.

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


