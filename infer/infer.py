import os
import random
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split
from torchvision.transforms import transforms
from torchvision.datasets import ImageFolder
from PIL import Image

from flask import Flask, request, jsonify
import sys
lib_path = os.environ.get('LIBPATH')
if lib_path is None:
    lib_path = '../lib/'


import sys
sys.path.append(lib_path)
from digit_recognizer import DigitRecognizer



# WHAT TO DO
# 1. 추론과 관련없는 것은 다 날렸습니다.
# 2. 추론을 위한 코드를 추가했습니다.
# 3. 모델을 읽어오기 위한 코드를 추가했습니다. (모델 패쓰 포함)
# 4. Flask를 통한 POST 서비스를 위한 코드를 추가했습니다.

app = Flask(__name__)                   #4
app.debug = True                        #4

model = DigitRecognizer()

model_path = os.environ.get('MODELPATH')    #3
if model_path is None:                      #3
    print("cannot fild env modelpath")
    model_path = '../model/'                #3
else:
    print("model_path_from_env", model_path)

model.load_state_dict(torch.load(model_path + 'modelfile')) #3
model.eval()



# Set seed for reproducibility
random.seed(42)
torch.manual_seed(42)

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")



@app.route('/recognize', methods=['POST'])          #4
def recog_image():                                  #4
    if 'image' not in request.files:                #4
        return "No image file uploaded", 400        #4
    image_file = request.files['image']             #4
    try:                                            #4
        transform = transforms.Compose([transforms.Grayscale(), transforms.ToTensor()])

        image = Image.open(image_file).convert('L')     #2
        image = transform(image).unsqueeze(0)           #2

        # 추론
        with torch.no_grad():                           #2
            output = model(image)                       #2

        # 결과 출력
        _, predicted = torch.max(output, 1)             #2
        return jsonify({'result':predicted.item()})     #2
    except Exception as e:                              #4
        return f"Error recognizing image: {str(e)}", 500    #4

if __name__ == '__main__':      #4
    app.run(host='0.0.0.0', port=80)                   #4

""" 

# Define transforms
transform = transforms.Compose([transforms.Grayscale(), transforms.ToTensor()])

model = DigitRecognizer()

model_path = os.environ.get('MODELPATH')
if model_path is None:
    model_path = '../model/'

model.load_state_dict(torch.load(model_path + 'modelfile'))

# Initialize the model
#model = DigitRecognizer().to(device)


# Evaluation
model.eval()

image_path = "../data/0/img_10701.jpg"

image = Image.open(image_path).convert('L')
image = transform(image).unsqueeze(0)

# 추론
with torch.no_grad():
    output = model(image)

# 결과 출력
_, predicted = torch.max(output, 1)
print('Predicted:', predicted.item())

 """