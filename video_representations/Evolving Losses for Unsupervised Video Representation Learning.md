# Evolving Losses for Unsupervised Video Representation Learning  
https://arxiv.org/pdf/2002.12177.pdf  
https://arxiv.org/pdf/1906.03248.pdf  
  
# 概要  
・multi-modal, multi-task learning problem　として特徴量を学習する  
・特徴量は、違うmodalitiesにdistillationを通じて共有される  
・Loss function evolutionを提案  
  
![image](https://user-images.githubusercontent.com/30098187/76744784-24f68300-67b8-11ea-90ac-25c33e1d2e72.png)  
  
![image](https://user-images.githubusercontent.com/30098187/76809858-8279e680-682f-11ea-9f50-d7f7b7d38d33.png)  

  
# Contribution  
  
# 本分メモ  
## 1. Introduction  
  
## 2. Related works  
  
## 3. Method  
・m : modality  
・I<sub>m</sub> : input  
・E<sub><>/sub : Embedding network。今回は3D convolutionを使ったresnet50  
・i.e. x<sub>m</sub> = E<sub>m</sub>(I<sub>m</sub>)  
 　・x<sub>m</sub> : feature representation for modality m  
・L<sub>m,t</sub> : loss from task t and modality m  
   
・方針としては、distillationで、メインネットワークに知識を注入する  
・loss function  
  
![image](https://user-images.githubusercontent.com/30098187/76816949-e8bd3400-6844-11ea-9db0-90465e70dffa.png)  
・L<sub>d</sub>: distillation losses  
・λ<sub>m,t</sub> , λ<sub>d</sub> : weights of losses, [0,1]  
・Lはentire model を学習するために使用  
  
![image](https://user-images.githubusercontent.com/30098187/76820330-2b373e80-684e-11ea-9cef-e9fe18fb5f88.png)  
・いわゆるlayer間でのL2 loss  
　・main network Mi, layer in another network Li  
  
