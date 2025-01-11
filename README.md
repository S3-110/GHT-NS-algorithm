# RNN降噪与WebRTC内置降噪之对比
本项目的广播功能存在严重啸叫与回音问题，本仓库作为课程期末作业，对RNNoise和WebRTC的降噪效果进行对比，试图找到更适合广播功能使用的降噪算法

详细分析与参考资料见：doc/report.pdf

\
|
|-RNNoise -- RNN降噪算法 基于(RNNoise项目)[https://github.com/cpuimage/rnnoise]，编译产物位于 build/bin
|-WebRTC_NS -- 降噪算法 基于(Zhihan Gaode 项目)[https://github.com/cpuimage/WebRTC_NS]，编译产物位于 bin/
|-assets -- 测试中产生的音频文件和相关截图
|-script -- 辅助测试编写的python脚本

