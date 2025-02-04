import sounddevice as sd
import numpy as np

# 设置录音参数
duration = 5  # 录音时长（秒）
fs = 44100    # 采样率（Hz）

print("开始录音...")
# 录制音频
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)

# 等待录音结束
sd.wait()

print("录音完成!")

# 进行增益处理（例如增大12dB）
gain_factor = 10 ** (20 / 20)  # 30 dB 对应的增益因子
increased_volume_recording = myrecording * gain_factor

# 播放处理后的音频（可选）
print("播放处理后的音频...")
sd.play(increased_volume_recording, samplerate=fs)
sd.wait()  # 等待播放结束

# 保存处理后的音频到文件
from scipy.io.wavfile import write

write('output_audio.wav', fs, increased_volume_recording.astype(np.int16))

print("处理后的音频已保存到 'output_audio.wav'")
