# Skip Connections Matter
 
This repository contains the code for [Skip Connections Matter: On the Transferability of Adversarial Examples Generated with ResNets](https://openreview.net/forum?id=BJlRs34Fvr) (ICLR 2020 Spotlight).


## Method

We propose the Skip Gradient Method (SGM) to generate adversarial examples using gradients more from the skip connections rather than the
residual modules. In particular, SGM utilizes a decay factor (gamma) to reduce gradients from the residual modules, 

<img src="https://github.com/csdongxian/security-of-skip-connections/blob/master/figs/formula_of_sgm.jpg" width="80%" height="80%">


## Requisite

This code is implemented in Pytorch, and we have tested the code under the following environment settings:

- python = 3.6.7
- torch = 1.1.0
- torchvision = 0.3.0
- advertorch = 0.1.4
- pretrainedmodels = 0.7.4

## Run the code

Assuming the source model is DenseNet-201, the target model is VGG-19. 

1. Data preparing: 
    - Select images which are **correctly classified** by the source model (DenseNet-201).  
    - Preprocess selected images (for DenseNet-201, crop and resize images to 224x224), and save them to nat_images.
2. Run the code and save adversarial examples to adv_images:
```
python attack_iter.py --input-dir=nat_images --output-dir=adv_images --arch=densenet201 --gamma=0.5 --epsilon=16 --num-steps=10 --step-size=2
```
3. Evaluate attack success rate.

## Results

<img src="https://github.com/csdongxian/security-of-skip-connections/blob/master/figs/examples.jpg" width="100%" height="100%">

## Implementation

For easier reproduction, we provide more detailed information here.

#### register backward hook for SGM

In fact, we manipulate gradients flowing through ReLU in [utils_sgm](https://github.com/csdongxian/security-of-skip-connections/blob/master/utils_sgm.py), since there is no ReLU in skip-connections: 

- For ResNet, there are "downsampling" modules in which skip-connections are replaced by a conv layer. We do not manipulate gradients of "downsampling" module;

- For DenseNet, we manipulate gradients in all dense block.


#### Pretrained models

All pretrained models in our paper can be found online:

- For VGG/ResNet/DenseNet/SENet, we use pretrained models in [pretrainedmodels](https://github.com/Cadene/pretrained-models.pytorch);

- For Inception models, we use pretrained models in [slim](https://github.com/tensorflow/models/tree/master/research/slim) of Tensorflow;

- For secured models (e.g. ), they are trained by [Ensemble Adversarial Training](https://arxiv.org/abs/1705.07204) [2], and pretrained results can be found in [adv_imagenet_models](https://github.com/tensorflow/models/tree/master/research/adv_imagenet_models).


## Reference

[1] Yinpeng Dong, Fangzhou Liao, Tianyu Pang, Hang Su, Jun Zhu, Xiaolin Hu, and Jianguo Li. Boosting
adversarial attacks with momentum. In CVPR, 2018.

[2] Florian Tramèr, Alexey Kurakin, Nicolas Papernot, Ian Goodfellow, Dan Boneh, Patrick McDaniel. Ensemble Adversarial Training: Attacks and Defenses. In ICLR, 2018.
