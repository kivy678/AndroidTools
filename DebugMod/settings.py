# -*- coding:utf-8 -*-

#############################################################################
import os

#############################################################################
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
VAR_DIR = os.path.join(BASE_DIR, "VAL")

#############################################################################
APK_TOOL = os.path.join(VAR_DIR, "apktool_2.4.1.jar")
DECODE_DIR = os.path.join(BASE_DIR, "decode")

OUT_APK = os.path.join(VAR_DIR, "out.apk")
KEY_APK = os.path.join(VAR_DIR, "key.apk")

MANIFEST = os.path.join(BASE_DIR, r"decode\AndroidManifest.xml")
MANIFEST_WRITE = os.path.join(BASE_DIR, r"decode\AndroidManifest_tmp.xml")

SIGN_KEY_JAR = os.path.join(VAR_DIR, "signapk")

signapk = os.path.join(SIGN_KEY_JAR, "signapk.jar")
certificate = os.path.join(SIGN_KEY_JAR, "certificate.pem")
pk8 = os.path.join(SIGN_KEY_JAR, "key.pk8")

#############################################################################
