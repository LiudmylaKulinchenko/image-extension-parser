# Image sizes parser
Script for the parser of image extensions in Python:

1) Take all the url of the images in the file (there are more than 40k images); 
2) Take the size of the image expansion;
3) Fill in the “SIZE” column in the file where the image extension should be
4) The result of the script in the Jupyter Notebook

## Installing

Python3 must be already installed

```shell
git clone https://github.com/LiudmylaKulinchenko/newspaper-agency.git  # clone project to your PK
cd image-sizer-parser/  # change directory to the project directory
python -m venv venv
venv/Scripts/activate  # create and activate virtual environment
pip install -r requirements.txt  # install requirements
python manage.py runserver  # starts Django Server
```

## Demo

![Result](demo_image.png)