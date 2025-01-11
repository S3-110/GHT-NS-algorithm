import librosa
import soundfile as sf

def resample_wav(input_file, output_file, target_sample_rate=16000):
    """
    将 WAV 文件重采样到目标采样率（48kHz）。

    参数:
        input_file (str): 输入的 WAV 文件路径。
        output_file (str): 保存重采样后的 WAV 文件路径。
        target_sample_rate (int): 目标采样率，默认为 48000 Hz。
    """
    # 加载音频文件
    audio_data, original_sample_rate = librosa.load(input_file, sr=None)
    print(f"原始采样率: {original_sample_rate} Hz")

    # 使用 librosa 重采样到目标采样率
    resampled_audio = librosa.resample(audio_data, orig_sr=original_sample_rate, target_sr=target_sample_rate)
    print(f"目标采样率: {target_sample_rate} Hz")

    # 将重采样后的音频保存为新的文件
    sf.write(output_file, resampled_audio, target_sample_rate)
    print(f"重采样后的音频已保存为: {output_file}")

# 示例用法
input_wav = "hello_fan_mixed.wav"  # 替换为您的输入文件路径
output_wav = "example_resampled_48k.wav"  # 替换为您的输出文件路径
resample_wav(input_wav, output_wav)
