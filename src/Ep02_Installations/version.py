#!/home/username/parrot/bin/python


import olympe  # Replace 'requests' with the name of the library you want to check
import torch

try:
    olympe_version = olympe.__version__
    print(f"The version of installed Olympe is: {olympe_version}")
except AttributeError:
    print("Olympe does not have a version attribute.")

try:
    torch_version = torch.__version__
    print(f"The version of installed Torch is: {torch_version}")
except AttributeError:
    print("Torch does not have a version attribute.")