import numpy as np
import torch
from torch.utils.tensorboard import SummaryWriter
import os
from datetime import datetime

class Logger:
    def __init__(self, log_dir='runs/experiment'):
        os.makedirs(log_dir, exist_ok=True)
        self.writer = SummaryWriter(log_dir)

    def log_scalar(self, tag, value, step, group=None):
        tag_name = f"{group}/{tag}" if group else tag
        self.writer.add_scalar(tag_name, value, step)

    def log_text(self, tag, lines: list[str], step: int, group=None):
        tag_name = f"{group}/{tag}" if group else tag
        full_text = "\n".join(lines)
        self.writer.add_text(tag_name, full_text, step)

    def log_dict(self, metrics: dict, step: int, group: str = None):
        def recurse(prefix, item):
            if isinstance(item, dict):
                for k, v in item.items():
                    new_prefix = f"{prefix}/{k}" if prefix else k
                    recurse(new_prefix, v)
            elif isinstance(item, list):
                if all(isinstance(x, str) for x in item):
                    self.log_text(prefix, item, step)
                else:
                    for i, v in enumerate(item):
                        recurse(f"{prefix}/{i}", v)
            elif isinstance(item, (float, int)):
                self.log_scalar(prefix, item, step)
            elif isinstance(item, str):
                self.log_text(prefix, [item], step)
            elif isinstance(item, np.ndarray):
                if item.ndim in [2, 3] and (item.shape[-1] in [1, 3] or item.shape[0] in [1, 3]):
                    self.log_image(prefix, item, step)
                else:
                    print(f"[log_dict] Skipped {prefix}: Unsupported ndarray shape {item.shape}")
            else:
                print(f"[log_dict] Skipped {prefix}: Unsupported type {type(item)}")

        recurse(group or "", metrics)

    
    def log_image(self, tag, img: np.ndarray, step: int, group=None):
        tag_name = f"{group}/{tag}" if group else tag

        if img.ndim == 2:
            img = np.expand_dims(img, axis=0)
        elif img.ndim == 3 and img.shape[0] in [1, 3]:
            pass
        elif img.ndim == 3 and img.shape[2] in [1, 3]:
            img = np.transpose(img, (2, 0, 1))
        else:
            raise ValueError(f"Unsupported image shape: {img.shape}")
        
        tensor_img = torch.from_numpy(img).float()
        if tensor_img.max() > 1.0:
            tensor_img /= 255.0  # Scale to [0, 1]
        
        self.writer.add_image(tag_name, tensor_img, step)

    def close(self):
        self.writer.close()


# === Singleton Wrapper ===
_logger_instance = None
_cur_time = datetime.now().strftime("%Y%m%d_%H%M%S")
_log_dir = f"runs/experiment_{_cur_time}"

def get_writer(log_dir=_log_dir) -> Logger:
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = Logger(log_dir)
    return _logger_instance
