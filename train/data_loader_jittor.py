import jittor as jt
import jittor.nn as nn
from jittor.dataset import ImageFolder
import jittor.transform as transform
from jittor.dataset.cifar import CIFAR100
from torchvision import transforms
from jittor import transform

def get_cifar100_dataloaders(config):
    batch_size = config['batch_size']
    img_size = config['image_size']
    
    train_transform = transform.Compose([
        transforms.RandAugment(),
        transforms.RandomCrop(32,padding=4),
        transform.Resize(img_size),
        transform.RandomHorizontalFlip(),
        transform.ToTensor(),
        transform.ImageNormalize(
            mean=[0.5071, 0.4867, 0.4408], 
            std=[0.2675, 0.2565, 0.2761]
        ),
    ])

    val_transform = transform.Compose([
        transform.Resize(img_size),
        transform.ToTensor(),
        transform.ImageNormalize(
            mean=[0.5071, 0.4867, 0.4408], 
            std=[0.2675, 0.2565, 0.2761]
        )
    ])
    
    num_workers = config['num_workers']
    
    train_dataset = CIFAR100(
        root=config['data_path'],
        train=True,
        transform=train_transform,
        download= True
    )
    
    val_dataset = CIFAR100(
        root=config['data_path'],
        train=False,
        transform=val_transform,
        download=True
    )

    train_loader = train_dataset.set_attrs(
        batch_size=batch_size, shuffle=True, num_workers=num_workers,buffer_size=1024**3)
    val_loader = val_dataset.set_attrs(
        batch_size=batch_size, shuffle=False, num_workers=num_workers,buffer_size=1024**3)

    return train_loader, val_loader 