from scipy.io import wavfile
import numpy as np
import os

def convert_to_mono(input_file, output_file):
    """
    将音频文件转换为单声道（Mono）。
    如果是立体声或多声道，将混合为单声道后保存。
    
    Parameters:
    - input_file: 输入的音频文件路径 (WAV 格式)
    - output_file: 输出的单声道音频文件路径 (WAV 格式)
    """
    try:
        # 加载音频文件
        sample_rate, data = wavfile.read(input_file)
        print(f"Audio loaded: {input_file}")
        print(f"Sample rate: {sample_rate} Hz")
        print(f"Original shape: {data.shape}")
        
        # 检查是否为多声道
        if len(data.shape) > 1:
            print("Audio is multi-channel. Converting to mono...")
            # 多声道情况下，取平均值（混合所有声道）
            data = np.mean(data, axis=1, dtype=data.dtype)
        else:
            print("Audio is already mono.")
        
        # 保存单声道音频到文件
        wavfile.write(output_file, sample_rate, data.astype(data.dtype))
        print(f"Converted audio saved to: {output_file}")
    
    except Exception as e:
        print(f"Error processing audio: {e}")

# 示例调用
if __name__ == "__main__":
    input_path = "hello.wav"  # 输入音频文件路径
    output_path = "hello_mono.wav"  # 输出单声道音频文件路径

    # 检查输入文件是否存在
    if not os.path.exists(input_path):
        print(f"Input file not found: {input_path}")
    else:
        convert_to_mono(input_path, output_path)
