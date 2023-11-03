from tensorflow.keras import layers
from tensorflow.keras import Model

def getRobustAE_decreaseFilters(input_shape):
    latent_dim = 9216

    entrada = layers.Input(shape=input_shape)

    # Encoder
    encoder = layers.Conv2D(192, (3,3), padding='same', activation='relu')(entrada)
    encoder = layers.MaxPooling2D(pool_size=(2,2), padding='same')(encoder)

    encoder = layers.Conv2D(96, (3,3), padding='same', activation='relu')(encoder)
    encoder = layers.MaxPooling2D(pool_size=(2,2), padding='same')(encoder)

    encoder = layers.Conv2D(48, (3,3), padding='same', activation='relu')(encoder)
    encoder = layers.MaxPooling2D(pool_size=(2,2), padding='same')(encoder)

    encoder = layers.Conv2D(24, (3,3), padding='same', activation='relu')(encoder)
    encoder = layers.MaxPooling2D(pool_size=(2,2), padding='same')(encoder)

    codificacion = layers.Flatten()(encoder)
    codificacion = layers.Dense(latent_dim, activation='relu')(codificacion)
    codificacion = layers.Reshape((16, 24, 24))(codificacion)

    decoder = layers.Conv2DTranspose(24, (3,3), padding='same', activation='relu')(codificacion)
    decoder = layers.UpSampling2D((2,2))(decoder)

    decoder = layers.Conv2DTranspose(48, (3,3), padding='same', activation='relu')(decoder)
    decoder = layers.UpSampling2D((2,2))(decoder)

    decoder = layers.Conv2DTranspose(96, (3,3), padding='same', activation='relu')(decoder)
    decoder = layers.UpSampling2D((2,2))(decoder)

    decoder = layers.Conv2DTranspose(192, (3,3), padding='same', activation='relu')(decoder)
    decoder = layers.UpSampling2D((2,2))(decoder)

    salida = layers.Conv2DTranspose(input_shape[len(input_shape) - 1], (3,3), padding='same', activation='sigmoid')(decoder)

    return Model(inputs = entrada, outputs = salida)