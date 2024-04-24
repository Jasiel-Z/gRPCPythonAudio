import grpc
import pyaudio

import audio_pb2
import audio_pb2_grpc


def streamAudio(stub, nombre_archivo):
    #se envia el nombre del archivo por el stub
    respuesta = stub.downloadAudio(audio_pb2.
        DownloadFileRequest(nombre = nombre_archivo))

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=2, 
        rate=48000, output=True)
    print("Reproduciendo el archivo " + nombre_archivo)
    for audio_chunk in respuesta:
        print(".", end="", flush=True)
        stream.write(audio_chunk.data)
    print("\nRecepción de datos correcta")
    print("\nReproducción terminada", end="\n\n")


def run():
    puerto = "9001"
    channel = grpc.insecure_channel("localhost:" + puerto)
    stub = audio_pb2_grpc.AudioServiceStub(channel)
    nombreArchivo = ""

    try:
        nombreArchivo = "anyma.wav"
        streamAudio(stub,nombreArchivo)
    except KeyboardInterrupt:
        pass
    finally:
        channel.close()


if __name__ == "__main__":
    run()