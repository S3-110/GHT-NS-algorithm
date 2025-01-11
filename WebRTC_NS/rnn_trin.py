# 自定义权重裁剪约束类
class WeightClip(Constraint):
    """权重裁剪，限制权重值在 [-c, c] 范围内，防止梯度爆炸或消失"""
    def __init__(self, c=2):
        self.c = c

    def __call__(self, p):
        return K.clip(p, -self.c, self.c)

# 创建 RNN 模型架构
def build_model():
    # 超参数
    reg = 0.000001  # L2 正则化系数
    constraint = WeightClip(0.499)  # 权重裁剪范围

    # 输入层，形状为 (时间步数, 特征维度)
    main_input = Input(shape=(None, 42), name='main_input')

    # 第一层：特征嵌入（全连接层）
    # 将 42 维输入特征映射到 24 维，激活函数为 tanh
    tmp = Dense(24, activation='tanh', name='input_dense', 
                kernel_constraint=constraint, bias_constraint=constraint)(main_input)

    # 语音活动检测 (VAD) 子网络
    # 使用 GRU 提取时间序列特征，输出 24 维隐藏状态
    vad_gru = GRU(24, activation='tanh', recurrent_activation='sigmoid', return_sequences=True, 
                  name='vad_gru', kernel_regularizer=regularizers.l2(reg), 
                  kernel_constraint=constraint, recurrent_constraint=constraint, 
                  bias_constraint=constraint)(tmp)
    # VAD 输出层，单神经元 sigmoid 激活，用于二分类（是否有语音活动）
    vad_output = Dense(1, activation='sigmoid', name='vad_output', 
                       kernel_constraint=constraint, bias_constraint=constraint)(vad_gru)

    # 噪声特征提取子网络
    # 将 VAD 隐藏状态、输入特征和特征嵌入层输出拼接
    noise_input = concatenate([tmp, vad_gru, main_input])
    # 使用 GRU 提取噪声特征，输出 48 维隐藏状态
    noise_gru = GRU(48, activation='relu', recurrent_activation='sigmoid', return_sequences=True, 
                    name='noise_gru', kernel_regularizer=regularizers.l2(reg), 
                    kernel_constraint=constraint, recurrent_constraint=constraint, 
                    bias_constraint=constraint)(noise_input)

    # 语音降噪子网络
    # 将噪声特征、VAD 隐藏状态和输入特征拼接
    denoise_input = concatenate([vad_gru, noise_gru, main_input])
    # 使用 GRU 提取降噪特征，输出 96 维隐藏状态
    denoise_gru = GRU(96, activation='tanh', recurrent_activation='sigmoid', return_sequences=True, 
                      name='denoise_gru', kernel_regularizer=regularizers.l2(reg), 
                      kernel_constraint=constraint, recurrent_constraint=constraint, 
                      bias_constraint=constraint)(denoise_input)
    # 降噪输出层，22 维向量，sigmoid 激活，对应频带增强系数
    denoise_output = Dense(22, activation='sigmoid', name='denoise_output', 
                           kernel_constraint=constraint, bias_constraint=constraint)(denoise_gru)

    # 构建模型
    # 输入：main_input，输出：denoise_output（语音增强）和 vad_output（语音活动检测）
    model = Model(inputs=main_input, outputs=[denoise_output, vad_output])

    # 编译模型
    model.compile(loss=['mean_squared_error', 'binary_crossentropy'],  # 使用两个不同的损失函数
                  loss_weights=[10, 0.5],  # 设置损失函数权重
                  optimizer='adam')  # 优化器为 Adam

    return model

# 调用模型构建函数
model = build_model()


def build_model():
    # 超参数
    reg = 0.000001  # L2 正则化系数
    constraint = WeightClip(0.499)  # 权重裁剪范围
    # 输入层，形状为 (时间步数, 特征维度)
    main_input = Input(shape=(None, 42), name='main_input')

    # 第一层：特征嵌入（全连接层）
    # 将 42 维输入特征映射到 24 维，激活函数为 tanh
    tmp = Dense(24, activation='tanh', name='input_dense', 
                kernel_constraint=constraint, bias_constraint=constraint)(main_input)

    # 语音活动检测 (VAD) 子网络
    # 使用 GRU 提取时间序列特征，输出 24 维隐藏状态
    vad_gru = GRU(24, activation='tanh', recurrent_activation='sigmoid', return_sequences=True, 
                  name='vad_gru', kernel_regularizer=regularizers.l2(reg), 
                  kernel_constraint=constraint, recurrent_constraint=constraint, 
                  bias_constraint=constraint)(tmp)
    # VAD 输出层，单神经元 sigmoid 激活，用于二分类（是否有语音活动）
    vad_output = Dense(1, activation='sigmoid', name='vad_output', 
                       kernel_constraint=constraint, bias_constraint=constraint)(vad_gru)

    # 噪声特征提取子网络
    # 将 VAD 隐藏状态、输入特征和特征嵌入层输出拼接
    noise_input = concatenate([tmp, vad_gru, main_input])
    # 使用 GRU 提取噪声特征，输出 48 维隐藏状态
    noise_gru = GRU(48, activation='relu', recurrent_activation='sigmoid', return_sequences=True, 
                    name='noise_gru', kernel_regularizer=regularizers.l2(reg), 
                    kernel_constraint=constraint, recurrent_constraint=constraint, 
                    bias_constraint=constraint)(noise_input)

    # 语音降噪子网络
    # 将噪声特征、VAD 隐藏状态和输入特征拼接
    denoise_input = concatenate([vad_gru, noise_gru, main_input])
    # 使用 GRU 提取降噪特征，输出 96 维隐藏状态
    denoise_gru = GRU(96, activation='tanh', recurrent_activation='sigmoid', return_sequences=True, 
                      name='denoise_gru', kernel_regularizer=regularizers.l2(reg), 
                      kernel_constraint=constraint, recurrent_constraint=constraint, 
                      bias_constraint=constraint)(denoise_input)
    # 降噪输出层，22 维向量，sigmoid 激活，对应频带增强系数
    denoise_output = Dense(22, activation='sigmoid', name='denoise_output', 
                           kernel_constraint=constraint, bias_constraint=constraint)(denoise_gru)

    # 构建模型
    # 输入：main_input，输出：denoise_output（语音增强）和 vad_output（语音活动检测）
    model = Model(inputs=main_input, outputs=[denoise_output, vad_output])

    # 编译模型
    model.compile(loss=['mean_squared_error', 'binary_crossentropy'],  # 使用两个不同的损失函数
                  loss_weights=[10, 0.5],  # 设置损失函数权重
                  optimizer='adam')  # 优化器为 Adam

    return model
