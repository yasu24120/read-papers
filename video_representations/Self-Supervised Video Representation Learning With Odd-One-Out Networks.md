# Self-Supervised Video Representation Learning With Odd-One-Out Networks
https://www.zpascal.net/cvpr2017/Fernando_Self-Supervised_Video_Representation_CVPR_2017_paper.pdf  
  
## 概要  
CNNのpre-training technique。self-supervised。  
時系列を混ぜたビデオクリップと、時系列順に画像が並んだビデオクリップを区別させるタスクを解く  
UCF101データセットの行動分類タスクで、この手法でpre-trainしたネットワークを使うと、精度が10%向上したらしい  
  
![image](https://user-images.githubusercontent.com/30098187/76594597-ed2fd700-653c-11ea-8234-171c04f0040e.png)  
  
## Contribution  
手法の提案  

## 本分メモ  
### 1. Intoduction  
・Training example は N + 1 elements (ビデオクリップor画像)  
　・N are similar or related (e.g., correctly ordered set of frames coming from a video)  
　・one is different or odd (e.g., wrongly ordered set of frames from a video)  
 ・N+1 multi-class label classification  
  
### 3. Odd-one-out learning  
・Task  
　・N+1 multi-class label classificationを解く  
　・順番を入れ替えるやつは、ランダムに決定する  
　・関数は下記  
![image](https://user-images.githubusercontent.com/30098187/76596439-84972900-6541-11ea-8e05-014cf6d9885c.png)  
  
・Model  
　・Fig.1 のとおり、video clip encoder の上に5 x conv layer, fc layer～  
　・Fusion layerは以下のふたつ:  
　　・concatenation model : (N + 1) × d dimensional vector  
　　・sum of difference model  
![image](https://user-images.githubusercontent.com/30098187/76597781-99c18700-6544-11ea-8978-dfc2dad42a45.png)  
・o を足し合わせたoutput of fusion layer?  
・v<sub>i</sub> : activation vector of the i-th branch  
![image](https://user-images.githubusercontent.com/30098187/76602099-9aaae680-654d-11ea-9cd6-90817133bb9c.png)  
  
### 4. Learning video representations with O3N  
・サンプリング方法をどうするか？３種類考えた  
![image](https://user-images.githubusercontent.com/30098187/76602284-f1182500-654d-11ea-83b1-bbd1113e71a8.png)  
  
### 5. Video frame encoding  
・3D convolution, recurrent encoders, rank-pooling encoders, concatenate framesなどあるが、どれにでも使える  
  
  
・基本的に、odd-one-outで学習させたネットワークでfine tuningすると、タスクの精度があがるらしい  
