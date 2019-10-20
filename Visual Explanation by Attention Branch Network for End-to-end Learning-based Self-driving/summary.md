# Visual Explanation by Attention Branch Network for End-to-end Learning-based Self-driving
http://mprg.jp/data/MPRG/C_group/C20190611_mori.pdf  
  
## 概要  

## Contribution  
・1. ステアリングとスロットルを画像と車速から推定する  
・2. attention mapをを会期問題に適用する  
　・Weighted Global Pooling (WGP) layerを用いる  
・3. Attention mapで可視化した    


## 本文メモ  
### III. Proposed method  
#### A. Steering and throttle controls by adding velocity  
・車速を用いる  
・Fully connected layerに入力する  
・ステリングとスロットルはそれぞれ[-1, 1]に正規化される  
　・ステアリング：　[-1, 0)は左方向、(0,1]は右方向を示す  
　・スロットル：　[-1, 0)は減速、(0,1]は加速を示す  
・output layer v<sup>c</sup> にtanhを適用して推定する  
  
・定式化は以下の通り:  
![image](https://user-images.githubusercontent.com/30098187/66757626-7cc25280-eed7-11e9-8596-b6d07e2151a8.png)  
　・v<sup>c</sup> : 特徴ベクトル  
　・p<sup>c</sup><sub>m</sub>(x;θ) : networkからの出力  
　・t<sup>c</sup><sub>m</sub> : Ground truth  
　・c : カテゴリ、0がステアリング、1がスロットル  
　・M : ミニバッチサイズ  
  
![image](https://user-images.githubusercontent.com/30098187/66757884-1558d280-eed8-11e9-865f-e73f8fa10b83.png)  
  
#### B. Attention mechanism for visual explanation  
・Attention Branch Network (ABN) を導入した  

![image](https://user-images.githubusercontent.com/30098187/66758082-8ac4a300-eed8-11e9-8f3f-97deff65816c.png)  
  
・feature extractor、attention branch、regression branchからなる  

・GAPを使うと、各dimensionのfeature mapの平均をとるため、情報が失われる  
　・なので、WGPを使った  

#### WGPの説明  
![image](https://user-images.githubusercontent.com/30098187/66758303-fa3a9280-eed8-11e9-9f6d-46021b82af37.png)  
  
・WGPは、feature mapと同じサイズのカーネルを用いて、convolutionを行う  
![image](https://user-images.githubusercontent.com/30098187/66758458-4a195980-eed9-11e9-8d2e-0c8dad64a5a2.png)  
　・v : WGPの出力  
　・α: weight for pooling  
　・f(x): feature map  
　・w, h : feature mapのwidth, height  
  
・Attention mapはConv.8から出力される  

・学習時には、regression、attention両方のMSEを足したもの用いる  
![image](https://user-images.githubusercontent.com/30098187/66758818-06731f80-eeda-11e9-9ec9-a8b3564a8a1e.png)  

### IV. Experiments
### IV. Experiments  
・Grand Theft Auto V上でシミュレータを作成した  

![image](https://user-images.githubusercontent.com/30098187/67156868-2afa4c00-f35f-11e9-8e77-25114a25b5a8.png)  
　・画像は420 x 350  
　・RGB  
　・3時間分  
　・学習３万フレーム、検証16556フレーム  
  
・RMS Prop + Gravesで学習  
・LR 0.01  
・decay 0.99  
・batch size 4  
・150 epochs  
  
#### A. Evaluations on control performance  
・autonomy score を用いて評価  

![image](https://user-images.githubusercontent.com/30098187/67156917-a5c36700-f35f-11e9-970e-117982d5d5cd.png)  
　・どれぐらい、運転に人間が介入したか？  
  
・結果は以下の通り:  
![image](https://user-images.githubusercontent.com/30098187/67156992-aad4e600-f360-11e9-9a5d-ed733516f50d.png)  
  ・FC3にvelocityを入れるのが一番良かった  

#### B. Visualization results of the network outpu
・Attention branchを追加した  
![image](https://user-images.githubusercontent.com/30098187/67157267-e40f5500-f364-11e9-9467-1f6b56e32b69.png)  
  
・Visualization maskと比較した  
![image](https://user-images.githubusercontent.com/30098187/67157305-6566e780-f365-11e9-9baa-30a4a0e35370.png)  
　・a: 右折時。センターラインにattention。Sが+  
　・b: 左折時。右ラインにattention。Sが-  
　・c: 停止時。前方車両のストップライトにattention。  
　・d: 追従時。前方車両にattention。  
  
#### C. Caption selection with attention maps
・キャプション生成もしてみた  

・Fully convolutional localization network (FCLN)を用いた  
　・Region Proposal Networkがベースになっている  

![image](https://user-images.githubusercontent.com/30098187/67157425-d8bd2900-f366-11e9-9008-95a46c3d7bf8.png)

