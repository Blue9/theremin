import pyaudio


if __name__ == '__main__':
    p = pyaudio.PyAudio()

    for i in range(p.get_device_count()):
        device = p.get_device_info_by_index(i)
        print(device['name'], device['defaultSampleRate'])
