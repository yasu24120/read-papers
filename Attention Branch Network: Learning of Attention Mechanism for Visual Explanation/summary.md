# Attention Branch Network: Learning of Attention Mechanism for Visual Explanation
http://openaccess.thecvf.com/content_CVPR_2019/papers/Fukui_Attention_Branch_Network_Learning_of_Attention_Mechanism_for_Visual_Explanation_CVPR_2019_paper.pdf  
https://github.com/machine-perception-robotics-group/attention_branch_network  

## 概要  
・Activation Mappingを、Attentionとしてネットワーク内に組み込み。  
・Perception branchとAttention branchを用意  
　・Perception branch: 通常のクラス分類を行う  
　・Attention branch: 通常のクラス分類 + perception branch へのweightの調整(attention)を行う  
　　・クラス分類を解かせることによって、supervised mannerでattention部分を学習することができる  
  
![image](https://user-images.githubusercontent.com/30098187/67998732-f199d880-fc9c-11e9-8ad0-bda343982cce.png)  
・上が通常のattention  
・下がproposed  

## Contribution  
  
## 本分メモ  
