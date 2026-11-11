# Modelos do Prisma

Arquivos (ficam em `core/`, onde o codigo os procura; sha256 em `manifests/ecosystem.lock.json`):
- `core/helpers/models/face_detection_yunet_2023mar.onnx` — YuNet (multicam, safe_layout). Fonte: opencv/opencv_zoo.
- `core/assets/models/blaze_face_short_range.tflite` — MediaPipe BlazeFace.
- `core/assets/models/selfie_multiclass_256x256.tflite` — MediaPipe selfie multiclasse.

Baixados no primeiro uso (cache fora da suite): Whisper (faster-whisper), wav2vec2 de alinhamento
por idioma, TransNetV2, pyannote, Parakeet (`PRISMA_PARAKEET_DIR`), RVM (`PRISMA_RVM_ONNX`).
Tamanhos dos caches: ver `caches` no manifesto.
