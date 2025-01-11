import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def plot_spectrogram(audio_path):
    """
    显示音频文件的频谱图（Spectrogram）

    参数:
        audio_path (str): 输入音频文件的路径（支持 WAV、MP3 等格式）
    """
    # 加载音频文件
    y, sr = librosa.load(audio_path, sr=None)  # y 是音频信号，sr 是采样率
    print(f"音频加载成功，采样率: {sr}, 时长: {len(y) / sr:.2f} 秒")

    # 计算短时傅里叶变换 (STFT)
    D = librosa.stft(y)  # 计算复数频谱
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)  # 转换为分贝 (dB)

    # 绘制频谱图
    plt.figure(figsize=(10, 6))
    librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='log', cmap='magma')
    plt.colorbar(format='%+2.0f dB')
    plt.title("Spectrogram (dB)")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.tight_layout()
    plt.show()

# 示例用法
audio_file = input("输入音频路径") 
plot_spectrogram(audio_file)
