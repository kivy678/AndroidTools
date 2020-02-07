# -*- coding:utf-8 -*-

import os
import shutil
import shlex
import subprocess

from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

VAR_DIR = os.path.join(BASE_DIR, "VAL")
APK_TOOL = os.path.join(VAR_DIR, "apktool_2.4.1.jar")
DECODE_DIR = os.path.join(BASE_DIR, "decode")

TEST_APK = os.path.join(VAR_DIR, "sample.apk")
OUT_APK = os.path.join(VAR_DIR, "out.apk")
KEY_APK = os.path.join(VAR_DIR, "key.apk")

MANIFEST = os.path.join(BASE_DIR, r"decode\AndroidManifest.xml")
MANIFEST_WRITE = os.path.join(BASE_DIR, r"decode\AndroidManifest_tmp.xml")

SIGN_KEY_JAR = os.path.join(BASE_DIR, "signapk")
signapk = os.path.join(SIGN_KEY_JAR, "signapk.jar")
certificate = os.path.join(SIGN_KEY_JAR, "certificate.pem")
pk8 = os.path.join(SIGN_KEY_JAR, "key.pk8")


def readManifest():

    try:
        with open(MANIFEST) as fr:
            soup = BeautifulSoup(fr, "lxml-xml")
            soup.application['android:debuggable'] = 'true'

            with open(MANIFEST_WRITE, "w", encoding='utf-8') as fw:
                fw.write(str(soup))
    except Exception as e:
        print(e)
        exit()


def fileManger():

    try:
        os.remove(MANIFEST)
        os.rename(MANIFEST_WRITE, MANIFEST)
    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":

    print("[*] start decode")
    cmd = f"java -jar {APK_TOOL} d -f -o {DECODE_DIR} {TEST_APK}"
    subprocess.call(shlex.split(cmd, posix=False))

    readManifest()
    fileManger()

    print("[*] start build")
    cmd = f"java -jar {APK_TOOL} b -f -o {OUT_APK} {DECODE_DIR}"
    subprocess.call(shlex.split(cmd, posix=False))

    print("[*] sign code")
    cmd = f"java -jar {signapk} {certificate} {pk8} {OUT_APK} {KEY_APK}"
    subprocess.call(shlex.split(cmd, posix=False))

    print("[*] File Cleanup")
    shutil.rmtree(DECODE_DIR, ignore_errors=True)
    os.remove(OUT_APK)

    print("Main End...")
