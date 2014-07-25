s3shovel
========

Move local files to S3

s3shovel uses s3cmd to upload local files to s3 for archivation, deleting the local files after successfull upload. I use it to move large and outdated files from my virtual server to s3, preserving the somewhat limited storage space provided by the hosting company.

Problem uploading filenames with UTF-8 characters due to known bug in s3cmd 1.0.0
S3cmd can be patched though, look here: http://sourceforge.net/p/s3tools/bugs/120/ 
