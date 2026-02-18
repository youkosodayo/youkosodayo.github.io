import numpy as np
import matplotlib.pyplot as plt

# --- パラメータ設定 ---
nx = 200          # 空間格子の数
nt = 800          # 1サイクルあたりの時間ステップ数（少し長くしました）
c = 3.0e8         # 光速 [m/s]
dx = 0.01         # 空間解像度 [m]
dt = dx / (2 * c) # 時間解像度

# 物理定数
eps0 = 8.854e-12
mu0 = 1.256e-6

# 可視化の準備
plt.ion()
fig, ax = plt.subplots(figsize=(10, 5)) # 少し横長に見やすく
ax.set_ylim(-1.5, 1.5)
ax.set_xlabel('Grid cell (x) - Space')
ax.set_ylabel('Electric Field (Ez) - Amplitude')
line, = ax.plot(np.zeros(nx), color='blue', lw=2) # 線を少し太く

print("シミュレーション開始：スローモーション版")

# --- メインループ ---
try:
    while plt.fignum_exists(fig.number):
        Ez = np.zeros(nx)
        Hy = np.zeros(nx)

        for t in range(nt):
            # 1. 磁場 Hy の更新
            Hy[:-1] += (dt / (mu0 * dx)) * (Ez[1:] - Ez[:-1])

            # 2. 電場 Ez の更新
            Ez[1:] += (dt / (eps0 * dx)) * (Hy[1:] - Hy[:-1])

            # 3. 波源の挿入
            pulse = np.exp(-0.5 * ((t - 40) / 12)**2)
            Ez[50] += pulse

            # 4. 可視化 (毎ステップ更新し、待ち時間を長く設定)
            # ここで「t % 1」にすることで、すべての計算ステップを表示します
            if t % 1 == 0:
                line.set_ydata(Ez)
                ax.set_title(f"Slow Motion - Time step: {t}")
                
                # --- ここで速度を調整 ---
                # 0.05秒(50ミリ秒)待機。もっと遅くしたい場合は数字を大きくしてください。
                plt.pause(0.01) 
                
                if not plt.fignum_exists(fig.number):
                    break

except KeyboardInterrupt:
    print("中断されました。")

print("シミュレーションを終了しました。")