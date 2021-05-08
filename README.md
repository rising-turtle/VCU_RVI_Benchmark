# VCU_RVI_Benchmark
All data sequences are accessible at 
https://vcu-rvi-dataset.github.io/2020/08/14/Dataset-Download/

Implementations of VIO methods to use the benchmark with examples

## 1. Demo
A preview for the data sequences in the benchmark is shown below

<a href="https://youtu.be/sgyO-Rcb7-8" target="_blank"><img src="https://github.com/rising-turtle/VCU_RVI_Benchmark/blob/master/page.png"
alt="VCU_RVI Benchmark demo" width="320" height="240" border="10" /></a>

## 2. Open source of VIO methods to test the data sequences
+ VINS-Fusion: https://github.com/rising-turtle/VINS-Fusion
+ VINS-RGBD: https://github.com/rising-turtle/VINS-RGBD 
+ VINS-Mono: https://github.com/rising-turtle/VINS-Mono

Topics:
+ depth topic: /cam0/depth
+ color topic: /cam0/color
+ imu topic: /imu

## 3. Evaluation 
Ground truths can be downloaded in the 'tools' folder as well as files with helper functions. 
The output files of the helper functions can be used by the evo evaluation tool
https://github.com/MichaelGrupp/evo
