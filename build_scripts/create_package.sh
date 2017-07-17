# This script creates zip file that is used to deploy in aws lambda

rm -rf ./output
mkdir output
cp ../*.py ../*.yml output/
cp -rf ../lib/python2.7/site-packages/ output/
cd output
zip -r -X "deployment.zip" *
