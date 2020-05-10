# A Survey of Simultaneous Localization and Mapping with an Envision in 6G Wireless Networks　　
https://arxiv.org/pdf/1909.05214.pdf  
2020/02  

## 概要
SLAMのサーベイ論文  
Lidar SLAM, Visual SLAMとそのfusionについて調査    

## Contributions  
  
## 本分メモ
  
### I. Introduction  
・歴史としては、Extended Kalman filterがあったが、以下の問題点があった  
　・GPSの誤差  
　・IMUセンサの誤差  
・filter-based slamから、Graph-based SLAMになった  
　・KF →　EKF →　PF → Graph based opt  
  
### II. Lidar SLAM  
・1991はソナー+EKFだったのが、今はLidar SLAMらしい  
  
#### A. Lidar Sensors  
・Lidar は2D と3Dにわかれる  
・Lidarの種類  
　・Mechanical Lidar  
　・hybrid solid-state Lidar e.g. MEMS  
・製品例 :Velodyne, SLAMTEC, Ouster, Quanergy, Ibeo など  
  
#### B. Lidar SLAM System  
##### 1) 2D SLAM  
・Gmapping: Rao-Blackwellisation Partical Filter baseなSLAM。FAST SLAMがベース  
・HectorSlam: 2D SLAM + 3D navigation  
・KartoSLAM: Graph based SLAM  
・LagoSLAM: Graph based SLAM, 非線形、非凸なコスト関数   
・CoreSLAM: 今のところ、minimum lossなSLAMらしい  
・Cartographer: GoogleによるSLAM。3D SLAMにも拡張可能  
  
##### 2) 3D SLAM  
・Loam: real-time method for 3D Lidar. 2D Lidar ver.もある  
・Lego-Loam: Velodyne+IMUが入力。6自由度のpose estimation in real-time, global optimizationする、loop closureで最適化する  
・Cartographer: GoogleによるSLAM  
・IMLS-SLAM: low-driftなSLAM。3D Lidarを使用。scan-to-model matching.  
  
##### 3) Deep Learning With Lidar Systems  
・Feature & Detection
  ・PointNetVLAD: end-to-end training と inferenceを可能にした。マッチする特徴量を検索する  
　・VoxelNet: feature extraction + bounding box predictionをひとつのネットワークで行う  
　・BirdNet: 〃  
　・LMNet: 
