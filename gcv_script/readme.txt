gcloud auth application-default login
# change key-file to the sounding spirit key file
gcloud auth activate-service-account --key-file precise-duality-432316-k8-71b151d9db35.json
gcloud auth print-access-token
# copy the token to the header (after bearer)
py app.py