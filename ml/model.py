import tensorflow as tf
import numpy as np
from PIL import Image
from django.conf import settings

IMG_SIZE = (128, 128)

MODEL_PATH = settings.BASE_DIR / "ml" / "blood_cell_model.h5"

model = tf.keras.models.load_model(MODEL_PATH)

CLASS_NAMES = [
    "Eritrositlar",
    "Sog'lom qon donachalari",
    "Leykositlar",
    "Noodatiy hujayralar",
    "Trombositlar"
]


def preprocess_image(image_field):
    image_field.open("rb")

    with Image.open(image_field) as img:
        img = img.convert("RGB")
        img = img.resize(IMG_SIZE)
        arr = np.array(img, dtype=np.float32) / 255.0

    return arr


def predict_from_multiple_images(media_objects):
    """
    media_objects: iterable[Media]
    """
    batch = []

    for media in media_objects:
        if not media.file:
            continue

        batch.append(preprocess_image(media.file))

    if not batch:
        raise ValueError("No valid images provided")

    batch = np.stack(batch, axis=0)

    preds = model.predict(batch)

    mean_probs = np.mean(preds, axis=0)

    class_index = int(np.argmax(mean_probs))
    confidence = float(np.max(mean_probs))

    return {
        "class_index": class_index,
        "class_name": CLASS_NAMES[class_index],
        "confidence": round(confidence, 3),
        "raw_probs": mean_probs.tolist(),
    }