import math
import torch, torchvision, torchaudio
print("PyTorch:", torch.__version__)
print('Torchvision:', torchvision.__version__)
print("CUDA 可用?:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU 数量:", torch.cuda.device_count())
    print("当前 GPU:", torch.cuda.get_device_name(0))
    print("cuDNN 版本:", torch.backends.cudnn.version())
# macOS Apple 芯片可测 MPS：
print("MPS 可用?:", torch.backends.mps.is_available() if hasattr(torch.backends, "mps") else "N/A")

import torch
from torch import nn

device = (
    "cuda" if torch.cuda.is_available()
    else ("mps" if hasattr(torch.backends, "mps") and torch.backends.mps.is_available() else "cpu")
)

# 人工数据: y = 3x + 2 + 噪声
N = 2048
x = torch.linspace(-1, 1, N, device=device).unsqueeze(1)
true_w, true_b = 3.0, 2.0
y = true_w * x + true_b + 0.1 * torch.randn_like(x)

# 模型: 单层线性
model = nn.Sequential(nn.Linear(1, 1)).to(device)
loss_fn = nn.MSELoss()
optim = torch.optim.SGD(model.parameters(), lr=0.1)

for step in range(201):
    optim.zero_grad()
    pred = model(x)
    loss = loss_fn(pred, y)
    loss.backward()
    optim.step()
    if step % 40 == 0:
        w = model[0].weight.item()
        b = model[0].bias.item()
        print(f"step={step:3d}  loss={loss.item():.6f}  w≈{w:.3f}  b≈{b:.3f}")

# 训练结束，打印最终参数
w = model[0].weight.item()
b = model[0].bias.item()
print(f"learned: y = {w:.3f} x + {b:.3f}  (true: 3.0, 2.0)")
