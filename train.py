import tensorflow as tf
from tensorflow.keras import layers, models

img_size = 224
batch_size = 32

dataset_path = "currency_dataset"

print("🚀 Loading dataset...")

train_ds = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    image_size=(img_size, img_size),
    batch_size=batch_size
)

print("Classes:", train_ds.class_names)

normalization = layers.Rescaling(1./255)
train_ds = train_ds.map(lambda x, y: (normalization(x), y))

print("🧠 Building model...")

model = models.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', input_shape=(224,224,3)),
    layers.MaxPooling2D(),

    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(),

    layers.Conv2D(128, (3,3), activation='relu'),
    layers.MaxPooling2D(),

    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(3, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print("🔥 Training started...")

model.fit(train_ds, epochs=10)

model.save("currency_model.h5")

print("✅ Model saved successfully!")
print("🚀 SCRIPT STARTED")
import os
print("DATASET EXISTS:", os.path.exists("currency_dataset"))