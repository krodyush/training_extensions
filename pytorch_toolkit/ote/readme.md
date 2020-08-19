## pytorch_toolkit/object_detection tree
```bash
├── face-detection
│   ├── face-detection-0200
│   │   ├── config.py
│   │   └── template.yml
│   ├── face-detection-0202
│   │   ├── config.py
│   │   └── template.yml
│   ├── problem.yml
│   ├── readme.md
│   ├── schema.json
│   └── tools
│       ├── eval.py
│       └── train.py
├── horizontal-text-detection
│   ├── horizontal-text-detection-0001
│   │   ├── config.py
│   │   └── template.yml
│   ├── problem.yml
│   ├── readme.md
│   ├── schema.json
│   └── tools
│       ├── eval.py
│       └── train.py
├── person-detection
│   ├── person-detection-0200
│   │   ├── config.py
│   │   └── template.yml
│   ├── person-detection-0201
│   │   ├── config.py
│   │   └── template.yml
│   ├── person-detection-0202
│   │   ├── config.py
│   │   └── template.yml
│   ├── problem.yml
│   ├── readme.md
│   ├── schema.json
│   └── tools
│       ├── eval.py
│       └── train.py
├── oteod
├── requirements.txt
├── setup.py
```

## template.yml
```bash
name: person-vehicle-bike-detection-2001
description: Person Vehicle Bike Detection based on MobileNetV2 (SSD).
dependencies:
- sha256: 9c4190208d9ff7b7b860821c48264a50ee529e84f23d0d2f6947eceb64c2346a
  size: 14937205
  source: https://download.01.org/opencv/openvino_training_extensions/models/object_detection/v2/vehicle-person-bike-detection-2001-1.pth
  destination: snapshot.pth
- source: ../tools/train.py
  destination: train.py
- source: ../tools/eval.py
  destination: eval.py
- source: ../../tools/export.py
  destination: export.py
- source: ../../tools/quantize.py
  destination: quantize.py
training_parameters:
  gpu_num: 4
  batch_size: 54
  base_learning_rate: 0.05
  epochs: 20
metrics:
- display_name: Size
  key: size
  unit: Mp
  value: 1.84
- display_name: Complexity
  key: complexity
  unit: GFLOPs
  value: 1.86
- display_name: mAP @ [IoU=0.50:0.95]
  key: map
  unit: '%'
  value: 22.6
config: config.py
```