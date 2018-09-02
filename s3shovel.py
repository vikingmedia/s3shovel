#!/usr/bin/python
'''
Created on Jun 11, 2014

@author: zking
'''


import argparse
import subprocess
import os
import sys
import time


if __name__ == '__main__':
    
    # Parse CLI parameters
    p = argparse.ArgumentParser(description='Looks for files in a location, loads them up to S3 and deletes locally. Uses s3cmd.')
    
    p.add_argument('source_paths', metavar='PATH', nargs='+', help='look for files in those paths')
    p.add_argument('--bucket', '-b', help='destination bucket')
    p.add_argument('--config', '-c', metavar='FILE', help='destination bucket')
    p.add_argument('--prefix', '-p', default='', help='prefix for uploaded files (e.g. "directory")')
    p.add_argument('--verbose', '-v', action='store_true', help='prefix for uploaded files (e.g. "directory")')
    p.add_argument('--dryrun', action='store_true', help='just pretend')
    p.add_argument('--recursive', '-R',  action='store_true', help='recurse into sub directories')
    
    kwargs = vars(p.parse_args())
    
    # walk trough source_paths
    for source_path in kwargs['source_paths']:
        full_source_path = os.path.abspath(source_path)
         
        for root, dirs, files in os.walk(source_path):
            
            for file_name in sorted(files):
                
                path = os.path.join(root, file_name)
                
                if file_name.startswith('.'): 
                    if kwargs['verbose']: print 'Omitting hidden file "%s"' % (path, )
                    continue
                
                statbuf = os.stat(path)
                if time.time() - statbuf.st_mtime < 60:   # file has to be unchanged for a minute
                    if kwargs['verbose']: print 'Omitting recently changed file "%s"' % (path, )
                    continue
                     
                S3_key_name = '/' + os.path.join(root.replace(full_source_path, ''), kwargs['prefix'],file_name).strip('/')
    
                command = ['s3cmd', 'put', path, 'S3://'+kwargs['bucket']+S3_key_name]
                
                if kwargs['config']: 
                    command.append('-c')
                    command.append(kwargs['config'])
                
                if kwargs['verbose']: print ' '.join(command)
                
                if not kwargs['dryrun']:
                    if subprocess.call(command) == 0:
                        if kwargs['verbose']: print 'Deleting "%s"' % (path, )
                        if not kwargs['dryrun']: os.remove(path)
                    else:
                        print 'warning: non-zero error code'
                
            if not kwargs['recursive']: break
    
    
    
