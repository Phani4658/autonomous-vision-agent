from pathlib import Path
from PIL import Image
from app.core.config import settings

def save_annotated_image(asset_id: str, pil_img: Image.Image, results0) -> str:
    """
    results0 is Ultralytics Results object for one image (results[0])
    Returns local file path for the annotated image.
    """
    out_dir = Path(settings.output_dir) / asset_id
    out_dir.mkdir(parents=True, exist_ok=True)

    # Ultralytics provides a rendered image via plot()
    # plot() returns a numpy array (BGR or RGB depending on version); we convert safely.
    plotted = results0.plot()  # numpy array
    annotated = Image.fromarray(plotted)

    out_path = out_dir / "annotated.jpg"
    annotated.save(out_path, quality=92)
    return str(out_path)