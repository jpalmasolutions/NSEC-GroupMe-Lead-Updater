time_stamp=$(date +"%b_%d_%Y_%H_%M_%S")
function_name=nsec-groupme-lead-updater
bucket=jpalmasolutions
key=zip/$function_name/$time_stamp.zip
artifact_name=s3://$bucket/$key
pipenv lock -r > requirements.txt
pip3 install -r requirements.txt --no-deps -t lambda
mkdir lambda/src
cp -r src/* lambda/src/
cd lambda
zip -r lambda.zip *
mv lambda.zip ..
cd ..
rm requirements.txt
aws s3 cp lambda.zip $artifact_name
rm lambda.zip
rm -r lambda

aws lambda update-function-code --function-name $function_name \
--s3-bucket $bucket \
--s3-key $key

sleep 5

aws lambda update-function-configuration --function-name $function_name \
--environment file://deploy/environment-variables.json