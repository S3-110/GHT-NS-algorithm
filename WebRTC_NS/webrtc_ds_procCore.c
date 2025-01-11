void WebRtcNs_ProcessCore(NoiseSuppressionC *self,
                          const int16_t *const *speechFrame,
                          size_t num_bands,
                          int16_t *const *outFrame) {
    // 噪声抑制主函数，输入为多频带语音信号，输出为处理后的语音信号
    // 省略部分变量声明
    

    // 如果多于一个频带，处理高频带
    if (num_bands > 1) {
        speechFrameHB = &speechFrame[1];
        outFrameHB = &outFrame[1];
        num_high_bands = num_bands - 1;
        flagHB = 1;
    }

    // 更新低频缓冲区
    UpdateBuffer(speechFrame[0], self->blockLen, self->anaLen, self->dataBuf);

    // 如果有高频带，更新高频缓冲区
    if (flagHB == 1) {
        for (i = 0; i < num_high_bands; ++i) {
            UpdateBuffer(speechFrameHB[i], self->blockLen, self->anaLen, self->dataBufHB[i]);
        }
    }

    // 计算加窗后的能量
    float energy1 = WindowingEnergy(self->window, self->dataBuf, self->anaLen, winData);
    if (energy1 == 0.0) {
        // 输入信号为零时，直接输出零信号
        for (i = self->windShift; i < self->blockLen + self->windShift; i++) {
            fout[i - self->windShift] = self->syntBuf[i];
        }
        UpdateBuffer(NULL, self->blockLen, self->anaLen, self->syntBuf);

        for (i = 0; i < self->blockLen; ++i)
            outFrame[0][i] = SPL_SAT(32767, fout[i], (-32768));

        if (flagHB == 1) {
            for (i = 0; i < num_high_bands; ++i) {
                for (j = 0; j < self->blockLen; ++j) {
                    outFrameHB[i][j] = SPL_SAT(32767, self->dataBufHB[i][j], (-32768));
                }
            }
        }
        return;
    }

    // 对低频信号进行傅里叶变换
    FFT(self, winData, self->anaLen, self->magnLen, real, imag, magn, NULL, 0, NULL, NULL);

    // 计算维纳滤波器
    ComputeDdBasedWienerFilter(self, magn, theFilter);

    // 对信号进行频域滤波
    for (i = 0; i < self->magnLen; i++) {
        theFilter[i] = fmaxf(fminf(theFilter[i], 1.f), self->denoiseBound); // 限制滤波器范围
        self->smooth[i] = theFilter[i];
        real[i] *= self->smooth[i];
        imag[i] *= self->smooth[i];
    }

    // 反傅里叶变换回时域
    IFFT(self, real, imag, self->magnLen, self->anaLen, winData);

    // 对输出信号进行缩放
    float factor = 1.f; // 缩放因子
    if (self->gainmap == 1 && self->blockInd > END_STARTUP_LONG) {
        // 根据能量比计算缩放因子
        float energy2 = Energy(winData, self->anaLen);
        factor = sqrtf(energy2 / (energy1 + epsilon) + epsilon_squ);
    }

    // 合成信号并输出
    for (i = 0; i < self->anaLen; i++) {
        self->syntBuf[i] += factor * winData[i] * self->window[i];
    }
    for (i = self->windShift; i < self->blockLen + self->windShift; i++) {
        fout[i - self->windShift] = self->syntBuf[i];
    }
    UpdateBuffer(NULL, self->blockLen, self->anaLen, self->syntBuf);

    for (i = 0; i < self->blockLen; ++i)
        outFrame[0][i] = SPL_SAT(32767, fout[i], (-32768));

    // 处理高频带
    if (flagHB == 1) {
        float avgProbSpeechHB = 0;
        float avgFilterGainHB = 0;

        // 计算高频增益调整
        for (i = self->magnLen - 1; i >= self->magnLen / 2; i--) {
            avgProbSpeechHB += self->speechProb[i];
            avgFilterGainHB += self->smooth[i];
        }
        avgProbSpeechHB /= (self->magnLen / 2);
        avgFilterGainHB /= (self->magnLen / 2);

        float gainTimeDomainHB = fmaxf(fminf((avgProbSpeechHB + avgFilterGainHB) / 2.f, 1.f), self->denoiseBound);

        // 应用增益到高频输出
        for (i = 0; i < num_high_bands; ++i) {
            for (j = 0; j < self->blockLen; j++) {
                outFrameHB[i][j] = SPL_SAT(32767, gainTimeDomainHB * self->dataBufHB[i][j], (-32768));
            }
        }
    }
}