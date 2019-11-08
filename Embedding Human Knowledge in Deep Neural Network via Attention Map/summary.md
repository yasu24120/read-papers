# Embedding Human Knowledge in Deep Neural Network via Attention Map
https://arxiv.org/pdf/1905.03540.pdf

## 概要  
![image](https://user-images.githubusercontent.com/30098187/68445455-531df200-021d-11ea-9a4b-17ebf068f1c3.png)  
  
・Attention Branch Networkを、教師ありで学習させる研究  
  
### Contributions  
・ABNに、人の知識を反映させる(どこに注視するべきかを教える)。その結果、classificationの精度が向上した。  
・Attention mapの調整をvisual explanationに適用した。その結果、パフォーマンスが向上した。  

## 本文メモ  
### 2. Related work  
#### 2.1 Human-in-the-loop on computer vision  
HITLの先行研究についての紹介。参考文献を後で漁る  

### 3. Investigation of modification of attention map  
・ABNは、attention mapを調整することで、出力を調整している。  
　・このattention mapを手動で調整できないか？  
  
#### 3.1 Modification of attention map  
・Imagenetのclassificationで、ミスをしたサンプルのattention mapを調整し、クラス分類にどう変化があるのかを検証した  
  
![image](https://user-images.githubusercontent.com/30098187/68451367-cd587180-0231-11ea-9ee8-e9491234472a.png)  
　・ミスしたサンプルをネットワークに投入  
　・Attention map (14 x 14)を出力  
　・(224 x 224)にリサイズ  
　・目視で、attentionを修正  
   
![image](https://user-images.githubusercontent.com/30098187/68451683-0a713380-0233-11ea-9696-b469fe96a3c4.png)  
   
・Classificationのエラー率の変化は以下の通り  
![image](https://user-images.githubusercontent.com/30098187/68451747-4a381b00-0233-11ea-94c2-62a965e56576.png)  
   
### 4. Proposed method  
・3つのデータセットを用いた  
　・ImageNet (image classification)  
　・CUB200-2010 (fine-grained recognition)  
　・Indian Diabetic Retinopathy Image Dataset (IDRiD) (medical image recognition)  
  
