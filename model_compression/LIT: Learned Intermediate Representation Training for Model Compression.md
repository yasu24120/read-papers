# LIT: Learned Intermediate Representation Training for Model Compression  
https://cs.stanford.edu/~matei/papers/2019/icml_lit.pdf  
http://github.com/stanford-futuredata/lit-code  
  
## 概要  
Teacher-Student modelで、下記2つのアイデアが盛り込まれている  
1) LIT はteacherとstudent modelの中間表現を直に比較する  
2) Student modelの中間層のinputとして、teacher model (一つ前の層)からの中間表現をinputにする  
　　そうすることで、中間表現の安定性を担保しているらしい  
  
## Contribution  
LITの提案。  
精度を保ったまま2倍以上でmodel compressionができるらしい。  
  
## 本文メモ  
### 1. Intoduction  
・Model compressionはふたつのアプローチがある  
1. Student / teacher model  
2. Deep compression - pruning / factorization / quantization  
  
・本論文では、LITを提案  
　・student/teacher compression  
　　1) LIT はteacherとstudent modelの中間表現の差を元に損失を与える  
　　2) Student modelの中間層のinputとして、teacher model (一つ前の層)からの中間表現をinputにする  
  
![image](https://user-images.githubusercontent.com/30098187/76271391-b8f9b380-62bb-11ea-9568-8cccc6d9bacf.png)  
  
・実験結果のサマリ  
　・LITは精度を損なうことなくmodel compressionできた  
　・ResNetに対する、いくつかのmodel compression手法よりも性能がよかった  
　・knowledge distillationによって、精度があがる先行研究がある。今回も同様だった  
　・LITはハイパフォーマンスで、汎用性があった  
　　・ただし、CNN系のモデルのみかもしれない  
  
### 2. Related Work  
・knowledge distillation  
　・teacherのoutputを小さいstudent modelに学習させる  
　・LITでは、中間表現を有効活用する  
  
・Deep compression  
　・pruning / factorization / quantization  
　・student/teacherほどcompressionできないらしい  
  
・Network architectures for fast inference  
　・mobile netやらshuffle netがあるけど、電源問題で精度が落ちる  
  
### 3. Methods  
・損失関数は以下  
　1) 中間表現のloss  
　2) Knowledge distillationのloss  
  
・Notation  
　・teacher T, student S, input x, true label y  
  
・損失関数  
![image](https://user-images.githubusercontent.com/30098187/76282137-2f0d1300-62da-11ea-8dc6-9002ed423a06.png)  
  
・α, β ∈ [0, 1]  
　・β is an interpolation parameter. GANなどでは β = 0 とした  
  
・Knowlege distillation loss  
　・cross entropy-loss + model のoutputのKL-divergenceが使われることもある  
　・今回  
![image](https://user-images.githubusercontent.com/30098187/76282398-e30e9e00-62da-11ea-8ea7-b4f7d46d0ebc.png)  
  
![image](https://user-images.githubusercontent.com/30098187/76282412-ec980600-62da-11ea-9ef7-5339ff1ed55d.png)  
　・z<sub>i</sub> : inputs to the softmax  
　・τ　:　temperature parameter  
  ・H : cross-entropy loss  
  
・Training via intermediate representations  
  
![image](https://user-images.githubusercontent.com/30098187/76282737-ec4c3a80-62db-11ea-9369-c66c2b2e541c.png)  
  
　・l : 何かしらのloss (L2 lossなど)  
　・T<sub>n</sub>, S<sub>n</sub> : n layer目の中間表現  
  
・Hyperparameter optimization  
　・τ　→　α　→　β　の順で設定した  
  
### 4. Experiments  
#### 4.1. LIT Significantly Compresses Models  
・使ったデータセットとモデル  
![image](https://user-images.githubusercontent.com/30098187/76283375-c6279a00-62dd-11ea-9869-b220c4863efb.png)  
  
・結果  
![image](https://user-images.githubusercontent.com/30098187/76283427-e9524980-62dd-11ea-804b-2884c28b612a.png)  
　・prune % が高ければ、圧縮されている  
  
・GANの結果  
![image](https://user-images.githubusercontent.com/30098187/76283948-4c90ab80-62df-11ea-85d0-05d9ee2f7b03.png)  
・β = 0　でstarGANをcompress  
　・starGAN : 18 convolutional layer, each layer 12 layers (residual layer)  
　　・6 residual blocks -> 2 residual blocksにcompressしたらしい  
