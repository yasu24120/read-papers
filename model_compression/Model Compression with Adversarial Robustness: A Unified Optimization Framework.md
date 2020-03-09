# Model Compression with Adversarial Robustness: A Unified Optimization Framework  
  
https://papers.nips.cc/paper/8410-model-compression-with-adversarial-robustness-a-unified-optimization-framework.pdf  
https://github.com/shupenggui/ATMC  
  
## 概要  
モデル圧縮技術の論文。  
adversarial attackに対するロバスト性を保持したまま、モデルを圧縮できるか？が観点。  
そのために、Adversarially Trained Model Compression (ATMC) framework を提案。  
ATMCは以下を包括する、効率的なアルゴリズム  
・Pruning  
・factorization  
・quantization  
  
注:ロバスト性をキープしたまま、compressionをかけるので、ロバスト性を高めることは主軸でない  
  
## Contribution
ATMCの提案  
  
## 本文メモ  
  
### 1 Introduction  
  
<b> Background: CNN Model Compression </b>
以下がメインストリームらしい  
・pruning　：　使われていない重みを切る  
・factorization　：　行列計算を、大きな行列計算から、複数の小さい行列計算に分割  
　https://data.gunosy.io/entry/deep-factorization-machines-2018  
・Quantization　：　計算時のビットサイズを低減する e.g. from 32 bits to 8 bits or less  
  
#### 1.1  Adversarial Robustness: Connecting to Model Compression?  
・ロバスト性(adversarial attackに対する強さ)はいつも議論になっているらしい  
・ロバスト性担保のために提案されている手法の例は以下の通り:  
　・hidden gradients  
　・adding stochasticity  
　・label smoothening/defensive distillation  
　・feature squeezing  
  
・モデルcompression も色々提案されているが、accuracy論で、ロバスト性は議論されていない  
  
#### 1.2 Our contribution
・ATMCの提案  
・compression と　ロバスト性の両立された手法はあまり活発でないらしい  
  
### 2 Adversally Trained Model Compression  
・ATMCの問題設定について論じる  
・min-max最適化問題を解く  
  
#### 2.1 Formulating the ATMC Objective: Adversarial Robustness  
・white-box attack を想定する  
・下記のデータセットを想定  
  
