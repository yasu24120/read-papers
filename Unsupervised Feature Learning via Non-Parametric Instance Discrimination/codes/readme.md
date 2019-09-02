cloned and modified following codes
https://github.com/zhirongw/lemniscate.pytorch

### 変更点  
・argumentの追加 (含むdefault)  
・pytorchのバージョンに合わせるための処理の変更  
　・longtensor, resize_ -> reshape  

### 各関数の説明  

main.py  
├─ test.py  
├─ lib/NCEAverage.py  
│ 　　　　　　└─ lib/Alias_multinomial.py    
├─ lib/NCECriterion.py  
├─ lib/utils.py  
└─ models/__init__.py    
 　　　　　　└─ models/resnet.py
  
#### main.py  
・imagenet用の学習ファイル  
  
・モデルの作成 or 読み込み　←　ここを変える  
・データの読み込み　←　ここを変える  
・lemniscate と loss functionの定義  
　・NCE Average.pyとNCE Criterion.pyで定義  
・学習  
　・1epochずつ学習し、nearest neighbourで評価。スコアが上回ればmodelを保存  
　　・Resnet, 画像サイズ224x224で1イテレーション3秒、5005イテレーション = 1エポックあたり250分程度  
　　・nvidia-smi -l 1でvolatile GPU utilを監視すると、2秒〜13秒に一度しかGPU計算が行われていない　→　ボトルネックはdata augmentation と推測  

#### cifar.py
・基本的に、main.pyと同様  
　・評価がkNNになった  
 
#### test.py
・評価用関数群  
  
・NNとkNNの実装  
  
#### NCEAverage.py
・論文中のeqn.4 と　eqn.8の実装  
　・添字が違うことに注意  
 
#### NCECriterion.py  
・eqn6. eqn.7の実装  
・論文と若干実装が違う気がしたが、合ってた  
　・loss = - (lnPmtsum + K*lnPonsum) / batchSize　では？  
 　　・cifar10で試したところ、うまく行かず。200 epochでTop1-accuracyが17.4%  
   　・Kを除くと、200 epoch で79.6%  
    　　・1000 epochで80.40。論文通り  
・eqn.9 と eqn.10 (Proximal Regularization)は実装されていない  

## ToDo  
・学習元をBDDに  
・クエリを投げて、画像を返す部分  
・DB部分  
　・保存されているのは学習モデルのみのため  
