## dVAE的训练 oss和 VQ-VAE 类似，只是使用了KL距离来让分布尽量分散：

$$
- E_{z \sim q ( z \mid x )} [ \operatorname{l o g} ( p ( x \mid z ) ) ]+K L ( q ( z \mid x ) \Vert p ( z ) ) 
$$
