import json
import requests
import unittest
import pdb
import os, shutil
from os.path import dirname, realpath
import sys
sys.path.append(dirname(dirname(realpath(__file__))))
import argparse

# import oncoserve.aggregators.basic as aggregators

# For density prediction
# For risk prediction
DOMAIN = "http://localhost:"

# python -m unittest tests.test_intecnus_app.Test_Intecnus_App.test_normal_request

class Test_Intecnus_App(unittest.TestCase):

    #TEST_DIR = os.path.join(dirname(realpath(__file__)), "..", "test_data")
    TEST_DIR = "/home/flavioc/Codes/Mammo/OncoServe_Public/test_data" 
    IMAGES_DIR = "/home/flavioc/Codes/Mammo/OncoServe_Public/test_images"
    domain = None

    def setUp(self):

        self.filenames = [os.path.join(self.TEST_DIR, f) for f in os.listdir(self.TEST_DIR)]
        self.files = [open(f, 'rb') for f in self.filenames]
        self.imagenames = [os.path.join(self.IMAGES_DIR, f) for f in os.listdir(self.IMAGES_DIR)]
        self.imagefiles = [open(f, 'rb') for f in self.imagenames]
        # self.f1 = open("/home/yala/sample_dicoms/1.dcm", 'rb')
        # self.f2 = open("/home/yala/sample_dicoms/2.dcm", 'rb')
        # self.f3 = open("/home/yala/sample_dicoms/3.dcm", 'rb')
        # self.f4 = open("/home/yala/sample_dicoms/4.dcm", 'rb')
        # Fake MRN
        self.MRN = '11111111'
        # Fake Accession
        self.ACCESSION = '2222222'
        self.METADATA = {'mrn':self.MRN, 'accession': self.ACCESSION}
        self.domain = Test_Intecnus_App.domain


    def tearDown(self):
        try:
            for f in self.files:
                f.close()
            for f in self.imagefiles:
                f.close()
            
            # self.f1.close()
            # self.f2.close()
            # self.f3.close()
            # self.f4.close()
        except Exception as e:
            pass

    def test_domain(self):
        print(f"Instance domain: {self.domain}")
        print(f"Class domain: {domain}")

    def test_normal_request(self):
        '''
        Demo of how to use MIRAI. Note, this is applicable for all MIRAI applications.
        '''

        '''
         1. Load dicoms. Make sure to filter by view, MIRAI will not take responsibility for this.
        '''
        files = [('dicom',f) for f in self.files]
        print(self.filenames)
        # print(files)
        # files = [('dicom',self.f1), ('dicom',self.f2), ('dicom',self.f3), ('dicom', self.f4)]

        '''
        2. Send request to model at /serve with dicoms in files field, and any metadata in the data field.
        Note, files should contain a list of tuples:
         [ ('dicom': bytes), '(dicom': bytes)', ('dicom': bytes) ].
        Deviating from this may result in unexpected behavior.
        '''
        r = requests.post(os.path.join(self.domain,"serve"), files=files,
                          data=self.METADATA)
        '''
        3. Results will contain prediction, status, version info, all original metadata
        '''
        print(r.__dict__)
        print(f"Status: {r.json()['msg']}")
        print(f"Density prediction: {r.json()['prediction']}")
        self.assertEqual(r.status_code, 200)
        content = json.loads(r.content)
        self.assertEqual(content['metadata']['mrn'], self.MRN)
        self.assertEqual(content['metadata']['accession'], self.ACCESSION)


    def test_normal_request_images(self):
        '''
        Demo of how to use MIRAI. Note, this is applicable for all MIRAI applications.
        '''

        '''
         1. Load dicoms. Make sure to filter by view, MIRAI will not take responsibility for this.
        '''

        files = [('png',f) for f in self.imagefiles]
        print(self.imagenames)
        print(files)

        '''
        2. Send request to model at /serve with dicoms in files field, and any metadata in the data field.
        Note, files should contain a list of tuples:
         [ ('dicom': bytes), '(dicom': bytes)', ('dicom': bytes) ].
        Deviating from this may result in unexpected behavior.
        '''
        r = requests.post(os.path.join(self.domain,"serve_from_images"), files=files,
                          data=self.METADATA)
        '''
        3. Results will contain prediction, status, version info, all original metadata
        '''
        print(r.__dict__)
        print(f"Status: {r.json()['msg']}")
        if '5000' in self.domain:
            print(f"Density prediction: {r.json()['prediction']}")
        else:
            print(f"Risk prediction: {r.json()['prediction']}")
        self.assertEqual(r.status_code, 200)
        content = json.loads(r.content)
        self.assertEqual(content['metadata']['mrn'], self.MRN)
        self.assertEqual(content['metadata']['accession'], self.ACCESSION)



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Test Intecnus App')
    parser.add_argument('--domain', type=str, default="http://localhost:5000", help="Domain to test")
    parser.add_argument('--density', action="store_true", required=False, help="Test density")
    parser.add_argument('--risk', action="store_true", required=False, help="Test risk")

    
    args, remaining_argv = parser.parse_known_args()

    if args.density:
        domain =  DOMAIN +  "5000"
    elif args.risk:
        domain =  DOMAIN + "5001"
    else:
        domain =  args.domain

    print(f"Domain: {domain}")

    # os.environ["DOMAIN"] = domain

    Test_Intecnus_App.domain = domain

    args, remaining_argv = parser.parse_known_args()    

    # Remove argparse arguments and run unittest
    import sys
    sys.argv = [sys.argv[0]] + remaining_argv

    unittest.main()
