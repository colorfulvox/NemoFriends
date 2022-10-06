# QuickDraw

## Version
1. tensorflow                2.1.0
2. tensorflow-gpu            2.1.0
3. keras                     2.10.0
4. h5py                      2.10.0
5. cudnn                     7.6.5
6. keras2onnx              1.7.0
7. python                    3.7.13

## Data - 46 AnimalFoods
```
['duck', 'snail', 'banana', 'broccoli', 'carrot', 'bird', 'fish', 'watermelon', 'cloud', 'apple', 'blackberry', 'pig', 'cow', 'bush', 'leaf', 'flamingo', 'zebra', 'octopus', 'ant', 'grass', 'donut', 'kangaroo', 'blueberry', 'parrot', 'raccoon', 'camel', 'frog', 'spider', 'pear', 'crab', 'garden', 'sandwich', 'asparagus', 'flower', 'mouse', 'swan', 'steak', 'potato', 'crocodile', 'owl', 'horse', 'strawberry', 'grapes', 'pineapple', 'cake', 'bread']
```
EachImageData : 10000 | 460,000


## Evaluate
Gpu=10 | Epochs=5 | BatchSize = 256 -> Accuarcy : 93.14% , ExecTime : 21s

## Model
QuickDraw.h5 -> QuickDraw.onnx
