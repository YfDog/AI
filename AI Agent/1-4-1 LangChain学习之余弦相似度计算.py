'''
四个向量：
A[0.5,0.5]
B[0.7,0.7]
C[0.7,0.5]
D[-0.6,-0.5]

计算AB的余弦相似度
计算AC的余弦相似度
计算AD的余弦相似度
'''
import numpy as np

def get_dot(vec_a,vec_b):
    '''计算两向量的点积，点积：两向量同维度数字乘积之和'''
    if len(vec_a) != len(vec_b):
        raise ValueError("向量的维度必须相同！")
    sum = 0
    for va,vb in zip(vec_a,vec_b):
        mul = va*vb
        sum += mul
    return sum

def get_norm(vec):
    '''计算单个向量的模长'''
    sum=0
    for v in vec:
        mul = v*v
        sum+=mul
    return np.sqrt(sum)

def cos_angle(vec_a,vec_b):
    '''计算余弦相似度，也就是计算两向量的cos夹角'''
    dot = get_dot(vec_a, vec_b)
    norm_a = get_norm(vec_a)
    norm_b = get_norm(vec_b)
    result  =  dot/ (norm_a* norm_b)
    return result

if __name__=='__main__':
    vec_A=[0.5, 0.5]
    vec_B=[0.7, 0.7]
    vec_C=[0.7, 0.5]
    vec_D=[-0.6, -0.5]

    print("a和b向量的余弦相似度是：",cos_angle(vec_A,vec_B)) #余弦相似度为1，表示两个向量方向一致
    print("a和c向量的余弦相似度是：",cos_angle(vec_A, vec_C)) #余弦相似度的值越靠近1，表示两个向量的方向越相近
    print("a和d向量的余弦相似度是：",cos_angle(vec_A, vec_D))
