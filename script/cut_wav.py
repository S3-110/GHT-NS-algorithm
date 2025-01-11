from scipy.io import wavfile
import numpy as np
import os

def truncate_or_pad_audio(input_file, output_file):
    """
    裁剪音频：跳过第一秒，截取后续的 10 秒，不足 10 秒则补充静音到 10 秒。
    - input_file: 输入音频文件路径 (WAV 格式)。
    - output_file: 输出裁剪后的音频文件路径 (WAV 格式)。
    """
    try:
        # 加载音频
        sample_rate, data = wavfile.read(input_file)
        print(f"Audio loaded: {input_file}")
        print(f"Sample rate: {sample_rate} Hz")
        
        # 计算音频时长
        duration = len(data) / sample_rate  # 音频时长（秒）
        print(f"Original duration: {duration:.2f} seconds")
        
        # 计算第一秒和截断点
        skip_samples = sample_rate * 1  # 第一秒对应的采样点数
        max_length = sample_rate * 10  # 截取 10 秒对应的采样点数
        
        # 裁剪音频
        if duration > 1:
            print("Skipping the first second and processing the next 10 seconds...")
            data = data[skip_samples:]  # 跳过第一秒
        else:
            print("Audio duration is less than 1 second. Processing entire audio.")
        
        # 如果裁剪后不足 10 秒，则填充静音
        if len(data) < max_length:
            print(f"Audio is less than 10 seconds after trimming. Padding with silence...")
            padding = np.zeros(max_length - len(data), dtype=data.dtype)  # 静音补充
            data = np.concatenate((data, padding))
        else:
            # 裁剪到 10 秒
            data = data[:max_length]
        
        # 保存裁剪和填充后的音频
        wavfile.write(output_file, sample_rate, data)
        print(f"Processed audio saved to: {output_file}")
    
    except Exception as e:
        print(f"Error processing audio: {e}")

# 示例调用
if __name__ == "__main__":
    input_path = "fan.wav"  # 输入音频文件路径
    output_path = "fan_processed.wav"  # 输出裁剪后的文件路径

    # 检查文件是否存在
    if not os.path.exists(input_path):
        print(f"Input file not found: {input_path}")
    else:
        truncate_or_pad_audio(input_path, output_path)
