from http import client
import torch
import torchvision
import torchvision.transforms as transforms
import cv2
from PIL import Image
import numpy as np
import os
import sys
sys.path.append("../communication")
from json_client import JSONClient
import asyncio

def cal_dist_ratio(x1,x2,y1,y2,width,height):
    max_dist = np.sqrt((width/2)**2 + (height/2)**2)
    max_area = width*height
    obj_cen = np.array([(x2-x1)/2+x1, (y2-y1)/2+y1])
    obj_area = (x2-x1)*(y2-y1)
    frame_cen = np.array([width/2, height/2])
    dist = np.linalg.norm(frame_cen-obj_cen)
    area_ratio = 1-obj_area/max_area
    dist_ratio = 1-dist/max_dist
    ratio = (area_ratio+dist_ratio)/2
    return ratio


COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

mv_client = JSONClient()

model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()
model.to("cuda")

cap = cv2.VideoCapture(0)
transform = transforms.ToTensor()

prev_img = None


while 1:
    grabbed, frame = cap.read()
    H,W,C = frame.shape
    img = [transform(frame).to("cuda")]
    predictions = model(img)

    boxes = predictions[0]['boxes'].cpu().detach().numpy()
    labels = predictions[0]['labels'].cpu().detach().numpy()
    scores = predictions[0]['scores'].cpu().detach().numpy()
    indices = torchvision.ops.batched_nms(predictions[0]['boxes'], predictions[0]['scores'], predictions[0]['labels'], 0.2)

    payload = {"distance_ratio": [], "labels": [], "scores": []}
    for i in indices:
        box = boxes[i]
        label = labels[i]
        score = scores[i]
        
        if score>=0.5:
            x1,y1,x2,y2 = [int(v) for v in box]
            dist_ratio = cal_dist_ratio(x1,x2,y1,y2,W,H)
            print(f'label: {COCO_INSTANCE_CATEGORY_NAMES[label]}, dist ratio: {dist_ratio}')
            payload["labels"].append(COCO_INSTANCE_CATEGORY_NAMES[label])
            payload["distance_ratio"].append(dist_ratio)
            payload["scores"].append(float(score))

        if score>=0.5:
            x1,y1,x2,y2 = [int(v) for v in box]
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
            texts = COCO_INSTANCE_CATEGORY_NAMES[label]
            cv2.putText(frame, texts, (x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    mv_client.send(payload, verbose=1)        

    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

    cv2.imshow("frame", frame)
    cv2.waitKey(1)