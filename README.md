# cough classification

# how to use 
#servier site
python inference.py


# client site
curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@/home/xxx/xxx/cough/asr/test/no/0d6394ae340047028efea4fc0c8eb4190020.wav"   http://127.0.0.1:8080/cough/inference


# response json format
{"response":{"cough": True}}
# and
{"response":{"cough": False}}

