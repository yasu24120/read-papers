# An Automatic Method for Detection and Update of Additive Changes in Road Network with GPS Trajectory Data
https://www.mdpi.com/2220-9964/8/9/411/htm

## 概要
Low quality trajectory data (GPS) から変化点を検出する。  
以下のステップで検出を行う。  
1. Point-to-segment matching algorithmで新規道路を検出する。  
2. Decomposition-combination map generation algorithm で、新規道路のgeometric structureで構築する。  
3. 新規道路をrefineしてmergeする。 

![image](https://user-images.githubusercontent.com/30098187/69318641-f391fe80-0c80-11ea-9b93-80a766494272.png)  
  
## 本文メモ
### Related work  
・Map updating は以下のふたつの種類にわけられる:  
　(1) global reconstruction methods  
 　　・道路ネットワーク全体が、raw GPS trajectoryから作られて、差分を逐次検出しながらアップデートをかけていく  
 　　・さらに、以下の4カテゴリにわけられる：  
　　　　・I. Density image skeleton extraction  
　　　　　・1. raw GPS trajectoryをdensity imageに変換  
　　　　　・2. skeleton extractionを使って、中心線を検出する。  
　　　　　　・Voronoi partitioning / mathematical morphology / Morse theory を用いて中心線を検出  
　　　　　・処理速度が高いけど、local informationが落ちるらしい  
　　　　・II. Point clustering  
　　　　　・1. K-meansやらでGPSサンプルをクラスタリング  
　　　　　・2. クラスタ中心を求めて、それをつなぐことでネットワークを生成する  
　　　　　・クラスタ数がハイパーパラメータなので、その辺のチューニングが難しいらしい  
　　　　・III. Incremental track insertion  
　　　　　・道路ネットワークをグラフとして定義して、GPS軌跡を逐次マージしていく  
　　　　　・表現するアルゴリズムはいろいろある  
　　　　　・複雑な道路形状を生成できるが、ノイズに弱く、間違ったネットワークを生成する可能性がある  
　　　　・IV. Intersection linking  
　　　　　・1. 交差点を検出する  
　　　　　・2. 交差点をつなぐような、road segmentを生成する  
　　　　　・CellNetなるものがあるらしい  
  
　(2) local additive update methods  
　　・既存道路との差分を検出して、既存道路に情報を足していく  
　　　・Zhao et al. : 既存道路にバッファを設けて、バッファ外のGPS情報をadditive roadと定義→binary image化→skeletonを抽出  
　　　・Tang et al. : traffic direction, topology, geometry relationship constraint rulesから  
　　　　　　　　　　　　新しい道路を検出　→ polynomial curve fitting algorithmで中心線を推定する  
　　　・CrowdAtlas : 隠れマルコフモデルを用いたマップマッチングアルゴリズム  
　　　　　　　　　　　 → unmatchedな軌跡をクラスタリングして、中心線を検出する  
　　　　・なお、ノイズにゲロ弱らしい  
　　　・COBWEB : unmatched trajectoryをinputとして、 ‘graph generalization,’ ‘merging,’ and ‘refinement’ を通じて道路を生成  
  

