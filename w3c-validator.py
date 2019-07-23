#!/usr/bin/env python
'''
w3c-validator - Validate HTML and CSS files using the WC3 validators

Copyright: Stuart Rackham (c) 2011
License:   MIT
Email:     srackham@gmail.com
'''

'''
Fork from https://github.com/srackham/w3c-validator
Modified by pulse-mind
Email: pulse.mind.com@gmail.com

Example : python w3c-validator.py --cssonly --file_url_or_directory=/mnt/d/projects/example/resources/css
'''

import os
import sys
import time
import json
import commands
import urllib
import getopt

html_validator_url = 'http://validator.w3.org/check'
css_validator_url = 'http://jigsaw.w3.org/css-validator/validator'

verbose_option = False

def message(msg):
    print >> sys.stderr, msg

def verbose(msg):
    if verbose_option:
        message(msg)

def validate(filename):
    '''
    Validate file and return JSON result as dictionary.
    'filename' can be a file name or an HTTP URL.
    Return '' if the validator does not return valid JSON.
    Raise OSError if curl command returns an error status.
    '''
    quoted_filename = urllib.quote(filename)
    if filename.startswith('http://'):
        # Submit URI with GET.
        if filename.endswith('.css'):
            cmd = ('curl -sG -d uri=%s -d output=json -d warning=0 %s'
                    % (quoted_filename, css_validator_url))
        else:
            cmd = ('curl -sG -d uri=%s -d output=json %s'
                    % (quoted_filename, html_validator_url))
    else:
        # Upload file as multipart/form-data with POST.
        if filename.endswith('.css'):
            cmd = ('curl -sF "file=@%s;type=text/css" -F output=json -F warning=0 %s'
                    % (quoted_filename, css_validator_url))
        else:
            cmd = ('curl -sF "uploaded_file=@%s;type=text/html" -F output=json %s'
                    % (quoted_filename, html_validator_url))
    verbose(cmd)
    status,output = commands.getstatusoutput(cmd)
    if status != 0:
        raise OSError (status, 'failed: %s' % cmd)
    verbose(output)
    try:
        result = json.loads(output)
    except ValueError:
        result = ''
    time.sleep(2)   # Be nice and don't hog the free validator service.
    return result


def usage(argv):
    message('usage: %s [--verbose] [--cssonly] --file_url_or_directory=FILE|URL|PATH' % os.path.basename(argv))
    exit(1)

if __name__ == '__main__':

    verbose_option = False
    css_only_option = False
    file_or_directory = None
    try:                                
        opts, args = getopt.getopt(sys.argv[1:], "hcvf:", ["help", "cssonly", "verbose", "file_url_or_directory="])
    except getopt.GetoptError:          
        usage(sys.argv[0])                         
        sys.exit(2)               
    for opt, arg in opts:    
        if opt in ("-h", "--help"): 
            usage(sys.argv[0])                     
            sys.exit()   
        elif opt in ("-v", "--verbose"):
            verbose_option = True                        
        elif opt in ("-c", "--cssonly"):
            css_only_option = True   
        elif opt in ("-f", "--file_url_or_directory"):
            file_or_directory = arg     

    if file_or_directory is None : 
        usage(sys.argv[0])                         
        sys.exit(2)        

    files = []     
    if os.path.isdir(file_or_directory):
        # r=root, d=directories, f = files
        for r, d, f in os.walk(file_or_directory):
            for file in f:
                if css_only_option and file.endswith('.css') or not css_only_option:     
                        if file.endswith('.css') or file.endswith('.html') or file.endswith('.htm'):
                            files.append(os.path.join(r, file))                   
        print("Found these files in %s: " % (file_or_directory))
        for f in files:
            print(f)
    else:
        files.append(file_or_directory)    

    errors = 0
    warnings = 0
    
    for f in files:           
        message('validating: %s ...' % f)
        retrys = 0
        while retrys < 2:
            result = validate(f)
            if result:
                break
            retrys += 1
            message('| retrying: %s ...' % f)
        else:
            message('| failed: %s' % f)
            errors += 1
            continue
        if f.endswith('.css'):
            errorcount = result['cssvalidation']['result']['errorcount']
            warningcount = result['cssvalidation']['result']['warningcount']
            # print(str(result))
            errors += errorcount
            warnings += warningcount
            if errorcount > 0:
                message('| errors: %d' % errorcount)
                for error in result['cssvalidation']['errors']:
                    print("|-- Ligne %s : %s" % (error['line'], error['message']))
                    print("|       %s" % (error['context']))
            if warningcount > 0:
                message('| warnings: %d' % warningcount)
        else:
            for msg in result['messages']:
                if 'lastLine' in msg:
                    message('%(type)s: line %(lastLine)d: %(message)s' % msg)
                else:
                    message('%(type)s: %(message)s' % msg)
                if msg['type'] == 'error':
                    errors += 1
                else:
                    warnings += 1