from pydub import AudioSegment

def overlay_audio(audio_file_1, audio_file_2, output_file):
    """
    将两个音频文件叠加在一起，长度以较短的音频为准（截断较长的音频）。
    
    - audio_file_1: 第一个音频文件路径。
    - audio_file_2: 第二个音频文件路径。
    - output_file: 输出的叠加音频文件路径。
    """
    try:
        # 加载两个音频文件
        audio1 = AudioSegment.from_file(audio_file_1)
        audio2 = AudioSegment.from_file(audio_file_2)

        # 对齐长度，以较短的音频为基准
        min_length = min(len(audio1), len(audio2))
        audio1 = audio1[:min_length]  # 截断第一个音频
        audio2 = audio2[:min_length]  # 截断第二个音频

        # 叠加音频（混音）
        mixed_audio = audio1.overlay(audio2)

        # 保存叠加后的音频
        mixed_audio.export(output_file, format="wav")
        print(f"叠加完成，输出文件保存在: {output_file}")

    except Exception as e:
        print(f"音频叠加出错: {e}")

# 示例调用
if __name__ == "__main__":
    audio_1 = "hello.wav"  # 第一个音频文件路径
    audio_2 = "fan.wav"  # 第二个音频文件路径
    output = "hello_fan_mixed.wav"  # 输出文件路径

    overlay_audio(audio_1, audio_2, output)
