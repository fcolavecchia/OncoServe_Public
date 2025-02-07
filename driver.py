import json
import requests
from dataclasses import dataclass
from enum import Enum
import os, shutil
from os.path import dirname, realpath
import sys
sys.path.append(dirname(dirname(realpath(__file__))))
# import oncoserve.aggregators.basic as aggregators

RISK_DOMAIN = "http://localhost:5001"
DENSITY_DOMAIN = "http://localhost:5000"

# python -m unittest tests.test_intecnus_app.Test_Intecnus_App.test_normal_request

class Intecnus_App():

    #TEST_DIR = os.path.join(dirname(realpath(__file__)), "..", "test_data")
    TEST_DIR = "/home/flavioc/Codes/Mammo/OncoServe_Public/test_data" 
    IMAGES_DIR = "/home/flavioc/Codes/Mammo/OncoServe_Public/test_images"


    def setUp(self):

        self.filenames = [os.path.join(self.TEST_DIR, f) for f in os.listdir(self.TEST_DIR)]
        self.files = [open(f, 'rb') for f in self.filenames]
        
        self.MRN = '11111111'
        # Fake Accession
        self.ACCESSION = '2222222'
        self.METADATA = {'mrn':self.MRN, 'accession': self.ACCESSION}


def request_from_images(domain, files, metadata):
    '''
    Demo of how to use MIRAI. Note, this is applicable for all MIRAI applications.
    '''

    # 1. Load dicoms. Make sure to filter by view, MIRAI will not take responsibility for this.

    files = [('png',f) for f in files]
    print(files)
    
    # 2. Send request to model at /serve with dicoms in files field, and any metadata in the data field.
    # Note, files should contain a list of tuples:
    #     [ ('dicom': bytes), '(dicom': bytes)', ('dicom': bytes) ].
    # Deviating from this may result in unexpected behavior.
    
    r = requests.post(os.path.join(domain,"serve_from_images"), files=files,
                        data=metadata)
    '''
    3. Results will contain prediction, status, version info, all original metadata
    '''
    # print(r.__dict__)
    content = json.loads(r.content)
    print(content)

    return content

def request(domain, files, metadata):
    '''
    Demo of how to use MIRAI. Note, this is applicable for all MIRAI applications.
    '''

    # 1. Load dicoms. Make sure to filter by view, MIRAI will not take responsibility for this.

    files = [('dicom',f) for f in files]
    print(files)
    # files = [('dicom',self.f1), ('dicom',self.f2), ('dicom',self.f3), ('dicom', self.f4)]

    
    # 2. Send request to model at /serve with dicoms in files field, and any metadata in the data field.
    # Note, files should contain a list of tuples:
    #     [ ('dicom': bytes), '(dicom': bytes)', ('dicom': bytes) ].
    # Deviating from this may result in unexpected behavior.
    
    r = requests.post(os.path.join(domain,"serve"), files=files,
                        data=metadata)
    '''
    3. Results will contain prediction, status, version info, all original metadata
    '''
    # print(r.__dict__)
    content = json.loads(r.content)
    print(content)

    return content

@dataclass
class Risk():

    prediction: float
    metadata: dict

    def from_content(content: dict):
        return Risk(content['prediction'], content['metadata'])  
    

class DensityValues(Enum):
    FATTY = 0
    SCATTERED = 1
    HETERODENSE = 2
    DENSE = 3 

    def to_spanish(self):
        if self == DensityValues.FATTY:
            return "Tejido graso"
        elif self == DensityValues.SCATTERED:
            return "Tejido fibroglandular disperso"
        elif self == DensityValues.HETERODENSE:
            return "Tejido heterogeneamente denso"
        elif self == DensityValues.DENSE:
            return "Tejido denso"

@dataclass
class Density():
    
        prediction: float
        metadata: dict
    
        def from_content(content: dict):
            return Density(content['prediction'], content['metadata'])
        


if __name__ == '__main__':
        
    app = Intecnus_App()

    app.setUp()
    #
    # Request from Dicoms
    #
    metadata = {'mrn':app.MRN, 'accession': app.ACCESSION}

    # Request Risk

    # filenames = [os.path.join(app.TEST_DIR, f) for f in os.listdir(app.TEST_DIR)]
    # files = [open(f, 'rb') for f in filenames]


    # content = request(RISK_DOMAIN, files, metadata)
    # print(content['prediction'])
    # risk = Risk.from_content(content)
    # print(risk.prediction)

    # filenames = [os.path.join(app.TEST_DIR, f) for f in os.listdir(app.TEST_DIR)]
    # files = [open(f, 'rb') for f in filenames]

    # # Request Density
    # content = request(DENSITY_DOMAIN, files, metadata)
    # print(content['prediction'])

    # density = Density.from_content(content)
    # print(density)
    # print(DensityValues(density.prediction).to_spanish())

    #
    # Request from Images
    #     

    # Request Risk

    filenames = [os.path.join(app.IMAGES_DIR, f) for f in os.listdir(app.IMAGES_DIR)]
    files = [open(f, 'rb') for f in filenames]

    content = request_from_images(RISK_DOMAIN, files, metadata)
    print(content['prediction'])
    risk = Risk.from_content(content)
    print(risk.prediction)

    # Request Density
    filenames = [os.path.join(app.IMAGES_DIR, f) for f in os.listdir(app.IMAGES_DIR)]
    files = [open(f, 'rb') for f in filenames]

    content = request_from_images(DENSITY_DOMAIN, files, metadata)
    print(content['prediction'])

    density = Density.from_content(content)
    print(density)
    print(DensityValues(density.prediction).to_spanish())


