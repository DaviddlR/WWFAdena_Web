import tensorflow as tf

if tf.test.is_gpu_available(cuda_only=True):
    print("HAY GPU")
else:
    print("NO GPU")
