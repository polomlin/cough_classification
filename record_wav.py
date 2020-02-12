# -*- coding: utf-8 -*-

import pyaudio
import wave
import subprocess

form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 22050 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 2 # seconds to record
dev_index = 2 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = '/tmp/ramdisk/test%d.wav' # name of .wav file

audio = pyaudio.PyAudio() # create pyaudio instantiation

# create pyaudio stream
#stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
#                    input_device_index = dev_index,input = True, \
#                    frames_per_buffer=chunk)

#stream = audio.open(format = form_1, rate = samp_rate, channels = chans, \
#                    input = True, \
#                    frames_per_buffer=chunk)
print("recording")

count = 1
while True:
    frames = []
    audio = pyaudio.PyAudio()
    stream = audio.open(format = form_1, rate = samp_rate, channels = chans, \
                    input = True, \
                    frames_per_buffer=chunk)
    # loop through stream and append audio chunks to frame array
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data = stream.read(chunk)
        frames.append(data)

    print("finished recording")

    # stop the stream, close it, and terminate the pyaudio instantiation
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # save the audio frames as .wav file
    wavefile = wave.open(wav_output_filename % count,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()
    command = 'curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@' + wav_output_filename % count + '"   http://127.0.0.1:8080/cough/inference'
    proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print("program output:", out)
    if count == 1000:
        break
    else:
        count += 1

