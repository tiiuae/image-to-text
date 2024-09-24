Building:

	cd data/image2text_docker
	./build.sh
	
Starting:

	cd data/image2text_docker
	./start.sh path/to/image-to-text
	
Testing:

	cd data/image2text_docker
	./test.sh
	
For the whole speech-text-image-text-speech pipeline you can move `data/image2text_docker/narration.sh` and `data/image2text_docker/text2speech` to the top of image-to-text, download corresponding repositories and launch it.

	https://github.com/tiiuae/image-to-text
	https://github.com/tiiuae/voicerecognition/
	https://github.com/tiiuae/CameraFetcher
	
