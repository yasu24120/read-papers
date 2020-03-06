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
  
