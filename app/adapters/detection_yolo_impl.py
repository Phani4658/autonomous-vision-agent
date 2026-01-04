from ultralytics import YOLO
import time
from PIL import Image
from app.services.annotate import save_annotated_image


class YOLODetectionService:
    def __init__(self, model_name: str="yolov8n.pt"):
        self.model = YOLO(model_name)

    async def detect(self, image_path: str, asset_id: str):
        t0 = time.time()

        img = Image.open(image_path)
        results = self.model.predict(source=img, verbose=False)

        detections = []
        r = results[0]
        names = r.names

        if r.boxes is not None:
            for b in r.boxes:
                cls_id = int(b.cls[0].item())
                score = float(b.conf[0].item())
                x1,y1,x2,y2 = b.xyxy[0].tolist()
                detections.append({
                    "label": names.get(cls_id, str(cls_id)),
                    "score": score,
                    "bbox": [int(x1), int(y1), int(x2), int(y2)]
                })

        latency_ms = int((time.time() - t0) * 1000)

        # ✅ Save annotated image
        annotated_path = save_annotated_image(asset_id, img, r)

        return {
            "asset_id": asset_id,
            "detections": detections,
            "model": "yolov8",
            "latency_ms": latency_ms,
            "artifacts": {
                "annotated_image_path": annotated_path
            }
        }
    
    async def debug_detect(self, image_path: str, asset_id: str):
        t0 = time.time()

        img = Image.open(image_path)
        results = self.model.predict(source=img, verbose=False)

        r = results[0]

        # ✅ JSON-safe debug payload
        debug = {
            "asset_id": asset_id,
            "type": str(type(r)),
            "orig_shape": list(getattr(r, "orig_shape", [])) if getattr(r, "orig_shape", None) else None,
            "names_sample": dict(list(r.names.items())[:5]) if getattr(r, "names", None) else None,

            "has_boxes": r.boxes is not None,
            "boxes_type": str(type(r.boxes)) if r.boxes is not None else None,
            "num_boxes": int(len(r.boxes)) if r.boxes is not None else 0,

            # Core tensors converted safely
            "boxes_xyxy": r.boxes.xyxy.cpu().numpy().tolist() if r.boxes is not None else [],
            "boxes_conf": r.boxes.conf.cpu().numpy().tolist() if r.boxes is not None else [],
            "boxes_cls": r.boxes.cls.cpu().numpy().tolist() if r.boxes is not None else [],
        }

        # ✅ Save annotated image
        annotated_path = save_annotated_image(asset_id, img, r)

        debug["latency_ms"] = int((time.time() - t0) * 1000)
        debug["model"] = "yolov8"
        return debug
