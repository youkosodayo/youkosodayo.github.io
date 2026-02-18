import numpy as np
import matplotlib.pyplot as plt

# --- パラメータ設定 ---
nx = 200
nt = 2500
c = 3.0e8
dx = 0.01
dt = dx / (2 * c)  # CFL安全側

# 物理定数
eps0 = 8.854e-12
mu0  = 1.256e-6

# --- フィールド（初期化はループの外！） ---
Ez = np.zeros(nx)
Hy = np.zeros(nx)

# --- Mur 1次吸収境界の係数 ---
alpha = (c*dt - dx) / (c*dt + dx)

# Mur用に「前の時刻の端の値」を覚える
Ez_left_old  = 0.0
Ez_right_old = 0.0

# 可視化
plt.ion()
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_ylim(-1.5, 1.5)
ax.set_xlabel('Grid cell (x) - Space')
ax.set_ylabel('Electric Field (Ez) - Amplitude')
line, = ax.plot(Ez, lw=2)

print("Mur吸収境界つきFDTD 開始")

try:
    for t in range(nt):
        # 1) 磁場 Hy 更新（Ezの空間差分）
        Hy[:-1] += (dt / (mu0 * dx)) * (Ez[1:] - Ez[:-1])

        # 2) 電場 Ez 更新（Hyの空間差分）
        Ez[1:] += (dt / (eps0 * dx)) * (Hy[1:] - Hy[:-1])

        # 3) 波源（ガウスパルス）を注入
        pulse = np.exp(-0.5 * ((t - 40) / 12)**2)
        Ez[50] += pulse

        # 4) --- 吸収境界（Mur 1次） ---
        # 左端 i=0
        Ez0_new = Ez[1] + alpha * (Ez[1] - Ez_left_old)
        Ez_left_old = Ez[0]
        Ez[0] = Ez0_new

        # 右端 i=nx-1
        EzN_new = Ez[-2] + alpha * (Ez[-2] - Ez_right_old)
        Ez_right_old = Ez[-1]
        Ez[-1] = EzN_new

        # 5) 可視化
        line.set_ydata(Ez)
        ax.set_title(f"Mur ABC - Time step: {t}")
        plt.pause(0.0005)

        if not plt.fignum_exists(fig.number):
            break

except KeyboardInterrupt:
    print("中断されました。")

print("終了")
