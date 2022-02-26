import torch
import torchvision
import torchvision.transforms as transforms
import cv2
from PIL import Image
import numpy as np

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


model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()
model.to("cuda")

cap = cv2.VideoCapture(1)
transform = transforms.ToTensor()

prev_img = None

while 1:
    grabbed, frame = cap.read()
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #img = np.repeat(frame[:,:,np.newaxis],3,axis=2)
    img = [transform(frame).to("cuda")]
    predictions = model(img)

    boxes = predictions[0]['boxes'].cpu().detach().numpy()
    labels = predictions[0]['labels'].cpu().detach().numpy()
    scores = predictions[0]['scores'].cpu().detach().numpy()
    indices = torchvision.ops.batched_nms(predictions[0]['boxes'], predictions[0]['scores'], predictions[0]['labels'], 0.1)

    # if prev_img is not None:
    #     diff = cv2.absdiff(frame,prev_img)
    #     cv2.imshow("diff", diff)
    #     cv2.imshow("prev", prev_img)
    #     print(np.sum(diff))
    # prev_img = frame.copy()

    for i in indices:
        box = boxes[i]
        label = labels[i]
        score = scores[i]
        if COCO_INSTANCE_CATEGORY_NAMES[label] == "person":
            x1,y1,x2,y2 = [int(v) for v in box]
            image = cv2.rectangle(frame, (x1,y1), (x2,y2), 1, 2)
            image = cv2.putText(image, COCO_INSTANCE_CATEGORY_NAMES[label],(x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

    cv2.imshow("frame", image)
    cv2.waitKey(1)