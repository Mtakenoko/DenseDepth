import os
import glob
import argparse
import matplotlib

# Keras / TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '5'
from keras.models import load_model
from layers import BilinearUpSampling2D
from utils import predict, load_images, display_images
from matplotlib import pyplot as plt

# Argument Parser
parser = argparse.ArgumentParser(description='High Quality Monocular Depth Estimation via Transfer Learning')
parser.add_argument('--model', default='nyu.h5', type=str, help='Trained Keras model file.')
parser.add_argument('--input', default='examples/default/*.png', type=str, help='Input filename or folder.')
parser.add_argument('--input_depth', default='', type=str, help='Input Deoth filename or folder.')
parser.add_argument('--bs', type=int, default=4, help='Batch size')
parser.add_argument('--mindepth', type=float, default=10.0, help='Minimum of input depths')
parser.add_argument('--maxdepth', type=float, default=1000.0, help='Maximum of input depths')
args = parser.parse_args()

# Custom object needed for inference and training
custom_objects = {'BilinearUpSampling2D': BilinearUpSampling2D, 'depth_loss_function': None}

print('Loading model...')

# Load model into GPU / CPU
model = load_model(args.model, custom_objects=custom_objects, compile=False)

print('\nModel loaded ({0}).'.format(args.model))

# Input images
inputs = load_images( glob.glob(args.input) )
# inputs_depth = load_images( glob.glob(args.input_depth) )
print('\nLoaded ({0}) images of size {1}.'.format(inputs.shape[0], inputs.shape[1:]))

# Compute results
outputs = predict(model, inputs, minDepth=args.mindepth, maxDepth=args.maxdepth, batch_size=args.bs)

#matplotlib problem on ubuntu terminal fix
#matplotlib.use('TkAgg')   

# Display results
viz = display_images(outputs.copy(), inputs.copy())
plt.figure(figsize=(10,5))
plt.imshow(viz)
plt.savefig('test.png')
plt.show()
