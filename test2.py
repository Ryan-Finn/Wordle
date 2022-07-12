import torch
from gpuparallel import GPUParallel, delayed


def perform(idx, device_id, **kwargs):
    tensor = torch.Tensor([idx]).to(device_id)
    return (tensor * tensor).item()


result = GPUParallel(n_gpu=2)(delayed(perform)(idx) for idx in range(5))
print(list(result))
