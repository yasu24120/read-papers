# Depth Prediction Without the Sensors: Leveraging Structure for Unsupervised Learning from Monocular Videos
https://arxiv.org/pdf/1811.06152.pdf  
https://sites.google.com/view/struct2depth  

## 概要
単眼カメラから、unsupervisedで深度推定を行う。  
ロボティクスでは、ego-motionの推定も行う。  
ミソは、シーンと各オブジェクトの推定結果に基づくgeometric structureを、learning processに導入。  
具体的には、camera ego-motionとobject motionがmonocular videoのinputから入力される。  

## Contributions  
・Moving object の3D motionsを推定する新しいアプローチの提案。  
　・camera egomotionも推定する  
　・new environmentに適用できる方法の提案  
　　・online refinementを適用する  
・domain transferを行う  

## 本文メモ  

### Problem setup
・Input  
　・Sequences of at least three RGB images  
　　・(I<sub>1</sub>, I<sub>2</sub>, I<sub>3</sub>)∈R<sup>HxWx3</sup>  
　・Camera intrinsics matrix K∈R<sup>3x3</sup>  
  
・デプスとego-motionはニューラルネットワークで学習される  
　・depth function Θ: R<sup>HxWx3</sup> → R<sup>HxW</sup>はfully convolutional encoder-decoder architecture  
　　・出力はデプスマップ D<sub>i</sub> = Θ(II<sub>i</sub>)  
　　・single RGB imageから出力される  
  
・ego-motion ネットワーク：　ψ<sub>E</sub>: R<sup>2xHxWx3</sup> → R<sup>6</sup>  
　・inputは sequence of two RGB images  
　・produces SE3 transform between the frames  
　　・i.e. 6 dimensional transformation vector E<sub>1→2</sub> = ψ<sub>E</sub>(I<sub>1</sub>, I<sub>2</sub>)  
　　・形式は(t<sub>x</sub>, t<sub>y</sub>, t<sub>z</sub>, r<sub>x</sub>, r<sub>y</sub>, r<sub>z</sub>)  
