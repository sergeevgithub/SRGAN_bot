import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import asyncio


class ResidualBlock(nn.Module):
    def __init__(self, in_c):
        super().__init__()
        self.res_block = nn.Sequential(
            nn.Conv2d(in_c, in_c, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(in_c, 0.8),
            nn.PReLU(),
            nn.Conv2d(in_c, in_c, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(in_c, 0.8),
        )

    def forward(self, x):
        return x + self.res_block(x)


class Generator(nn.Module):
    def __init__(self, in_c=3, out_c=3, num_res_blocks=16):
        super().__init__()

        # Enter layer
        self.enter_layer = nn.Sequential(nn.Conv2d(in_c, out_channels=64, kernel_size=9, stride=1, padding=4),
                                         nn.PReLU())

        # Residual layers
        res_blocks = []
        for _ in range(num_res_blocks):
            res_blocks.append(ResidualBlock(64))
        self.res_layers = nn.Sequential(*res_blocks)

        # Post residual layer
        self.postres_layer = nn.Sequential(nn.Conv2d(64, 64, kernel_size=3, stride=1, padding=1),
                                           nn.BatchNorm2d(64, 0.8))

        # Upsampling layers
        upsample = []
        for _ in range(2):
            upsample.append(nn.Sequential(
                nn.Conv2d(64, 256, kernel_size=3, stride=1, padding=1),
                # nn.BatchNorm2d(256),
                nn.PixelShuffle(upscale_factor=2),
                nn.PReLU()
            ))
        self.upsample = nn.Sequential(*upsample)

        # Output layer
        self.output = nn.Sequential(nn.Conv2d(64, out_c, kernel_size=9, stride=1, padding=4), nn.Tanh())

    def forward(self, x):
        out1 = self.enter_layer(x)  # goes to skip connection
        out2 = self.res_layers(out1)
        out3 = self.postres_layer(out2)  # goes to skip connection
        out4 = torch.add(out1, out3)  # skip connection
        out5 = self.upsample(out4)
        out = self.output(out5)
        return out


generator = Generator()
generator.load_state_dict(torch.load('data/generator.pt', map_location=torch.device('cpu')))


def generate(path):
    image = Image.open(path)
    to_tensor = transforms.ToTensor()
    to_image = transforms.ToPILImage()
    tensor = to_tensor(image).unsqueeze(0)
    output = generator(tensor)
    return to_image(output.squeeze(0))
