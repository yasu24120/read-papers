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
・
