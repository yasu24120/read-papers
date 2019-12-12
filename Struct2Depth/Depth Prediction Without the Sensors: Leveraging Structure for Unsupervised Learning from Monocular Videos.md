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
　　・2→3も同様に、E<sub>2→3</sub> = ψ<sub>E</sub>(I<sub>2</sub>, I<sub>3</sub>)  
  
・ある画像から、次の画像のwarp operationは、以下のように解釈が可能  
　・depthがθ(I<sub>i</sub>)で得られる。  
　・次のフレームのego-motion Ψ<sub>E</sub>は次のフレームへの写像として定義できる。  
　・微分可能なimage warping operater φ(I<sub>i</sub>, D<sub>j</sub> , E<sub>i→j</sub> ) → ˆI<sub>i→j</sub>を使えば、どんな画像へも変換可能  
　　・ˆI<sub>i→j</sub>: reconstructed j-th image  
　　・D<sub>j</sub>: corresponding depth estimate  
　　・E<sub>i→j</sbu>: egomotion estimate  
　　・φ : 下記の画像座標Iから、warpingをする関数  
　　　・ˆI<sup>xy</sup><sub>i→j</sub> = I<sup>xˆyˆ</sup><sub>i</sub>
　　　・[ˆx, y, ˆ 1]<sup>T</sup> = KE<sub>i→j</sub> (D<sup>xy</sup><sub>j</sub>·K<sup>−1</sup>[x, y, 1]<sup>T</sup>)  
　　　　・こいつはprojected coordinates  
　・次フレームとのphotometric lossを計算する  
　　・ˆI<sub>i→j</sub>と実際の次のフレーム画像 I<sub>j</sub>を比較  
　　・例えば、reconstruction loss: L<sub>rec</sub> = min(||ˆI<sub>1→2</sub> − I<sub>2</sub>||)  
  
### Algorithm Baseline 
・ベースラインのlossは以下  
　・reconstruction loss : 前後のフレームからの再投影誤差  
![image](https://user-images.githubusercontent.com/30098187/70493650-c2a03d80-1b4b-11ea-98c0-d93c83453ca5.png)  
  
　・ SSIM (a depth smoothness loss) と depth normalization during trainingを行っている  
![image](https://user-images.githubusercontent.com/30098187/70493713-0135f800-1b4c-11ea-8542-2b659b23bfac.png)  
  
### Motion Model