![image](https://user-images.githubusercontent.com/30098187/76044699-72941400-5f9e-11ea-9285-f9b08654049a.png)  
 ・x : clean image  
 ・x' : xに何かしらの変更 (add attack magnitude) を加えたimage  
 ・Δ≧0 : predefined bound for the attack magnitude  
   
 ・Attackerの目的関数  
 ![image](https://user-images.githubusercontent.com/30098187/76044853-e2a29a00-5f9e-11ea-86ee-765cab202af0.png)  
・f(θ; x, y) : modelが最小化しようとする損失関数  
・θ : model parameters  
・(x, y): training pairs  
i.e. modelの損失関数を最大化したい  
  
・attackerの目的関数を考慮した上で、model （defendする側）が最小化したい関数  
![image](https://user-images.githubusercontent.com/30098187/76045117-93a93480-5f9f-11ea-9095-057bc60f3c29.png)  
i.e. (x,y)が与えられた時に、(1)を最小化したい(ノイズが加わっても、損失関数が大きくならないパラメータを得たい)  
  
#### 2.2 Integrating Pruning, Factorization and Quantization for the ATMC Constraint  
・pruning / factorization / quantizationを全部導入することを考える  
  
・CNNからDLのモデルを下記とする:  
x<sub>out  = Wx<sub>in</sub>, W ∈ R<sup>m×n</sup>, m ≥ n  
  
・basic pruning : Wを0にする  
・factorization : W = W<sub>1</sub> W<sub>2</sub> にする  
  
・この研究  
![image](https://user-images.githubusercontent.com/30098187/76048370-f2bf7700-5fa8-11ea-9a45-1c38a3d3dac0.png)  
・k :　ハイパーパラメータ  
・||・||<sub>o</sub> : augment matrix内の、non-zeroの個数  
  
・factorization  
・Wをsparseにする  
　・Cはsparse error  
　・U ∈ R<sup>m×m</sup> (初期値)  
　・V ∈ R<sup>m×n</sup> (初期値)  
  
・pruning  
・channel pruningはWのいくつかの行を0にする  
　・簡単化のため、今回はl<sub>0</sub>normを導入する  
  
・quantization  
・nonuniform quantization strategyを用いる  
　・non-zeroのパラメータは、いくつかの値の集合　という考え方  
 ![image](https://user-images.githubusercontent.com/30098187/76061126-37a5d680-5fc6-11ea-8aac-94b8219f3220.png)  
　・|・|<sub>0</sub> : number of different values except 0 in Matrix  
　　・例: M = [0, 1; 4; 1], |M|<sub>0</sub> = 3, |M|<sub>0</sub> = 2  
　・この研究では、ATMCを下記の制約下の学習で集合を得ようとしている  
![image](https://user-images.githubusercontent.com/30098187/76061763-94ee5780-5fc7-11ea-9255-4b99352e3b27.png)  
　・b : number of representation bits  
  
#### 2.3 ATMC:Formulation  
・θを(re-parameterized)weightとする。Lはlayers  
![image](https://user-images.githubusercontent.com/30098187/76062017-1e058e80-5fc8-11ea-9b85-87344aa37486.png)
  
・目的関数と制約  
![image](https://user-images.githubusercontent.com/30098187/76062093-51481d80-5fc8-11ea-944d-9812ce5091a6.png)  
・kとbはハイパーパラメータ  
　・k: θのスパース具合をコントロール  
　・b: quantization bit をコントロール  
  
#### 2.4 Optimizaiton  
・ADMM optimization frameworkを使用  
・アルゴリズム：　多分ソースコードのほうがわかりやすい  
![image](https://user-images.githubusercontent.com/30098187/76063113-67ef7400-5fca-11ea-875c-19a7219ca390.png)  
  
### 3 Experiments  
#### 3.1 Experimental setup  
・Datasets and benchmark models
![image](https://user-images.githubusercontent.com/30098187/76063633-77bb8800-5fcb-11ea-8f97-134166ce7a36.png)  
    
・Evaluation metrics  
　・良性と敵性データに対するaccuracy  
　・model compression ratio  
  
・ATMC Hyper Parameters  
　・b=32 (32bit) full precision  
　・b=8 (8bit) quantization  
　・その後、kを調整した  
  
・Train settings  
　・PGD attacksを敵性データ作成に使用  
　　・perturbation magnitude ∆  
　　　・MNIST 76  
　　　・他 4  
　　・PGD attack iteration numbers n 16 for MNIST, 7 for other  
  
・Adversarial attack settings  
　・PGD attack, FGSM attack, WRM attack　で評価  
  
#### 3.2 Comparison to Pure Compression, Pure Defense, and Their Mixtures  
下記で比較  
・Non-Adversarial Pruning (NAP)  
　・CNNをpruning(勾配が最大のもののweightのみ保持し、その他をzeroにする。その後、non-zero weightsをfine-tuning)  
　・no defence  
・Dense Adversarial Training (DA)  
　・adversarial trainingをCNNに実施  
　・no compression  
・Adversarial Pruning (AP)  
　・DA →　NAPを実施  
・Adversarial l<sub>0</sub> Pruning (Al<sub>0</sub>)  
　・AP → l<sub>0</sub> projected gradient descentを実施  
・Adversarial Low-Rank Decomposition (ALR)  
　・APと基本的には一緒だが、pruningの代わりに low rank factorizationを実施  
・ATMC (8 bits, 32 bits)  
　・kは実験的に求めたっぽい  
   
 ![image](https://user-images.githubusercontent.com/30098187/76182816-afb00e80-6209-11ea-8a84-abfdb07c520d.png)  
   
・結果からわかること  
　・ナイーブなcompressionだと、敵性データにすごく弱くなる  
　・low model size (high compression)だと、ATMCが一番良い  
　・compression後でも、DAに近い値を叩き出すことが可能  
　・ATMC-8bitでも割と良い性能が出る  

・色々なattackに対する性能  
  
![image](https://user-images.githubusercontent.com/30098187/76200369-dafc2300-6234-11ea-9c06-f31f9a930b83.png)  
  
