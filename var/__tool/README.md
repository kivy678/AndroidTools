1. NDK를 다운로드
https://developer.android.com/ndk/downloads?hl=ko

2. 안드로이드 툴 체인 생성
$ python3 android-ndk-r21b/build/tools/ --arch x86  --api 24  --install-dir=my-toolchain

3. 크로스 컴파일
$ my-toolchain/bin/i686-linux-android-clang -o example example.c
※ i686=32bit x86_64=64bit

4. dockcross 를 이용한 크로스 컴파일
docker run --rm -v /root/data:/work dockcross/linux-x86 bash -c 'my-toolchain/bin/i686-linux-android-clang -o example example.c'
