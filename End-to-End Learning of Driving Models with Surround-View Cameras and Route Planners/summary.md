# End-to-End Learning of Driving Models with Surround-View Cameras and Route Planners
http://www.vision.ee.ethz.ch/~daid/publications/[eccv18]End-to-End-Driving-Surround-View-Route-Planer.pdf

http://people.ee.ethz.ch/~heckers/Drive360/index.html

## 概要  
サラウンドビューカメラ(8台のカメラ)、ルートプランナ、CANバスを使ってステアリングとスピードを推定。  
新しいデータセットも提案した。  
ルートプランナとして、以下のふたつを使用した:  
・OpenStreetMap上での、GPSの軌跡  
・TomTom Go Mobile  
結果は、以下の通り  
・サラウンドビューにしたら精度が上がった。特に市街地と交差点  
・ルートプランナの情報を使うと、ステアリングの精度が上がる  
  
## Contributions  
.driving dataset of 60hours  
　・8台のサラウンドビューカメラ  
　・ルートプランナの情報  
　　・GPSの軌跡  
　　・地図上にルートを図示したもの  
　・GPS-IMU  
  
・上記データから車両の挙動を推定するモデル  

![image](https://user-images.githubusercontent.com/30098187/67160081-f77fe780-f387-11e9-81cc-0063db4b79d1.png)  
  
## 本文メモ  
